from halc import get_client
from .get import StorageNotFound


class StorageDeletionFailed(Exception):
    pass


def delete_storage(
    project_id: str,
    storage_id: str,
) -> dict:
    """Delete a storage
    :param project_id: Id of the project
    :param storage_id: Id of the storage
    :return: status of the operation
    """
    client = get_client()
    try:
        res = client.delete(f"/projects/storage/{project_id}/{storage_id}")
        if res.status_code == 204:
            return StorageNotFound(f"storage with id '{storage_id}' not found")
        return {"status": "ok"}
    except Exception:
        raise StorageDeletionFailed(f"could not delete srorage with id '{storage_id}'")
