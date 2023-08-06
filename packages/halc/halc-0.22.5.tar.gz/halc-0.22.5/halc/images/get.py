from halc.initialize import get_client
from halc.projects import get_project


class ImagesGetFailed(Exception):
    pass


class S3ImagesGetFailed(Exception):
    pass


def get_images(
    project_id: str,
) -> list[dict]:
    """Get project images
    :param project_id: Id of the project
    :return: list of the images spec in the project
    """
    client = get_client()
    try:
        res = client.get(f"/images/{project_id}")
        images = res.json()
        return images
    except:
        raise ImagesGetFailed(
            f"failed to get images from project with id '{project_id}'"
        )


def get_s3_images(
    project_id: str,
    storage_id: str,
) -> list[dict]:
    """Get images from an S3 bucket
    :param project_id: Id of the project
    :param storage_id: Id of the storage
    :return: list of the image paths on the bucket
    """

    # Assert the user has access to the project
    client = get_client()
    get_project(project_id)

    try:
        res = client.post(f"/projects/storage/sync/{project_id}/{storage_id}", None)
        images = res.json()
        return images
    except:
        raise ImagesGetFailed(
            f"failed to sync images from S3 storage with id '{storage_id}'"
        )
