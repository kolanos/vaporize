from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class Change(DotDict):
    pass


class Domain(DotDict):
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

    def update(self, ttl=None, emailAddress=None, comment=None):
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
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id'])])
        url = query(url, deleteSubdomains=subdomains)
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    def records(self):
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'records'])
        session = get_session()
        response = session.get(munge_url(url))
        self['records'] = handle_response(response, Record, 'records',
                                          domain_id=self['id'])
        return self['records']

    def subdomains(self):
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'subdomains'])
        session = get_session()
        response = session.get(munge_url(url))
        self['subdomains'] = handle_response(response, Subdomain, 'domains',
                                             domain_id=self['id'])
        return self['subdomains']

    def changes(self, since):
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'changes'])
        url = query(url, since=str(since))
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Change, 'changes')

    def export_zone(self):
        url = '/'.join([get_url('clouddns'), 'domains', str(self['id']),
                        'export'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Export)


class Export(DotDict):
    pass


class Nameserver(DotDict):
    def __repr__(self):
        if 'name' in self:
            return '<Nameserver %s>' % self['name']
        return super(Nameserver, self).__repr__()


class Record(DotDict):
    def __repr__(self):
        if 'name' in self:
            return '<Record %s>' % self['name']
        return super(Record, self).__repr__()

    @classmethod
    def create(cls, name, type, data, ttl=300, priority=None, comment=None):
        if ttl is not None:
            ttl = int(ttl)
        if priority is not None:
            priority = int(priority)
        return cls(name=name, type=type, data=data, ttl=ttl, priority=priority,
                   comment=comment)

    def reload(self):
        url = '/'.join([get_url('clouddns'), 'domains', str(self['domain_id']),
                        'records', str(self['id'])])
        session = get_session()
        response = session.get(munge_url(url))
        self = handle_response(response, Record)
        return self


class Subdomain(DotDict):
    def __repr__(self):
        if 'name' in self:
            return '<Subdomain %s>' % self['name']
        return super(Nameserver, self).__repr__()

    @classmethod
    def create(cls, name, comment=None, emailAddress=None):
        return cls(name=name, comment=comment, emailAddress=None)


def list(limit=None, offset=None, filter=None):
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
    data = {'domains': [{'contentType': type,
                         'contents': contents}]}
    data = json.dumps(data)
    url = '/'.join([get_url('clouddns'), 'import'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, Domain, 'domains')
