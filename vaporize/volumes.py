from vaporize.core import get_url, handle_request
from vaporize.utils import DotDict


class Volume(DotDict):
    """A CloudBlockStorage Volume."""

    def delete(self):
        """Delete this CloudBlockStorage volum."""
        assert 'id' in self
        url = '/'.join((get_url('cloudblockstorage'), 'volumes',
            str(self['id'])))
        handle_request('delete', url)

    @classmethod
    def list(cls, detail=False):
        """Returns a list of volumes.

        :param detail: Provides more details about the volume
        :type detail: bool
        :type: A list of :class:`Volume`
        """
        url = [get_url('cloudblockstorage'), 'volumes']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='volumes')

    @classmethod
    def get(cls, volume_id):
        """Returns a Volume by id

        :param volume_id: The ``volume_id`` of the Volume to be retrieved
        :type volume_id: str
        :returns: A :class:`Volume`
        """
        url = '/'.join((get_url('cloudblockstorage'), 'volumes',
            str(volume_id)))
        return handle_request('get', url, wrapper=cls, container='volume')

    @classmethod
    def types(cls):
        """Returns a list of volume types."""
        url = '/'.join((get_url('cloudblockstorage'), 'types'))
        return handle_request('get', url, container='volume_types')

    @classmethod
    def describe_type(cls, volume_type_id):
        """Returns info about :param volume_type_id.

        :param volume_type_id: One of the ids returned by the types() call.
        :type volume_type_id: int
        """
        url = '/'.join((get_url('cloudblockstorage'), 'types',
            str(volume_type_id)))
        return handle_request('get', url, container='volume_type')
