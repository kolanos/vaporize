# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, handle_request
from vaporize.resources import (Resource, CloudServer, Createable, Modifyable,
                                Deleteable, Findable, Listable, Reloadable)

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


class BackupSchedule(Resource):
    """A CloudServers Backup Schedule."""

    IDENTIFIER = ['daily', 'weekly']

    @classmethod
    def create(cls, weekly=None, daily=None):
        return cls(weekly=weekly, daily=daily)

    def to_dict(self):
        ret = {'backupSchedule': {'enabled': True}}
        if self.weekly:
            ret['backupSchedule']['weekly'] = self.weekly
        if self.daily:
            ret['backupSchedule']['daily'] = self.daily
        return ret


class Flavor(CloudServer, Findable, Listable):
    """A CloudServers Flavor."""

    pass


class Image(CloudServer, Createable, Modifyable, Findable, Listable,
            Deleteable, Reloadable):
    """A CloudServers Image."""

    def __setitem__(self, key, value):
        if key == 'serverId':
            key = 'server_id'
        if key in ['created', 'updated']:
            value = convert_datetime(value)
        super(Image, self).__setitem__(key, value)

    @classmethod
    def create(cls, name, server):
        """Create an Image.

        :param name: Name of the Image.
        :type name: str
        :param server: Server or ``id`` to base the Image upon.
        :type server: int or :class:`Server`
        :returns: A shiny new CloudServers Image.
        :rtype: :class:`Image`

        .. versionadded:: 0.1
        """
        if isinstance(server, Server):
            server = server.id
        data = {'image': {'serverId': server,
                          'name': name}}
        return super(Image, cls).create(data)


class IP(Resource):
    """A CloudServers IP Address."""

    IDENTIFIER = ['public', 'private']


class Server(CloudServer, Createable, Modifyable, Findable, Listable,
             Deleteable, Reloadable):
    """A CloudServers Server."""

    def __setitem__(self, key, value):
        if key == 'addresses':
            value = IP(value)
        super(Server, self).__setitem__(key, value)

    def modify(self, name=None, password=None):
        """Modify this Server's name or root password.

        :param name: Change the server's name.
        :type name: str
        :param password: Change the server's root password.
        :type password: str
        :returns: A modified CloudServers Server.
        :rtype: :class:`Server`

        .. versionadded:: 0.1
        """
        data = {'server': {}}
        if name is not None:
            data['server']['name'] = name
        if password is not None:
            data['server']['adminPass'] = password
        super(Server, self).modify(data)

    @property
    def ips(self):
        """Returns a list of public and private IPs for this Server.

        :returns: A list of public and private IPs for this server.
        :rtype: A list of :class:`IP`.

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            assert 'id' in self, 'Missing id attribute.'
            url = '/'.join([self.BASE_URL, str(self.id), 'ips'])
            response = handle_request('get', url, wrapper=IP,
                                      container='addresses')
            self.addresses = response
        return self.addresses

    @property
    def public_ips(self):
        """Returns the Server's Public IP.

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            self.addresses = IP()
        if 'public' not in self.addresses:
            assert 'id' in self, 'Missing id attribute.'
            url = '/'.join([self.BASE_URL, str(self.id), 'ips', 'public'])
            response = handle_request('get', url, wrapper=IP)
            self.addresses.update(**response)
        return self.addresses.public

    @property
    def private_ips(self):
        """Returns the Server's Private IP.

        .. versionadded:: 0.1
        """
        if 'addresses' not in self:
            self.addresses = IP()
        if 'private' not in self.addresses:
            assert 'id' in self, 'Missing id attribute'
            url = '/'.join([self.BASE_URL, str(self.id), 'ips', 'private'])
            response = handle_request('get', url, wrapper=IP)
            self.addresses.update(**response)
        return self.addresses.private

    def share_ip(self, address, ipgroup, configure=True):
        """Share this Server's IP in a Shared IP Group.

        :param address: IP to share in the Shared IP Group
        :type address: str
        :param ipgroup: A :class:`SharedIpGroup` or ``id``
        :type ipgroup: int or :class:`SharedIpGroup`
        :param configure: Configure the shared IP on the Server
        :type configure: bool
        :returns: The Shared IP Group associated with this Server.
        :rtype: :class:`SharedIpGroup`

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        if isinstance(ipgroup, SharedIpGroup):
            ipgroup = ipgroup.id
        data = json.dumps({'shareIp': {'sharedIpGroup': ipgroup,
                                       'configureServer': configure}})
        url = '/'.join([self.BASE_URL, str(self.id), 'ips', 'public',
                        address])
        handle_request('put', url, data=data)

    def unshare_ip(self, address):
        """Unshare this Server's IP

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        url = '/'.join([self.BASE_URL, str(self.id), 'ips', 'public',
                        address])
        handle_request('delete', url)

    def reboot(self, type='SOFT'):
        """Perform a soft/hard reboot on this Server.

        :param type: A reboot type (``SOFT`` or ``HARD``).
        :type type: str

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        assert type in ['SOFT', 'HARD'], 'Reboot type must be "SOFT" or "HARD"'
        data = json.dumps({'reboot': {'type': type}})
        url = '/'.join([self.BASE_URL, str(self.id), 'action'])
        handle_request('post', url, data)

    def rebuild(self, image):
        """Rebuild this Server using a specified Image.

        :param image: The Image or ``id``
        :type image: int or :class:`Image`

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        if isinstance(image, Image):
            image = image.id
        data = json.dumps({'rebuild': {'imageId': int(image)}})
        url = '/'.join([self.BASE_URL, str(self.id), 'action'])
        handle_request('post', url, data)

    def resize(self, flavor):
        """Resize this Server to a specific Flavor size.

        :param flavor: The Flavor or ``id``
        :type flavor: int or :class:`Flavor`

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        if isinstance(flavor, Flavor):
            flavor = flavor.id
        data = json.dumps({'resize': {'flavorId': flavor}})
        url = '/'.join([self.BASE_URL, str(self.id), 'action'])
        handle_request('post', url, data)

    def confirm_resize(self):
        """Confirm a successful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        data = json.dumps({'confirmResize': None})
        url = '/'.join([self.BASE_URL, str(self.id), 'action'])
        handle_request('post', url, data)

    def revert_resize(self):
        """Revert an unsuccessful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        data = json.dumps({'revertResize': None})
        url = '/'.join([self.BASE_URL, str(self.id), 'action'])
        handle_request('post', url, data)

    @property
    def backup_schedule(self):
        """Return this Server's backup schedule

        :return: :class:`BackupSchedule`

        .. versionadded:: 0.1
        """
        if 'backup_schedule' not in self:
            assert 'id' in self, 'Missing id attribute'
            url = '/'.join([self.BASE_URL, str(self.id),
                            'backup_schedule'])
            response = handle_request('get', url, wrapper=BackupSchedule,
                                      container='backupSchedule')
            self.backup_schedule = response
        return self.backup_schedule

    @backup_schedule.setter
    def backup_schedule(self, schedule):
        """Enable a backup schedule for this Server

        :param schedule: A BackupSchedule instance 
        :type schedule: :class:`BackupSchedule`

            >>> server = vaporize.servers.Server.find(...)
            >>> bs = vaporize.servers.BackupSchedule.create(weekly=...,
            ...                                             daily=...)
            >>> server.backup_schedule = bs


        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        assert isinstance(schedule, BackupSchedule)
        url = '/'.join([self.BASE_URL, str(self.id), 'backup_schedule'])
        handle_request('post', url, schedule.to_dict())
        self.backup_schedule = schedule

    @backup_schedule.deleter
    def backup_schedule(self):
        """Disable a backup schedule for this Server

            >>> server = vaporize.servers.Server.find(...)
            >>> del server.backup_schedule

        .. versionadded:: 0.1
        """
        assert 'id' in self, 'Missing id attribute'
        url = '/'.join([self.BASE_URL, str(self.id), 'backup_schedule'])
        handle_request('delete', url)
        del self.backup_schedule

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
        if isinstance(flavor, Flavor):
            flavor = flavor.id
        data = {'server': {'name': name,
                           'imageId': image,
                           'flavorId': flavor,
                           'metadata': metadata or {},
                           'personality': []}}
        if isinstance(files, dict):
            for path, contents in list(files.items()):
                data['personality'].append({'path': path,
                                            'contents': contents})
        return super(Server, cls).create(data)


class SharedIpGroup(CloudServer, Findable, Listable, Deleteable):
    """A Cloudservers Shared IP Group."""

    def __setitem__(self, key, value):
        if key == 'sharedIpGroupId':
            key = 'id'
        if key == 'configuredServer':
            key = 'configured'
        super(SharedIpGroup, self).__setitem__(key, value)

    @classmethod
    def create(cls, name, server):
        """Create a Shared IP Group.

        :param name: Name of the Shared IP Group
        :type name: str
        :param server: The Server or ``id`` to add to group
        :type server: int or :class:`Server`
        :returns: A shiny new CloudServers Shared IP Group.
        :rtype: :class:`SharedIpGroup`

        .. versionadded:: 0.1
        """
        if isinstance(server, Server):
            server = server.id
        data = {'sharedIpGroup': {'name': name,
                                  'server': server}}
        return super(SharedIpGroup, cls).create(data)
