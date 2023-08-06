from enum import IntEnum

from halc.initialize import get_client
from halc.projects import get_project

class StorageCheckFailed(Exception):
    pass


class StorageCreationFailed(Exception):
    pass


class StorageType(IntEnum):
    S3 = 1


def check_s3_storage_permissions(
    bucket_name: str,
    region: str,
) -> dict:
    """Check permissions on existing S3 bucket
    :param bucket_name: name of the existing S3 bucket
    :param region: region of the bucket
    :return: permissions
    """

    # Get client
    client = get_client()

    try:
        res = client.post(
            "/projects/storage/check",
            {
                "type": StorageType.S3,
                "bucket_name": bucket_name,
                "region": region,
            },
        )
        permissions = res.json()
        return permissions
    except Exception:
        raise StorageCheckFailed(
            f"could not check storage with bucket name '{bucket_name}' in region '{region}'"
        )


def create_s3_storage(
    project_id: str,
    bucket_name: str,
    region: str,
) -> dict:
    """Create storage for an existing S3 bucket
    :param project_id: Id of the project
    :param bucket_name: name of the existing S3 bucket
    :param region: region of the bucket
    :return: storage spec
    """

    # Assert the name
    bucket_name = bucket_name.strip()
    if bucket_name is None or bucket_name == "":
        raise StorageCreationFailed(f"name {bucket_name} is invalid")

    # Assert the name
    region = region.strip()
    if region is None or region == "":
        raise StorageCreationFailed(f"region {region} is invalid")

    # Check storage permissions
    permissions = check_s3_storage_permissions(bucket_name, region)
    if not permissions["list"] or not permissions["read"]:
        raise StorageCreationFailed(
            f"invalid permissions: {permissions}. Read the docs at https://docs.happyrobot.ai"
        )

    # Get project
    client = get_client()
    project = get_project(project_id)

    try:
        res = client.post(
            f"/projects/storage/{project['id']}",
            {
                "type": StorageType.S3,
                "bucket_name": bucket_name,
                "region": region,
            },
        )
        storage = res.json()
        return storage
    except Exception:
        raise StorageCreationFailed(
            f"could not create storage with bucket name '{bucket_name}' in region '{region}'"
        )
