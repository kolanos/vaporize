# -*- coding: utf-8 -*-

import json

from .core import convert_datetime, get_url, handle_request
from .resources import Resource


class Volume(Resource):
    """A CloudBlockStorage Volume."""

    def __repr__(self):
        if 'display_name' in self:
            return '<Volume %s>' % self['display_name']
        return super(Volume, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'display_name':
            key = 'name'
        elif key == 'display_description':
            key = 'description'
        elif key == 'createdAt':
            key = 'created_at'
            value = convert_datetime(value)
        super(Volume, self).__setitem__(key, value)

    def delete(self):
        """Delete this CloudBlockStorage Volume."""
        assert 'id' in self
        url = '/'.join([get_url('cloudblockstorage'), 'volumes',
                        str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls):
        """Returns a list of Volumes.

        """
        url = [get_url('cloudblockstorage'), 'volumes']
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='volumes')

    @classmethod
    def find(cls, id):
        """Returns a Volume by ID.

        :param id: The ``id`` of the Volume to be retrieved
        :type id: str
        :returns: A :class:`Volume`
        """
        url = '/'.join([get_url('cloudblockstorage'), 'volumes', str(id)])
        return handle_request('get', url, wrapper=cls, container='volume')

    @classmethod
    def create(cls, size, name=None, description=None, snapshot=None,
               volume_type=None):
        """Create a CloudBlockStorage Volume.

        :param size: Volume size in GB (min. 100GB max. 1TB).
        :type size: int
        :param name: Name of Volume.
        :type name: str
        :param description: Description of Volume.
        :type description: str
        :param snapshot: Snapshot_ID or :class:`Snapshot` of the volume restore.
        :type snapshot: int or :class:`Snapshot`
        :param volume_type: Volume Type, either ``SATA`` or ``SSD``.
        :type volume_type: str or :class:`VolumeType`
        """
        assert 100  <= int(size) <= 1000
        data = {'volume': {'size': int(size)}}
        if name:
            data['volume']['display_name'] = str(display_name)
        if description:
            data['volume']['display_descrition'] = str(description)
        if snapshot:
            if isinstance(snapshot, Snapshot):
                snapshot = snapshot.id
            data['volume']['snapshot_id'] = int(snapshot)
        if volume_type:
            if isinstance(volume_type, VolumeType):
                volume_type = volume_type.name
            data['volume']['volume_type'] = str(volume_type)
        data = json.dumps(data)
        url = '/'.join([get_url('cloudblockstorage'), 'volumes'])
        return handle_request('post', url, data, cls, 'volume')


class VolumeType(Resource):
    """A CloudBlockStorage Volume Type."""

    def __repr__(self):
        if 'name' in self:
            return '<VolumeType %s>' % self['name']
        return super(VolumeType, self).__repr__()

    @classmethod
    def list(cls):
        """Returns a list of CloudBlockStorage Volume Types."""
        url = '/'.join((get_url('cloudblockstorage'), 'types'))
        return handle_request('get', url, wrapper=cls, container='volume_types')

    @classmethod
    def find(cls, id):
        """Returns a CloudBlockStorage Volume Type.

        :param id: One of the IDs returned by the types() call.
        :type volume_type_id: int
        """
        url = '/'.join([get_url('cloudblockstorage'), 'types', str(id)])
        return handle_request('get', url, wrapper=cls, container='volume_type')


class Snapshot(Resource):
    """A CloudBlockStorage Snapshot."""

    def __repr__(self):
        if 'display_name' in self:
            return '<Snapshot %s>' % self['name']
        return super(Snapshot, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'display_name':
            key = 'name'
        elif key == 'display_description':
            key = 'description'
        elif key == 'createdAt':
            key = 'created_at'
            value = convert_datetime(value)
        super(Snapshot, self).__setitem__(key, value)

    def delete(self):
        """Delete this CloudBlockStorage Snapshot."""
        assert 'id' in self
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots',
                        str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls):
        """Returns a list of Snapshots.

        :returns: A list of :class:`Snapshot`
        """
        url = [get_url('cloudblockstorage'), 'snapshots']
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='snapshots')

    @classmethod
    def find(cls, id):
        """Returns a Snapshot by ID

        :param id: The ``id`` of the snapshot to be retrieved
        :type volume_id: str
        :returns: A :class:`Snapshot`
        """
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots', str(id)])
        return handle_request('get', url, wrapper=cls, container='snapshot')

    @classmethod
    def create(cls, volume, force=False, name=None, description=None):
        """Create a CloudBlockStorage Snapshot.

        :param volume: Volume_ID or :class:`Volume` to snapshot.
        :type volume: int or :class:`Volume`
        :param force: Force volume snapshot.
        :type force: bool
        :param name: Display name of volume.
        :type name: str
        :param description: Display description of volume.
        :type description: str
        """
        assert volume
        if isinstance(volume, Volume):
            volume = volume.id
        data = {'snapshot': {'volume_id': str(volume)}}
        if force:
            data['snapshot']['force'] = bool(force)
        if name:
            data['snapshot']['display_name'] = str(name)
        if description:
            data['snapshot']['display_descrition'] = str(description)
        data = json.dumps(data)
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots'])
        return handle_request('post', url, data, cls, 'snapshot')
