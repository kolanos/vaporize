import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict

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
    """A CloudServers Backup Schedule"""
    def __repr__(self):
        if 'daily' in self:
            return '<BackupSchedule %s>' % self['daily']
        if 'weekly' in self:
            return '<BackupSchedule %s>' % self['weekly']
        return super(BackupSchedule, self).__repr__()


class IP(dict):
    """A CloudServer IP Address"""
    def __repr__(self):
        if 'public' in self:
            return '<IP %s>' % self['public'][0]
        if 'private' in self:
            return '<IP %s>' % self['private'][0]
        return super(IP, self).__repr__()


class Server(DotDict):
    """A CloudServer Server"""
    def __repr__(self):
        if 'name' in self:
            return "<Server %s>" % self['name']
        return super(Server, self).__repr__()

    def reload(self):
        """reload this Server (implicit ``get``)

        :returns: self
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id'])])
        session = get_session()
        response = session.get(munge_url(url))
        self = handle_response(response, Server, 'server')
        return self

    def update(self, name=None, password=None):
        """Update this Server

        :param name: Change the Server's name
        :type name: str
        :param password: Change the Server's root password
        :type password: str
        :returns: self
        """
        assert 'id' in self
        data = {'server': {}}
        if name:
            data['server']['name'] = name
        if password:
            data['server']['adminPass'] = password
        data = json.dumps(data)
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id'])])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if response:
            if name:
                self.name = name
        return self

    def delete(self):
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id'])])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def ips(self):
        """
        Returns a list of public and private IPs for this Server
        
        :returns: A list of IP types
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, IP, 'addresses')

    @property
    def public_ips(self):
        """Returns the Server's Public IP"""
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'public'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, IP)

    @property
    def private_ips(self):
        """Returns the Server's Private IP"""
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'private'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, IP)

    def share_ip(self, address, ipgroup, configure=True):
        """Share this Server's IP in a Shared IP Group"""
        assert 'id' in self
        data = json.dumps({'shareIp': {'sharedIpGroup': int(ipgroup),
                                       'configureServer': configure}})
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'public', address])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response, IP)

    def unshare_ip(self, address):
        """Unshare this Server's IP"""
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'ips', 'public', address])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    def soft_reboot(self):
        """Perform a soft reboot on this Server"""
        assert 'id' in self
        data = json.dumps({'reboot': {'type': 'SOFT'}})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def hard_reboot(self):
        """Perform a hard reboot on this Server"""
        assert 'id' in self
        data = json.dumps({'reboot': {'type': 'HARD'}})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def rebuild(self, image):
        """Rebuild this Server using a specified Image"""
        assert 'id' in self
        data = json.dumps({'rebuild': {'imageId': int(image)}})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def resize(self, flavor):
        """Resize this Server to a specific Flavor size"""
        assert 'id' in self
        data = json.dumps({'resize': {'flavorId': int(flavor)}})
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def confirm_resize(self):
        """Confirm a successful resize operation"""
        assert 'id' in self
        data = json.dumps({'confirmResize': None})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def revert_resize(self):
        """Revert an unsuccessful resize operation"""
        assert 'id' in self
        data = json.dumps({'revertResize': None})
        url = '/'.join([get_url('cloudservers'), 'servers',
                        str(self['id']), 'action'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    @property
    def backup_schedule(self):
        """Return this Server's backup schedule"""
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'backup_schedule'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, BackupSchedule, 'backupSchedule')

    def enable_backup_schedule(self, weekly, daily):
        """Enable a backup schedule for this Server"""
        assert 'id' in self
        data = {'backupSchedule': {'enable': True,
                                   'weekly': weekly,
                                   'daily': daily}}
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'backup_schedule'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response)

    def disable_backup_schedule(self):
        """Disable a backup schedule for this Server"""
        assert 'id' in self
        url = '/'.join([get_url('cloudservers'), 'servers', str(self['id']),
                        'backup_schedule'])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)


def list(limit=None, offset=None, detail=False):
    """
    List of CloudServer Servers

    :param limit: Limit the result set to a certain number
    :type limit: int
    :param offset: Offset the result set by a certain number
    :type offset: int
    :param detail: Return detailed information about each Server
    :type detail: bool
    :returns: List of Servers
    """
    url = [get_url('cloudservers'), 'servers']
    if detail:
        url.append('detail')
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Server, 'servers')


def get(id):
    """
    Return a Server using an ID

    :param id: The ID ofthe Server to be retrieved
    :type id: int
    :return: A Server
    """
    url = '/'.join([get_url('cloudservers'), 'servers', str(id)])
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Server, 'server')


def create(name, image, flavor, metadata=None, files=None):
    data = {'server': {'name': name,
                       'imageId': int(image),
                       'flavorId': int(flavor),
                       'metadata': metadata or {},
                       'personality': []}}
    if isinstance(files, dict):
        for path, contents in files.items():
            data['personality'].append({'path': path, 'contents': contents})
    data = json.dumps(data)
    url = '/'.join([get_url('cloudservers'), 'servers'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, Server, 'server')
