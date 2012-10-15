# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict


class Change(DotDict):
    """A CloudDNS Change History."""
    pass


class Domain(DotDict):
    """A CloudDNS Domain."""
    def __repr__(self):
        if 'name' in self:
            return '<Domain %s>' % self.name
        return super(Domain, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'recordsList':
            key = 'records'
            value = [Record(v) for v in value['records']]
        elif key == 'subdomains':
            value = [Subdomain(v) for v in value['domains']]
        elif key in ['created', 'updated']:
            value = convert_datetime(value)
        super(Domain, self).__setitem__(key, value)

    def reload(self):
        """
        Reload this Domain (an implicit :func:`get`).

        :returns: An updated Domain.
        :rtype: :class:`Domain`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        response = self.get(self['id'])
        self.update(response)
        return self

    def modify(self, ttl=None, email_address=None, comment=None):
        """Modify this Domain's properties.

        :param ttl: Time-To-Live (TTL0 in seconds
        :type ttl: int
        :param email_address: E-mail address associated with Domain
        :type email_address: str
        :param comment: A comment or note about this Domain
        :type comment: str
        :returns: A :class:`Domain`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {}
        if ttl is not None:
            data['ttl'] = int(ttl)
        if email_address is not None:
            data['emailAddress'] = email_address
        if comment is not None:
            data['comment'] = comment
        data = json.dumps(data)
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        handle_request('put', url, data)
        if ttl is not None:
            self['ttl'] = int(ttl)
        if email_address is not None:
            self['email_address'] = email_address
        if comment is not None:
            self['comment'] = comment
        return self

    def delete(self, subdomains=False):
        """Delete this Domain.

        .. warning::

            There is no confirmation step to this operation. Deleting this
            domain is permanent. If in doubt you can export a copy of the DNS
            zone (:func:`vaporize.domains.Domain.export_zone`) before deleting.

        :param subdomains: Delete this Domain's Subdomains (optional)
        :type subdomains: bool

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        url = query(url, deleteSubdomains=subdomains)
        handle_request('delete', url)

    @property
    def records(self):
        """Returns a list of CloudDNS Records.

        :returns: A list of Records.
        :rtype: A list of :class:`Record`

        .. versionadded:: 0.1
        """
        if 'records' not in self:
            assert 'id' in self
            url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                            'records'])
            response = handle_request('get', url,
                                      wrapper=Record,
                                      container='records',
                                      domain_id=self['id'])
            self['records'] = response
        return self['records']

    def add_records(self, *records):
        """Add Records to a Domain.

            >>> domain = vaporize.domains.create(...)
            >>> record1 = vaporize.domains.Record.create(....)
            >>> record2 = vaporize.domains.Record.create(...)
            >>> domain.add_recrods(record1, record2)

        :param records: Records you wish to add to this Domain.
        :type records: :class:`Record`
        :returns: A list of Records
        :rtype: :class:`Record`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'records': []}
        for record in records:
            if isinstance(record, Record):
                data['records'].append({
                    'name': record.name,
                    'type': record.type,
                    'data': record.data,
                    'ttl': record.ttl,
                    'priority': record.priority,
                    'comment': record.comment
                    })
        data = json.dumps(data)
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'records'])
        self['records'] = handle_request('post', url, data, Record, 'records',
                                          domain_id=self['id'])
        return self['records']

    def remove_record(self, record):
        """Remove a Record from this Domain.

        :param record: A Record or ``id`` for the Record to remove.
        :type record: int or :class:`REcord`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        record = record.id if isinstance(record, Record) else record
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'records', str(record)])
        handle_request('delete', url)

    @property
    def subdomains(self):
        """Returns a list of Subdomains.

        :returns; A list of Subdomains.
        :rtype: A list of :class:`Subdomain`

        .. versionadded:: 0.1
        """
        if 'subdomins' not in self:
            assert 'id' in self
            url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                            'subdomains'])
            response = handle_request('get', url, wrapper=Subdomain,
                                      container='domains',
                                      domain_id=self['id'])
            self['subdomains'] = response
        return self['subdomains']

    def changes(self, since):
        """Returns a list of CloudDNS changes for this domain.

        :param since: A datetime as a starting point.
        :type since: str or datetime
        :returns: A list of Changes
        :rtype: A list of :class:`Change`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'changes'])
        url = query(url, since=str(since))
        return handle_request('get', url, wrapper=Change, container='changes')

    @property
    def export_zone(self):
        """Export the raw BIND zone for this Domain.

        :returns: An :class:`Export` containing the raw BIND zone

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'export'])
        return handle_request('get', url, wrapper=Export)

    @classmethod
    def list(cls, limit=None, offset=None, filter=None):
        """List of Domains.

        :param limit: Limit the number of results returned
        :type limit: int
        :param offset: Offset the result set by a certain amount
        :type offset: int
        :param filter: Filter results by a domain name
        :type filter: str
        :returns: A list of Domains
        :rtype: A list of :class:`Domain`

        .. versionadded:: 0.1
        """
        url = [get_url('clouddns'), 'domains']
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        if filter is not None:
            url = query(url, name=filter)
        return handle_request('get', url, wrapper=cls, container='domains')

    @classmethod
    def get(cls, id, records=False, subdomains=False):
        """Retrieve a Domain using an ID.

        :param records: Include the Domain's Records in the result
        :type records: bool
        :param subdomains: Include the Domain's Subdomainsi n the result
        :type subdomains: bool
        :returns: A Domain with the specified ID.
        :rtype: :class:`Domain`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('clouddns'), 'domains', str(id)])
        if records is True:
            url = query(url, showRecords='true')
        if subdomains is True:
            url = query(url, showSubdomains='true')
        return handle_request('get', url, wrapper=cls)

    @classmethod
    def create(cls, name, ttl=300, records=None, subdomains=None, comment=None,
               email_address=None):
        """Create a CloudDNS Domain.

        :param name: A domain name such as ``yourname.com``
        :type name: str
        :param ttl: Time-To-Live (TTL) in seconds
        :type ttl: int
        :param records: A list of Records to create
        :type records: list of :class:`Record`
        :param subdomains: A list of Subdomains to create
        :type subdomains: list of :class:`Subdomain`
        :param comment: An optional comment to associated with the domain
        :type comment: str
        :param email_address: An e-mail address to associated with the domain
        :type email_address: str
        :returns: A shiny new Domain.
        :rtype: :class:`Domain`

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
                            'priority': record.priority,
                            'comment': record.comment
                            })
        if create_ns_records:
                data['domains'][0]['recordsList']['records'].append({
                        'name': name,
                        'type': 'NS',
                        'data': 'dns1.stabletransit.com',
                        'ttl': 3600
                        })
                data['domains'][0]['recordsList']['records'].append({
                        'name': name,
                        'type': 'NS',
                        'data': 'dns2.stabletransit.com',
                        'ttl': 3600
                        })
        if isinstance(subdomains, (list, tuple)):
            for subdomain in subdomains:
                if isinstance(subdomain, Subdomain):
                    data['domains'][0]['subdomains']['domains'].append({
                            'name': subdomain.name,
                            'emailAddress': subdomain.email_address,
                            'comment': subdomain.comment
                            })
        if comment is not None:
            data['domains'][0]['comment'] = comment
        if email_address is not None:
            data['domains'][0]['email_address'] = email_address
        data = json.dumps(data)
        url = '/'.join([get_url('clouddns'), 'domains'])
        return handle_request('post', url, data, cls, 'domains')

    @classmethod
    def import_zone(cls, contents, type='BIND_9'):
        """Import a raw BIND zone into CloudDNS.

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
        return handle_request('post', url, data, cls, 'domains')


class Export(DotDict):
    """A CloudDNS BIND Zone Export."""
    pass


class Nameserver(DotDict):
    """A CloudDNS Nameserver."""
    def __repr__(self):
        if 'name' in self:
            return '<Nameserver %s>' % self['name']
        return super(Nameserver, self).__repr__()


class Record(DotDict):
    """A CloudDNS Record."""
    def __repr__(self):
        if 'name' in self:
            return '<Record %s>' % self['name']
        return super(Record, self).__repr__()

    def __setitem__(self, key, value):
        if key in ['created', 'updated']:
            value = convert_datetime(value)
        super(Record, self).__setitem__(key, value)

    @classmethod
    def create(cls, name, type, data, ttl=None, priority=None, comment=None):
        """Create a CloudDNS Record.

        .. important::

            This is only a factory method. In order for the Record to be
            created on CloudDNS you must add the :class:`Record` this method
            returns to an existing :class:`Domain`.

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
        """Reload a Record.

        :returns: A Record
        :rtype: :class:`Record`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'domain_id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['domain_id']),
                                'records', str(self['id'])])
        response = handle_request('get', url, wrapper=Record)
        self.update(response)
        return self

    def modify(self, name=None, data=None, ttl=None):
        """Modify this Record's properties.

        :param name: Modify the Record's name.
        :type ttl: str
        :param data: Modify the Record's data.
        :type data: str
        :param ttl: Modify the Record's time-to-live (TTL).
        :type ttl: int
        :returns: A list of Records.
        :rtype: A list of :class:`Record`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'domain_id' in self
        data = {}
        if name is not None:
            data['name'] = name
        if data is not None:
            data['data'] = data
        if ttl is not None:
            data['ttl'] = int(ttl)
        data = json.dumps(data)
        url = '/'.join([get_url('clouddns'), 'domains', str(self['domain_id']),
                        'records', str(self['id'])])
        handle_request('put', url, data)
        if name is not None:
            self['name'] = name
        if data is not None:
            self['data'] = data
        if ttl is not None:
            self['ttl'] = int(ttl)
        return self

    def delete(self, subdomains=False):
        """Delete this Record.

        .. warning::

            There is no confirmation step to this operation. Deleting this
            record is permanent. If in doubt you can export a copy of the DNS
            zone (:func:`vaporize.domains.Domain.export_zone`) before deleting.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'domain_id' in self
        url = '/'.join([get_url('clouddns'), 'domains', str(self['domain_id']),
                        'records', str(self['id'])])
        handle_request('delete', url)


class Subdomain(DotDict):
    """A CloudDNS Subdomain."""
    def __repr__(self):
        if 'name' in self:
            return '<Subdomain %s>' % self['name']
        return super(Nameserver, self).__repr__()

    @classmethod
    def create(cls, name, comment=None, email_address=None):
        """Create a Subdomain.

        .. important::

            This is only a factory method. In order for the Subdomain to be
            created the :class:`Subdomain` returned by this method must be
            added to an existing CloudDNS :class:`Domain`.

        :param name: A subdomain such as ``www.yourdomain.com``
        :type name: str
        :param comment: An optional comment associated with the subdomain
        :type comment: str
        :param email_address: An e-mail address associated with the subdomain
        :type email_address: str
        :returns: A Subdomain
        :rtype: :class:`Subdomain`

        .. versionadded:: 0.1
        """
        return cls(name=name, comment=comment, email_address=None)
