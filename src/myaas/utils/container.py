import docker
from os import getenv

from .. import settings

client = docker.Client(base_url=settings.DOCKER_SOCKET)


def find_container(name):
    # prepend / to name
    name = '/{}'.format(name)
    containers = client.containers(all=True)
    containers = [c for c in containers if name in c['Names']]
    if not containers:
        return None
    return containers[0]


def list_containers(all=True):
    client = docker.Client()
    return client.containers(all=all)


def translate_host_basedir(path):
    # TODO: if container is created with a custom hostname this will not work
    # improve self id detection in the future.
    self_id = getenv('HOSTNAME')
    self_container = client.containers(filters={'id': self_id})[0]

    for mount in self_container['Mounts']:
        if mount['Destination'] == settings.BASE_DIR:
            break

    if mount['Destination'] != settings.BASE_DIR:
        raise KeyError("Could not find %s mountpoint" % settings.BASE_DIR)

    return path.replace(mount['Destination'], mount['Source'], 1)