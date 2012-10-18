# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict


STATUSES = {
    "BUILD": "The database instance is being provisioned.",
    "REBOOT": "The database instance is rebooting.",
    "ACTIVE": ("The database instance is online and available to take "
               "requests."),
    "BLOCKED": "The database instance is unresponsive at the moment.",
    "RESIZE": "The database instance is being resized at the moment.",
    "SHUTDOWN": ("The database instance is terminating services. Also, "
                 "SHUTDOWN is returned if for any reason the MySQL instance "
                 "is shut down but not the actual server."),
    "FAILED": "The database instance was not created due to an error."
}


class Database(DotDict):
    """A CloudDatabase Database."""
    def __repr__(self):
        if 'name' in self:
            return '<Database %s>' % self['name']
        return super(Database, self).__repr__()

    def delete(self):
        """Deletes the specified database.

        This operation deletes the requested database within the specified
        database instance. Note that all data associated with the database is
        also deleted.

        .. warning::

            There is no confirmation step for this operation.

        .. versionadded:: 0.2
        """
        assert 'name' in self, "missing Database Name"
        assert 'instance_id' in self, "Missing Instance ID"
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['instance_id']), 'databases',
                        str(self['name'])])
        handle_request('delete', url)

    @classmethod
    def create(cls, name, character_set='utf8', collate='utf8_general_ci'):
        """Create a CloudDatabase Database.

        .. note::

            Must be added to a CloudDatabase Instance before it is created.

        :param name: Name of the CloudDatabase Database.
        :type name: str
        :param character_set: Character set for the CloudDatabase Database
            (default: utf8).
        :type character_set: str
        :param collate: Collation for the CloudDatabase Database (default:
            utf8_general_ci).
        :type collate: str
        :returns: A shiny new CloudDatabases Database.
        :rtype: :class:`Database`

        .. versionadded:: 0.2
        """
        return cls(name=name, character_set=character_set, collate=collate)

    def to_dict(self):
        return dict([(k, self[k]) for k in ['name', 'character_set',
                                            'collate']])

class Flavor(DotDict):
    """A CloudDatabase Flavor"""
    def __repr__(self):
        if 'name' in self:
            return '<Flavor %s>' % self['name']
        return super(Flavor, self).__repr__()

    @classmethod
    def list(cls, limit=None, offset=None):
        """Lists information for all available flavors.

        This operation lists information for all available flavors.

        :param limit: Limit the result set by a number
        :type limit: int
        :param offset: Offset the result set by a number
        :type offset: int
        :returns: A list of CloudDatabases Flavors.
        :rtype: list of :class:`Flavor`

        .. versionadded:: 0.2
        """
        url = '/'.join([get_url('clouddatabases'), 'flavors'])
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls, container='flavors')

    @classmethod
    def get(cls, id):
        """Lists all flavor information about the specified flavor ID.

        This operation lists all information for the specified flavor ID with
        details of the RAM.

        :param id: The ID of the Flavor to retrieve.
        :type id: int
        :returns: A CloudDatabases Flavor matching the ID.
        :rtype: :class:`Flavor`

        .. versionadded:: 0.2
        """
        url = '/'.join([get_url('clouddatabases'), 'flavors', str(id)])
        return handle_request('get', url, wrapper=cls, container='flavor')

    @property
    def ref(self):
        """Returns the self link reference."""
        return [l['href'] for l in self['links'] if l['rel'] == 'self'][0]

class Instance(DotDict):
    """A CloudDatabase Instance."""
    def __repr__(self):
        if 'name' in self:
            return '<Instance %s>' % self['name']
        return super(Instance, self).__repr__()

    def __setitem__(self, key, value):
        if key in ['created', 'updated']:
            value = convert_datetime(value)
        elif key == 'databases':
            value = [Database(v, instance_id=self.get('id')) for v in value]
        elif key == 'flavor':
            value = Flavor(value)
        elif key == 'users':
            value = [User(v, instance_id=self.get('id')) for v in value]
        elif key == 'volume':
            value = Volume(value)
        super(Instance, self).__setitem__(key, value)

    def reload(self):
        """Reload this CloudDatabases Instance.

        :returns: An updated CloudDatabases Instance.
        :rtype: :class:`Instance`

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Missing Instance ID"
        response = Instance.get(self['id'])
        self.update(response)
        return self

    def delete(self):
        """Delete this CloudDatabases Instance.

        This operation deletes the specified database instance, including any
        associated data.

        .. warning::

            There is not confirmation step for this operation. Deleting an
            image is permanent.

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Missing Instance ID"
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['id'])])
        handle_request('delete', url)

    @property
    def databases(self):
        """Lists databases for the specified instance.

        This operation lists the databases for the specified instance.

        :returns: A list of Databases for this Instance.
        :rtype: list of :class:`Database`

        .. versionadded:: 0.2
        """
        if 'databases' not in self:
            assert 'id' in self, "Missing Instance ID"
            url = '/'.join([get_url('clouddatabases'), 'insances',
                            str(self['id']), 'databases'])
            response = handle_request('get', url, data, Database, 'databases',
                                      instance_id=self['id'])
            self['databases'] = response
        return self['databases']

    def add_databases(self, *databases):
        """Creates a new database within the specified instance.

        This operation creates a new database within the specified instance.

        :param databases: Databases to add to CloudDatabases Instance.
        :type databases: :class:`Database`

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Mising Instance ID"
        data = {'databases': []}
        for database in databases:
            if isinstance(database, Database):
                data['databases'].append(database.to_dict())
        data = json.dumps(data)
        url = '/'.join([get_url('clouddatabases'), 'insances', str(self['id']),
                        'databases'])
        handle_request('post', url, data)

    @property
    def users(self):
        """Lists the users in the specified database instance.

        This operation lists the users in the specified database instance, along
        with the associated databases for that user.

        :returns: A list of Users for this Instance.
        :rtype: list of :class:`User`

        .. versionadded:: 0.2
        """
        if 'users' not in self:
            assert 'id' in self, "Missing Instance ID"
            url = '/'.join([get_url('clouddatabases'), 'insances',
                            str(self['id']), 'users'])
            response = handle_request('get', url, data, User, 'users',
                                      instance_id=self['id'])
            self['users'] = response
        return self['users']

    def add_users(self, *users):
        """Creates a user for the specified database instance.

        This operation asynchronously provisions a new user for the specified
        database instance based on the configuration defined in the request
        object. Once the request is validated and progress has started on the
        provisioning process, a 202 Accepted response object is returned.

        :param users: Users to add to CloudDatabases Instance.
        :type databases: :class:`User`

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Mising Instance ID"
        data = {'users': []}
        for user in users:
            if isinstance(user, User):
                data['users'].append(user.to_dict())
        data = json.dumps(data)
        url = '/'.join([get_url('clouddatabases'), 'insances', str(self['id']),
                        'users'])
        handle_request('post', url, data)

    @property
    def root_enabled(self):
        """
        Returns true if root user is enabled for the specified database
        instance or false otherwise.

        This operation checks an active specified database instance to see if
        root access is enabled. It returns True if root user is enabled for the
        specified database instance or False otherwise.

        :returns: Status of whether root access is enabled.
        :rtype: bool

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Missing Instance ID"
        if 'root_enabled' not in self:
            url = '/'.join([get_url('clouddatabases'), 'instances',
                            str(self['id']), 'root'])
            self['root_enabled'] = handle_request('get', url, bool,
                                                  'rootEnabled')
        return self['root_enabled']

    def enable_root(self):
        """Enable root access for this CloudDatabase Instance.

        This operation enables login from any host for the root user and
        provides the user with a generated root password.

        :returns: The root user's credentials for the Instance.
        :rtype: :class:`User`

        .. versionadded:: 0.2
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['id']), 'root'])
        return handle_request('post', url, wrapper=User, container='user')

    def restart(self):
        """Restart the database service on the instance.

        The restart operation will restart only the MySQL Instance. Restarting
        MySQL will erase any dynamic configuration settings that you have made
        within MySQL.

        .. versionadded:: 0.2
        """
        assert 'id' in self
        data = json.dumps({'restart': {}})
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['id']), 'action'])
        handle_request('post', url, dataa)

    def resize(self, flavor=None, size=None):
        """Resize the memory and/or volume of the instance.

        This operation changes the memory and/or volume size of the instance,
        assuming a valid Flavor is provided. Restarts MySQL in the process.

        :param flavor: New Flavor (memory size) ofr the Instance.
        :type flavor: :class:`Flavor`
        :param size: New volume size Iin GBs) for Instance, 1 to 25.
        :type size: int

        .. versionadded:: 0.2
        """
        assert 'id' in self, "Missing Instance ID"
        if isinstance(flavor, Flavor):
            flavor = flavor.ref
        data = {'resize': {}}
        if flavor is not None:
            data['resize']['flavorRef'] = flavor
        if size is not None:
            data['resize']['volume'] = {'size': int(size)}
        data = json.dumps(data)
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['id']), 'action'])
        handle_request('post', url, data)
 
    @classmethod
    def list(cls):
        """Returns a list of CloudDatabase instances.

        This operation lists the status and information for all database
        instances.

        :returns: A list of CloudDatabase instances.
        :rtype: :class:`Instance`

        .. versionadded:: 0.2
        """
        url = '/'.join([get_url('clouddatabases'), 'instances'])
        return handle_request('get', url, wrapper=cls, container='instances')

    @classmethod
    def get(cls, id):
        """Returns an Instance by ID.

        This operation lists the status and details of the specified database
        instance.

        :param id: The ID of the Instance to retrieve.
        :type id: int
        :returns: A CloudDatabases Instance matching the ID.
        :rtype: :class:`Instance`

        .. versionadded:: 0.2
        """
        url = '/'.join([get_url('clouddatabases'), 'instances', str(id)])
        return handle_request('get', url, wrapper=cls, container='instance')

    @classmethod
    def create(cls, name, flavor, size, databases, users):
        """Create a CloudDatabases Instance.

        This operation asynchronously provisions a new database instance. This
        call requires the user to specify a flavor and a volume size. The
        service then provisions the instance with the requested flavor and sets
        up a volume of the specified size, which is the storage for the
        database instance.

        :param name: Name of the Instance.
        :type name: str
        :param flavor: The Flavor of the CloudDatabase instance.
        :type flavor: :class:`Flavor`
        :param size: Specifies the volume size in gigabytes (GB). The value
            specified must be between 1 and 10.
        :type size: int
        :param databases: A list of Databases to create for the instance.
        :type databases: list of :class:`Database`
        :param users: A list of Users to create for the instance.
        :type users: list of :class:`User`
        :returns: A shiny new CloudDatabases Instance.
        :rtype: :class:`Instance`

        .. versionadded:: 0.2
        """
        if isinstance(flavor, Flavor):
            flavor = flavor.ref
        data = {'instance': {'name': name,
                             'flavorRe': flavor,
                             'size': int(size),
                             'databases': [],
                             'users': []}}
        if isinstance(databases, (list, tuple)):
            for database in databases:
                if isinstance(database, Database):
                    data['databases'].append(database.to_dict())
        if isinstance(users, (list, tuple)):
            for user in users:
                if isinstance(user, User):
                    data['users'].append(user.to_dict())
        data = json.dumps(data)
        url = '/'.join([get_url('clouddatabases'), 'instances'])
        return handle_request('post', url, data, cls, 'instance')


class User(DotDict):
    """A CloudDatabases User."""
    def __repr__(self):
        if 'name' in self:
            return '<Instance %s>' % self['name']
        return super(Instance, self).__repr__()

    def delete(self):
        """
        Deletes the user identified by {name} for the specified database
        instance.

        This operation deletes the specified user for the specified database
        instance.

        .. warning::

            There is no confirmation step for this operation.

        .. versionadded:: 0.2
        """
        assert 'name' in self, "Missing User Name"
        assert 'instance_id' in self, "Missing Instance ID"
        url = '/'.join([get_url('clouddatabases'), 'instances',
                        str(self['instance_id']), 'users',
                        str(self['name'])])
        handle_request('delete', url)

    @classmethod
    def create(cls, name, password, *databases):
        """Create a CloudDatabase User.

        .. note::

            Must be added to a CloudDatabase Instance before it is created.

        :param name: Username of the Database User.
        :type name: str
        :param password: Password for the Database User.
        :type password: str
        :param databases: Databases that the User should have full access.
        :type databases: :class:`Database`
        :returns: A shiny new CloudDatabases User.
        :rtype: :class:`User`

        .. versionadded:: 0.2
        """
        assert all([isinstance(d, Database) for d in databases]), \
            "Must be Database instance(s)"
        return cls(name=name, password=password, databases=list(databases))

    def to_dict(self):
        ret = {'name': self['name'], 'password': self['password']}
        ret['databases'] = [{'name': d['name']} for d in self['databases']]
        return ret


class Volume(DotDict):
    """A CloudDatabase Volume."""
    def __repr__(self):
        if 'used' in self and 'size' in self:
            return '<Volume %.2f%%>' % ((self['used'] / self['size']) * 100.0)
        return super(Volume, self).__repr__()
