from halc import get_client
from halc.projects import get_project


class StorageNotFound(Exception):
    pass


class StoragesListFailed(Exception):
    pass


def list_storages(
    project_id: str,
) -> list:
    """List storages in project
    :param project_id: Id of the project
    :return: list of storages specs
    """
    client = get_client()
    try:
        res = client.get(f"/projects/storage/{project_id}")
        storages = res.json()
        return storages
    except Exception:
        raise StoragesListFailed(
            f"failed to list storages in project with id '{project_id}'"
        )
