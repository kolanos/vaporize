# -*- coding: utf-8 -*-

import json

from vaporize.core import get_url, handle_request
from vaporize.utils import DotDict


class Volume(DotDict):
    """A CloudBlockStorage Volume."""

    def __repr__(self):
        if 'display_name' in self:
            return '<Volume %s>' % self['display_name']
        return super(Volume, self).__repr__()

    def delete(self):
        """Delete this CloudBlockStorage volume."""
        assert 'id' in self
        url = '/'.join([get_url('cloudblockstorage'), 'volumes',
            str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls):
        """Returns a list of volumes.

        """
        url = [get_url('cloudblockstorage'), 'volumes']
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='volumes')

    @classmethod
    def find(cls, volume_id):
        """Returns a Volume by id

        :param volume_id: The ``volume_id`` of the Volume to be retrieved
        :type volume_id: str
        :returns: A :class:`Volume`
        """
        url = '/'.join([get_url('cloudblockstorage'), 'volumes',
            str(volume_id)])
        return handle_request('get', url, wrapper=cls, container='volume')

    @classmethod
    def create(cls, size, display_description='', display_name='',
            snapshot_id='', volume_type=''):
        """Returns info about :param volume_type_id.

        :param size: volume size in GB (min. 100GB max. 1TB).
        :type : str
        :param display_description: display description.
        :type : str
        :param display_name: display name.
        :type : str
        :param snapshot_id: snapshot_id of the volume to be restored.
        :type : str
        :param volume_type: volume type.
        :type : str
        """
        assert 100  <= int(size) <= 1000
        data = { 'volume': { 'size': int(size)}}
        if display_description:
            data['volume']['display_descrition'] = str(display_description)
        if display_name:
            data['volume']['display_name'] = str(display_name)
        if snapshot_id:
            data['volume']['snapshot_id'] = str(snapshot_id)
        if volume_type:
            data['volume']['volume_type'] = str(volume_type)
        data = json.dumps(data)
        url = '/'.join([get_url('cloudblockstorage'), 'volumes'])
        return handle_request('post', url, data, cls, 'volume')


class Type(DotDict):
    """A CloudBlockStorage Type."""

    def __repr__(self):
        if 'name' in self:
            return '<Type %s>' % self['name']
        return super(Type, self).__repr__()

    @classmethod
    def list(cls):
        """Returns a list of volume types."""
        url = '/'.join((get_url('cloudblockstorage'), 'types'))
        return handle_request('get', url, wrapper=cls, container='volume_types')

    @classmethod
    def describe(cls, volume_type_id):
        """Returns info about :param volume_type_id.

        :param volume_type_id: One of the ids returned by the types() call.
        :type volume_type_id: int
        """
        url = '/'.join([get_url('cloudblockstorage'), 'types',
            str(volume_type_id)])
        return handle_request('get', url, wrapper=cls, container='volume_type')


class Snapshot(DotDict):
    """A CloudBlockStorage Snapshot."""

    def __repr__(self):
        if 'display_name' in self:
            return '<Snapshot %s>' % self['display_name']
        return super(Snapshot, self).__repr__()

    def delete(self):
        """Delete this CloudBlockStorage snapshot."""
        assert 'id' in self
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots',
            str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls, detail=False):
        """Returns a list of snapshots.

        :type: A list of :class:`Snapshot`
        """
        url = [get_url('cloudblockstorage'), 'snapshots']
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='snapshots')

    @classmethod
    def find(cls, id):
        """Returns a Snapshot by id

        :param id: The ``id`` of the snapshot to be retrieved
        :type volume_id: str
        :returns: A :class:`Snapshot`
        """
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots',
            str(volume_id)])
        return handle_request('get', url, wrapper=cls, container='snapshot')

    @classmethod
    def create(cls, volume_id, force=False, display_description='',
            display_name=''):
        """Returns info about :param volume_type_id.

        :param volume_id: volume_id to snapshot.
        :type : str
        :param force: force volume snapshot
        :type : bool
        :param display_description: display description.
        :type : str
        :param display_name: display name.
        :type : str
        """
        assert volume_id
        data = { 'snapshot': { 'volume_id': str(volume_id)}}
        if display_description:
            data['snapshot']['display_descrition'] = str(display_description)
        if display_name:
            data['snapshot']['display_name'] = str(display_name)
        if force:
            data['snapshot']['force'] = 'True'
        data = json.dumps(data)
        url = '/'.join([get_url('cloudblockstorage'), 'snapshots'])
        return handle_request('post', url, data, cls, 'snapshot')
