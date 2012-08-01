# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict

BACKUP_WEEKLY_DISABLED  = 'DISABLED'
BACKUP_WEEKLY_SUNDAY    = 'SUNDAY'
BACKUP_WEEKLY_MONDAY    = 'MONDAY'
BACKUP_WEEKLY_TUESDAY   = 'TUESDAY'
BACKUP_WEEKLY_WEDNESDAY = 'WEDNESDAY'
BACKUP_WEEKLY_THURSDAY  = 'THURSDAY'
BACKUP_WEEKLY_FRIDAY    = 'FRIDAY'
BACKUP_WEEKLY_SATURDAY  = 'SATURDAY'

BACKUP_DAILY_DISABLED    = 'DISABLED'
BACKUP_DAILY_H_0000_0200 = 'H_0000_0200'
BACKUP_DAILY_H_0200_0400 = 'H_0200_0400'
BACKUP_DAILY_H_0400_0600 = 'H_0400_0600'
BACKUP_DAILY_H_0600_0800 = 'H_0600_0800'
BACKUP_DAILY_H_0800_1000 = 'H_0800_1000'
BACKUP_DAILY_H_1000_1200 = 'H_1000_1200'
BACKUP_DAILY_H_1200_1400 = 'H_1200_1400'
BACKUP_DAILY_H_1400_1600 = 'H_1400_1600'
BACKUP_DAILY_H_1600_1800 = 'H_1600_1800'
BACKUP_DAILY_H_1800_2000 = 'H_1800_2000'
BACKUP_DAILY_H_2000_2200 = 'H_2000_2200'
BACKUP_DAILY_H_2200_0000 = 'H_2200_0000'


class BackupSchedule(DotDict):
    """A CloudServers Backup Schedule."""
    def __repr__(self):
        if 'daily' in self:
            return '<BackupSchedule %s>' % self['daily']
        if 'weekly' in self:
            return '<BackupSchedule %s>' % self['weekly']
        return super(BackupSchedule, self).__repr__()

    @classmethod
    def create(cls, weekly=None, daily=None):
        return cls(weekly=weekly, daily=daily)

    def to_dict(self):
        ret = {'backupSchedule': {'enabled': True}}
        if self.weekly:
            ret['backupSchedule']['weekly'] = self.weekly
        if self.daily:
            self['backupSchedule']['daily'] = daily
        return ret


class Flavor(DotDict):
    """A CloudServers Flavor."""
    def __repr__(self):
        if 'name' in self:
            return '<Flavor %s>' % self['name']
        return super(Flavor, self).__repr__()

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of Flavors.

        :param limit: Limit the result set by a number
        :type limit: int
        :param offset: Offset the result set by a number
        :type offset: int
        :param detail: Return additional details about each Flavor
        :type: bool
        :returns: A list of CloudServers Flavors.
        :rtype: :class:`Flavor`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudservers'), 'flavors']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls, container='flavors')

    @classmethod
    def get(cls, id):
        """Returns a Flavor by ID.

        :param id: The ID of the Flavor to retrieve
        :type id: int
        :returns: A CloudServers Flavor matching the ID.
        :rtype: :class:`Flavor`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudservers'), 'flavors', str(id)])
        return handle_request('get', url, wrapper=cls, container='flavor')


class Image(DotDict):
    """A CloudServers Image."""
    def __repr__(self):
        if 'name' in self:
            return '<Image %s>' % self['name']
        return super(Image, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'serverId':
            key = 'server_id'
        elif key in ['created', 'updated']:
            value = convert_datetime(value)
        super(Image, self).__setitem__(key, value)

    def reload(self):
        """Reload this Image (an implicit :func:`get`).

        :returns: An updated CloudServers Image.
        :rtype: :class:`Image`

        .. versionadded:: 0.1.9
        """
        assert 'id' in self, "Missing Image ID"
        response = Image.get(self['id'])
        self.update(response)
        return self

    def delete(self):
        """Delete this Image.

        .. note::

            You can only delete Images you create.

        .. warning::

            There is not confirmation step for this operation. Deleting an
            image is permanent.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'images', str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of CloudServers Images.

        :param limit: Limit the result set by a cetain number
        :type limit: int
        :param offset: Offset the result set by a certain number
        :type offset: int
        :param detail: Return additional details about each Image
        :type detail: bool
        :returns: A list of CloudServers Images.
        :rtype: A list of :class:`Image`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudservers'), 'images']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=Image, container='images')

    @classmethod
    def get(cls, id):
        """Return an Image by ID.

        :param id: The ID of the Image to retrieve
        :type id: int
        :returns: A CloudServer Image matching the ID.
        :rtype: :class:`Image`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudservers'), 'images', str(id)])
        return handle_request('get', url, wrapper=cls, container='image')

    @classmethod
    def create(cls, name, server):
        """Create an Image.

        :param name: Name of the Image
        :type name: str
        :param server: Server or ``id`` to base the Image upon
        :type server: int or :class:`Server`
        :returns: A shiny new CloudServers Image.
        :rtype: :class:`Image`

        .. versionadded:: 0.1
        """
        if isinstance(server, Server):
            server = server.id
        server = int(server)
        data = {'image': {'serverId': server,
                          'name': name}}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudservers'), 'images'])
        return handle_request('post', url, data, cls, 'image')


class IP(DotDict):
    """A CloudServers IP Address."""
    def __repr__(self):
        if 'public' in self:
            return '<IP %s>' % self['public'][0]
        if 'private' in self:
            return '<IP %s>' % self['private'][0]
        return super(IP, self).__repr__()


class Server(DotDict):
    """A CloudServers Server."""
    def __repr__(self):
        if 'name' in self:
            return "<Server %s>" % self['name']
        return super(Server, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'addresses':
            value = IP(value)
        super(Server, self).__setitem__(key, value)

    def reload(self):
        """Reload this Server (an implicit :func:`get`).

        :returns: An updated CloudServers Server.
        :rtype: :class:`Server`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        response = Server.get(self['id'])
        self.update(response)
        return self

    def modify(self, name=None, password=None):
        """Modify this Server's name or root password.

        :param name: Change the Server's name
        :type name: str
        :param password: Change the Server's root password
        :type password: str
        :returns: A modified CloudServers Server.
        :rtype: :class:`Server`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'server': {}}
        if name is not None:
            data['server']['name'] = name
        if password is not None:
            data['server']['adminPass'] = password
        data = json.dumps(data)
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id'])])
        response = handle_request('put', url, data=data)
        if response:
            if name is not None:
                self['name'] = name
        return self

    def delete(self):
        """Delete this Server.

        .. warning::

            There is no confirmation step for this operation. When you delete a
            server it is permanent. If in doubt, create a backup image
            (:func:`vaporize.images.create`) first before deleting.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id'])])
        handle_request('delete', url)

    @property
    def ips(self):
        """
        Returns a list of public and private IPs for this Server.

        :returns: A list of public and private IPs for this Server.
        :rtype: A list of :class:`IP`

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                            'ips'])
            response = handle_request('get', url, wrapper=IP,
                                      container='addresses')
            self['addresses'] = response
        return self['addresses']

    @property
    def public_ips(self):
        """Returns the Server's Public IP.

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            self['addresses'] = IP()
        if 'public' not in self['addresses']:
            assert 'id' in self
            url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                            'ips', 'public'])
            response = handle_request('get', url, wrapper=IP)
            self['addresses'].update(response)
        return self['addresses']['public']

    @property
    def private_ips(self):
        """Returns the Server's Private IP.

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            self['addresses'] = IP()
        if 'private' not in self['addresses']:
            assert 'id' in self
            url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                            'ips', 'private'])
            response = handle_request('get', url, wrapper=IP)
            self['addresses'].update(response)
        return self['addresses']['private']

    def share_ip(self, address, ipgroup, configure=True):
        """Share this Server's IP in a Shared IP Group.

        :param address: IP to share in the Shared IP Group
        :type address: str
        :param ipgroup: A :class:`SharedIPGroup` or ``id``
        :type ipgroup: int or :class:`SharedIPGroup`
        :param configure: Configure the shared IP on the Server
        :type configure: bool
        :returns: The Shared IP Group associated with this Server.
        :rtype: :class:`SharedIPGroup`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(ipgroup, SharedIPGroup):
            ipgroup = ipgroup.id
        ipgroup = int(ipgroup)
        data = json.dumps({'shareIp': {'sharedIpGroup': ipgroup,
                                       'configureServer': configure}})
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'public', address])
        handle_request('put', url, data=data)

    def unshare_ip(self, address):
        """Unshare this Server's IP

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'public', address])
        handle_request('delete', url)

    def reboot(self, type='SOFT'):
        """Perform a soft/hard reboot on this Server.

        :param type: A reboot type (``SOFT`` or ``HARD``).
        :type type: str

        .. versionadded:: 0.1
        """
        assert 'id' in self, "Missing Server ID"
        assert type in ['SOFT', 'HARD'], "Reboot type must be 'SOFT' or 'HARD'"
        data = json.dumps({'reboot': {'type': type}})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def rebuild(self, image):
        """Rebuild this Server using a specified Image

        :param image: The Image or ``id``
        :type image: int or :class:`Image`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(image, Image):
            image = image.id
        image = int(image)
        data = json.dumps({'rebuild': {'imageId': int(image)}})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def resize(self, flavor):
        """Resize this Server to a specific Flavor size

        :param flavor: The Flavor or ``id``
        :type flavor: int or :class:`Flavor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(flavor, Flavor):
            flavor = flavor.id
        flavor = int(flavor)
        data = json.dumps({'resize': {'flavorId': flavor}})
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'action'])
        handle_request('post', url, data)

    def confirm_resize(self):
        """Confirm a successful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'confirmResize': None})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def revert_resize(self):
        """Revert an unsuccessful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'revertResize': None})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    @property
    def backup_schedule(self):
        """Return this Server's backup schedule

        :return: :class:`BackupSchedule`

        .. versionadded:: 0.1
        """
        if 'backup_schedule' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                            'backup_schedule'])
            response = handle_request('get', url, wrapper=BackupSchedule,
                                      container='backupSchedule')
            self['backup_schedule'] = response
        return self['backup_schedule']

    @backup_schedule.setter
    def backup_schedule(self, schedule):
        """Enable a backup schedule for this Server

        :param schedule: A BackupSchedule instance 
        :type schedule: :class:`BackupSchedule`

            >>> server = vaporize.servers.Server.get(...)
            >>> bs = vaporize.servers.BackupSchedule.create(weekly=...,
            ...                                             daily=...)
            >>> server.backup_schedule = bs


        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert isinstance(schedule, BackupSchedule)
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'backup_schedule'])
        handle_request('post', url, schedule.to_dict())
        self['backup_schedule'] = schedule

    @backup_schedule.deleter
    def backup_schedule(self):
        """Disable a backup schedule for this Server

            >>> server = vaporize.servers.Server.get(...)
            >>> del server.backup_schedule

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'backup_schedule'])
        handle_request('delete', url)
        del self['backup_schedule']

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """
        List of CloudServer Servers

        :param limit: Limit the result set to a certain number
        :type limit: int
        :param offset: Offset the result set by a certain number
        :type offset: int
        :param detail: Return detailed information about each Server
        :type detail: bool
        :returns: A list of CloudServers Servers.
        :rtype: List of :class:`Server`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudservers'), 'servers']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls, container='servers')

    @classmethod
    def get(cls, id):
        """Return a Server using an ID

        :param id: The ``id`` of the Server to be retrieved
        :type id: int
        :return: A :class:`Server`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudservers'), 'servers', str(id)])
        return handle_request('get', url, wrapper=cls, container='server')

    @classmethod
    def create(cls, name, image, flavor, metadata=None, files=None):
        """Create a CloudServers Server

        :param name: A Server's name
        :type name: str
        :param image: An Image or ``id``
        :type image: int or :class:`Image`
        :param flavor: A Flavor or ``id``
        :type flavor: int or :class:`Flavor`
        :param metadata: Optional meta data to include with Server
        :type metadata: dict
        :param files: A list of files to load on Server
        :type files: dict
        :returns: A shiny new CloudServers Server.
        :rtype: :class:`Server`

        .. versionadded:: 0.1
        """
        if isinstance(image, Image):
            image = image.id
        image = int(image)
        if isinstance(flavor, Flavor):
            flavor = flavor.id
        flavor = int(flavor)
        data = {'server': {'name': name,
                           'imageId': image,
                           'flavorId': flavor,
                           'metadata': metadata or {},
                           'personality': []}}
        if isinstance(files, dict):
            for path, contents in list(files.items()):
                data['personality'].append({'path': path, 'contents': contents})
        data = json.dumps(data)
        url = '/'.join([get_url('cloudservers'), 'servers'])
        return handle_request('post', url, data, cls, 'server')


class SharedIPGroup(DotDict):
    """A Cloudservers Shared IP Group."""
    def __repr__(self):
        if 'name' in self:
            return '<SharedIPGroup %s>' % self['name']
        return super(SharedIPGroup, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'sharedIpGroupId':
            key = 'id'
        elif key == 'configuredServer':
            key = 'configured'
        super(SharedIPGroup, self).__setitem__(key, value)

    def delete(self):
        """Delete this Shared IP Group.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'shared_ip_groups',
                        str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of Shared IP Groups.

        :param limit: Limit the result set by a certain number
        :type limit: int
        :param offset: Offset the result set by a certain number
        :type offset: int
        :param detail: Return additional details about each Shared IP Group
        :type detail: bool
        :returns: A list of Shared IP Groups.
        :rtype: A list of :class:`SharedIPGroup`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudservers'), 'shared_ip_groups']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls,
                              container='sharedIpGroups')

    @classmethod
    def get(cls, id):
        """Return a Shared IP Group by ID.

        :param id: The ID of the Shared IP Group to retrieve
        :type id: int
        :returns: A :class:`SharedIPGroup`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudservers'), 'shared_ip_groups', str(id)])
        return handle_request('get', url, wrapper=cls,
                              container='sharedIpGroup')

    @classmethod
    def create(cls, name, server):
        """Create a Shared IP Group.

        :param name: Name of the Shared IP Group
        :type name: str
        :param server: The Server or ``id`` to add to group
        :type server: int or :class:`Server`
        :returns: A shiny new CloudServers Shared IP Group.
        :rtype: :class:`SharedIPGroup`

        .. versionadded:: 0.1
        """
        if isinstance(server, Server):
            server = server.id
        server = int(server)
        data = {'sharedIpGroup': {'name': name,
                                  'server': server}}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudservers'), 'server_ip_groups'])
        return handle_request('post', url, data, cls, 'sharedIpGroup')
