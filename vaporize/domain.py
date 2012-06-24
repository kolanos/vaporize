from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class Change(DotDict):
    """A CloudDNS Change History"""
    pass


class Domain(DotDict):
    """A CloudDNS Domain"""
    def __repr__(self):
        if 'name' in self:
            return '<Domain %s>' % self.name
        return super(Domain, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'recordsList':
            records = []
            for record in value['records']:
                records.append(Record(record))
            super(Record, self).__setitem__('records', records)
        elif key == 'subdomains':
            subdomains = []
            for domain in value['domains']:
                subdomains.append(Subdomain(domain))
            super(Record, self).__setitem__('subdomains', subdomains)
        else:
            super(Domain, self).__setitem__(key, value)

    def reload(self):
        """
        Reload this Domain

        :returns: a :class:`Domain`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Domain)

    def update(self, ttl=None, emailAddress=None, comment=None):
        """
        Update this Domain

        :param ttl: Time-To-Live (TTL0 in seconds
        :type ttl: int
        :param emailAddress: E-mail address associated with Domain
        :type emailAddress: str
        :param comment: A comment or note about this Domain
        :type comment: str
        :returns: A :class:`Domain`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {}
        if ttl is not None:
            data['ttl'] = int(ttl)
        if emailAddress is not None:
            data['emailAddress'] = emailAddress
        if comment is not None:
            data['comment'] = comment
        data = json.dumps(data)
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if response:
            if ttl is not None:
                self['ttl'] = int(ttl)
            if emailAddress is not None:
                self['emailAddress'] = emailAddress
            if comment is not None:
                self['comment'] = comment
        return self

    def delete(self, subdomains=False):
        """
        Delete this Domain
        
        :param subdomains: Delete this Domain's Subdomains (optional)
        :type subdomains: bool

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        url = query(url, deleteSubdomains=subdomains)
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def records(self):
        """
        Returns a list of CloudDNS Records
        
        :returns: A list of :class:`Record`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'records'])
        session = get_session()
        response = session.get(munge_url(url))
        self['records'] = handle_response(response, Record, 'records',
                                          domain_id=self['id'])
        return self['records']

    def subdomains(self):
        """
        Returns a list of Subdomains.
        
        :returns; A list of :class:`Subdomain`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'subdomains'])
        session = get_session()
        response = session.get(munge_url(url))
        self['subdomains'] = handle_response(response, Subdomain, 'domains',
                                             domain_id=self['id'])
        return self['subdomains']

    def changes(self, since):
        """
        Returns a list of CloudDNS changes for this domain.

        :param since: A datetime as a starting point.
        :type since: str
        :returns: A list of :class:`Change`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'changes'])
        url = query(url, since=str(since))
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Change, 'changes')

    def export_zone(self):
        """Export the raw BIND zone for this Domain

        :returns: An :class:`Export` containing the raw BIND zone

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'export'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Export)


class Export(DotDict):
    """A BIND Zone Export"""
    pass


class Nameserver(DotDict):
    """A DNS Nameserver"""
    def __repr__(self):
        if 'name' in self:
            return '<Nameserver %s>' % self['name']
        return super(Nameserver, self).__repr__()


class Record(DotDict):
    """A CloudDNS Record"""
    def __repr__(self):
        if 'name' in self:
            return '<Record %s>' % self['name']
        return super(Record, self).__repr__()

    @classmethod
    def create(cls, name, type, data, ttl=300, priority=None, comment=None):
        """Create a CloudDNS Record

        .. note::

            This is only a factory method. In order for the Record to be created
            on CloudDNS you must add the :class:`Record` this method returns to
            an existing :class:`Domain`.

        :param name: A domain name such as ``www.mydomain.com``
        :type name: str
        :param type: A record type, such as ``A``, ``CNAME``, ``MX``, etc.
        :type type: str
        :param data: Data associated with the record (depends on `type`)
        :type data: str
        :param ttl: Time-To-Live (TTL) in seconds
        :type ttl: int
        :param priority: Weighted priority (required for ``MX`` records)
        :type priority: int
        :param comment: An optional comment or note for this record
        :type comment: str
        :returns: A :class:`Record`

        .. versionadded:: 0.1
        """
        if ttl is not None:
            ttl = int(ttl)
        if priority is not None:
            priority = int(priority)
        return cls(name=name, type=type, data=data, ttl=ttl, priority=priority,
                   comment=comment)

    def reload(self):
        """
        Reload a Record (an implicit ``get``)

        :returns: A :class:`Record`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'domain_id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['domain_id']),
                                'records', str(self['id'])])
        session = get_session()
        response = session.get(munge_url(url))
        self = handle_response(response, Record)
        return self


class Subdomain(DotDict):
    """A CloudDNS Subdomain"""
    def __repr__(self):
        if 'name' in self:
            return '<Subdomain %s>' % self['name']
        return super(Nameserver, self).__repr__()

    @classmethod
    def create(cls, name, comment=None, emailAddress=None):
        """Create a Subdomain

        .. note::

            This is only a factory method. In order for the Subdomain to be
            created the :class:`Subdomain` returned by this method must be added
            to an existing CloudDNS :class:`Domain`.

        :param name: A subdomain such as ``www.yourdomain.com``
        :type name: str
        :param comment: An optional comment associated with the subdomain
        :type comment: str
        :param emailAddress: An e-mail address associated with the subdomain
        :type emailAddress: str
        :returns: A :class:`Subdomain`

        .. versionadded:: 0.1
        """
        return cls(name=name, comment=comment, emailAddress=None)


def list(limit=None, offset=None, filter=None):
    """
    List of Domains

    :param limit: Limit the number of results returned
    :type limit: int
    :param offset: Offset the result set by a certain amount
    :type offset: int
    :param filter: Filter results by a domain name
    :type filter: str
    :returns: List of :class:`Domain`

    .. versionadded:: 0.1
    """
    url = [get_url('clouddns'), 'domains']
    url = '/'.join(url)
    if limit is not None or offset is not None:
        url = query(url, limit=limit, offset=offset)
    if filter is not None:
        url = query(url, name=filter)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Domain, 'domains')


def get(id, records=False, subdomains=False):
    """
    Retrieve a Domain using an ID

    :param records: Include the Domain's Records in the result
    :type records: bool
    :param subdomains: Include the Domain's Subdomainsi n the result
    :type subdomains: bool
    :returns: A :class:`Domain`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('clouddns'), 'domains', str(id)])
    if records is True:
        url = query(url, showRecords='true')
    if subdomains is True:
        url = query(url, showSubdomains='true')
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Domain)


def create(name, ttl=300, records=None, subdomains=None, comment=None,
           emailAddress=None):
    """
    Create a CloudDNS Domain

    :param name: A domain name such as ``yourname.com``
    :type name: str
    :param ttl: Time-To-Live (TTL) in seconds
    :type ttl: int
    :param records: A list of :class:`Record` to create
    :type records: list
    :param subdomains: A list of :class:`Subdomain` to create
    :type suddomains: list
    :param comment: An optional comment to associated with the domain
    :type comment: str
    :param emailAddress: An e-mail address to associated with the domain
    :type emailAddress: str
    :returns: A :class:`Domain`

    .. versionadded:: 0.1
    """
    data = {'domains': [{'name': name,
                         'ttl': int(ttl),
                         'recordsList': {'records': []},
                         'subDomains': {'domains': []}}]}
    create_ns_records = True
    if isinstance(records, (list, tuple)):
        for record in records:
            if isinstance(record, Record):
                if record.type == 'NS':
                    create_ns_records = False
                data['domains'][0]['recordsList']['records'].append({
                        'name': record.name,
                        'type': record.type,
                        'data': record.data,
                        'ttl': record.ttl,
                        'priority': record.get('priority', None),
                        'comment': record.get('comment', None)
                        })
    if create_ns_records:
            data['domains'][0]['recordsList']['records'].append({
                    'name': name,
                    'type': 'NS',
                    'data': 'dns1.stabletransit.com',
                    'ttl' : 3600
                    })
            data['domains'][0]['recordsList']['records'].append({
                    'name': name,
                    'type': 'NS',
                    'data': 'dns2.stabletransit.com',
                    'ttl' : 3600
                    })
    if isinstance(subdomains, (list, tuple)):
        for subdomain in subdomains:
            if isinstance(subdomain, Subdomain):
                data['domains'][0]['subdomains']['domains'].append({
                        'name': subdomain.name,
                        'emailAddress': subdomain.get('emailAddress', None),
                        'comment': subdomain.get('comment', None)
                        })
    if comment is not None:
        data['domains'][0]['comment'] = comment
    if emailAddress is not None:
        data['domains'][0]['emailAddress'] = emailAddress
    data = json.dumps(data)
    url = '/'.join([get_url('clouddns'), 'servers'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, Domain, 'domains')


def import_zone(contents, type='BIND_9'):
    """
    Import a raw BIND zone into CloudDNS

    :param contents: Contents of the BIND zone
    :type contents: str
    :param type: The BIND format type being used, such as ``BIND_9``
    :type type: str
    :returns: A list of :class:`Domain`

    .. versionadded:: 0.1
    """
    data = {'domains': [{'contentType': type,
                         'contents': contents}]}
    data = json.dumps(data)
    url = '/'.join([get_url('clouddns'), 'import'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, Domain, 'domains')
