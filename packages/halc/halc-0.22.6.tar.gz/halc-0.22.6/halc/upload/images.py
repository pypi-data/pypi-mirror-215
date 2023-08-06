from typing import List
from tqdm import tqdm
import os
from uuid import uuid4
import requests
import magic
from PIL import Image
import threading
import queue

from halc import Client, get_client
from halc.projects import get_project
from halc.storage import list_storages, StorageNotFound
from halc.utils import get_random_color


def _upload_image(
    path: str,
    project: dict,
    client: Client,
) -> dict:
    """Upload one image to the database
    :param path: path to the image
    :param project: project spec
    :param client: backend client
    :return: image spec
    """

    # Detect content type
    content_type = magic.from_file(path, mime=True)

    # Open image
    img = Image.open(path)
    w, h = img.size

    # Create image document
    image = {
        "id": str(uuid4()),
        "project_id": project["id"],
        "name": os.path.basename(path),
        "width": w,
        "height": h,
        "content_type": content_type,
        "status": 1,  # Status NEW
        "has_thumbnail": True,
    }

    # Upload to database
    res = client.get(f"/images/signed_put/{project['id']}", {"key": image["name"]})
    url = res.json()["url"]
    data = open(path, "rb").read()
    res = requests.put(
        url,
        data,
        headers={"Content-Type": content_type, "Content-Length": str(len(data))},
    )
    res.raise_for_status()

    return image


def _parse_tags(
    project: dict,
    tags: list[str],
    client: Client,
) -> dict:
    """Parse tags for project
    :param project: project spec
    :param tags: tags to set
    :param client: client to use
    :return: attributes
    """
    tag_ids = []
    project_tags = project["attributes"][0]
    if len(tags) > 0:
        # Map tags to project tags
        project_options = project_tags["options"]
        project_option_names = [opt["name"] for opt in project_options]
        for tag in tags:
            try:
                # Tag exists
                index = project_option_names.index(tag)
                tag_ids.append(project_options[index]["id"])
            except:
                # Create tag option
                opt = {
                    "id": str(uuid4()),
                    "name": tag,
                    "color": get_random_color(),
                }
                project_options.append(opt)
                tag_ids.append(opt["id"])

        # Save options to backend
        client.post(
            f"/attributes/options/{project['id']}/{project_tags['id']}",
            project_options,
        )
    attributes = {project_tags["id"]: tag_ids}
    return attributes


def upload_images(
    paths: List[str],
    project_id: str,
    tags: List[str] = [],
) -> dict:
    """Upload a list of local images to the app
    :param paths: list of paths to images
    :param project_id: Id of the project
    :param tags: list of tags to apply to the uploaded images
    :return: status of the operation
    """

    # Get project from backend
    client = get_client()
    project = get_project(project_id)

    # If tags provided, merge them with existing tags and update the project
    attributes = _parse_tags(project, tags, client)

    # Upload images params
    session_id = str(uuid4())
    total = len(paths)

    # Create queues and progress bar
    read = queue.Queue()
    pbar = tqdm(total=total)

    # Create worker callback
    def worker():
        while True:
            # Read from queue
            path = read.get()

            # Upload image to database
            image = _upload_image(path, project, client)

            # Send update to backend
            image["attributes"] = attributes
            client.post(
                f"/images/{project['id']}",
                [image],
                {"session_id": session_id, "total": total},
            )

            # Update progress bar and set task as done in the queue
            pbar.update(1)
            read.task_done()

    # Spin up workers
    for _ in range(10):
        threading.Thread(target=worker, daemon=True).start()

    # Send paths to the read queue
    for path in paths:
        read.put(path)

    # Wait for queue to empty
    read.join()

    # Finish the progress bar
    pbar.update(total - pbar.n)

    return {"status": "ok", "upload_count": total}


def upload_images_from_dir(
    base_dir: str,
    project_id: str,
    tags: List[str] = [],
    valid_images: List[str] = [".jpg", ".jpeg", ".png", ".tif", ".tiff"],
) -> dict:
    """Upload images from a directory
    :param base_dir: directory where the images live
    :param project_id: Id of the project
    :param tags: list of tags to apply to the uploaded images
    :param valid_images: valid extensions for the image files
    :return: status of the operation
    """

    # Find the images
    files = []
    for f in os.listdir(base_dir):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        files.append(os.path.join(base_dir, f))
    print(f"Found {len(files)} images in {base_dir}")

    # Upload them to the app
    return upload_images(files, project_id, tags)


class ImageRegistrationFailed(Exception):
    pass


def register_images(
    image_names: list[str],
    project_id: str,
    storage_id: str,
    tags: List[str] = [],
    create_thumbnail: bool = False,
) -> dict:
    """Register images to existing storage
    :param image_names: list of image names to register
    :param project_id: Id of the project
    :param storage_id: Id of the storage
    :param tags: list of tags to apply to the registered images
    :param create_thumbnail: Whether to create a thumbnail for every image
    :return: status of the operation
    """

    # Check if storage id in project
    if storage_id not in [storage["id"] for storage in list_storages(project_id)]:
        raise StorageNotFound(f"storage with id '{storage_id}' not found")

    # Get project from backend
    client = get_client()
    project = get_project(project_id)

    # If tags provided, merge them with existing tags and update the project
    attributes = _parse_tags(project, tags, client)

    # Create image specs
    images = [
        {
            "name": name,
            "project_id": project_id,
            "storage_id": storage_id,
            "id": str(uuid4()),
            "has_thumbnail": create_thumbnail,
            "attributes": attributes,
        }
        for name in image_names
    ]

    # Register
    try:
        print(
            f"Registering images. Check the status of the upload at https://app.happyrobot.ai/{project['organization_id']}/{project['id']}"
        )
        client.post(
            f"/images/{project_id}",
            images,
            {"session_id": str(uuid4()), "total": len(images)},
        )
    except Exception:
        raise ImageRegistrationFailed(
            f"could not register images to storage with id '{storage_id}'"
        )
