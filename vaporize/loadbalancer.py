import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.util import DotDict


class AccessRule(DotDict):
    def __repr__(self):
        return '<AccessRule %s %s>' % (self.type, self.address)

    def delete(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.loadbalancer_id), 'accesslist', str(self.id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)


class Algorithm(DotDict):
    def __repr__(self):
        return '<Algorithm %s>' % self.name


class AllowedDomain(DotDict):
    pass


class ContentCaching(DotDict):
    pass


class ConnectionLogging(DotDict):
    pass


class ConnectionThrottle(DotDict):
    pass


class ErrorPage(DotDict):
    pass


class HealthMonitor(DotDict):
    pass


class LoadBalancer(DotDict):
    def __repr__(self):
        return '<LoadBalancer %s>' % self.name

    def reload(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id)])
        session = get_session()
        response = session.get(munge_url(url))
        self = handle_response(response, LoadBalancer, 'loadbalancer')
        return self

    def update(self, name=None, protocol=None, port=None, algorithm=None,
               connection_logging=False):
        data = {'loadBalancer': {}}
        if name:
            data['loadBalancer']['name'] = name
        if algorithm:
            data['loadBalancer']['algorithm'] = algorithm
        if protocol:
            data['loadBalancer']['protocol'] = protocol
        if port:
            data['loadBalancer']['port'] = int(port)
        if connection_logging:
            data['loadBalancer']['connectionLogging'] = bool(connection_logging)
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id)])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if response:
            if name:
                self.name = name
            if algorithm:
                self.algorithm = algorithm
            if protocol:
                self.protocol = protocol
            if port:
                self.port = bool(port)
            if connection_logging:
                self.connectionLogging.enabled = bool(connection_logging)
        return self

    def delete(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def nodes(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'nodes'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, Node, 'nodes', loadbalancer_id=self.id)

    def create_node(self, address, port, condition, type, weight):
        data = {'nodes': [{'address': address,
                           'port': int(port),
                           'condition': condition,
                           'type': type,
                           'weight': int(weight)}]}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'nodes'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response, Node, 'nodes', loadbalancer_id=self.id)

    def delete_node(self, id):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'nodes', str(id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def virtual_ips(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'virtualips'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, VirtualIP, 'virtualIps',
                               loadbalancer_id=self.id)

    def create_virtual_ip(self, type):
        data = json.dumps({'virtualIp': {'ipVersion': 'IPV6', 'type': type}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'virtualips'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response, VirtualIP, 'virtualIp',
                               loadbalancer_id=self.id)

    def delete_virtual_ip(self, id):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'virtualips', str(id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def access_list(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'accesslist'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, AccessRule, 'accessList',
                               loadbalancer_id=self.id)

    def create_access_rule(self, type, address):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'accesslist'])
        session = get_session()
        response = session.post(url)
        return handle_response(response, AccessRule, 'accessList')

    def delete_access_rule(self, id):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'accesslist', str(id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def connection_logging(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionlogging'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ConnectionLogging,
                               'connectionLogging')

    def enable_connection_logging(self):
        data = json.dumps({'connectionLogging': {'enabled': True}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionlogging'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    def disable_connection_logging(self):
        data = json.dumps({'connectionLogging': {'enabled': False}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionlogging'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    @property
    def content_caching(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'contentcaching'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ContentCaching, 'contentCaching')

    def enable_content_caching(self):
        data = json.dumps({'contentCaching': {'enabled': True}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'contentCaching'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    def disable_content_caching(self):
        data = json.dumps({'contentCaching': {'enabled': False}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'contentcaching'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    @property
    def connection_throttle(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionthrottle'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ConnectionThrottle,
                               'connectionThrottle')

    def enable_connection_throttle(self, max_connections, min_connections,
                                   max_connection_rate, rate_interval):
        data = {'connectionThrottle': {'maxConnections': int(max_connections),
                                       'minConnections': int(min_connections),
                                       'maxConnectionRate': int(max_connection_rate),
                                       'rateInterval': int(rate_interval)}}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionthrottle'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    def disable_connection_throttle(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'connectionthrottle'])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def health_monitor(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'healthmonitor'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, HealthMonitor, 'healthMonitor')

    def enable_health_monitor(self, type, delay, timeout,
                              attempts_before_deactivation):
        data = {'healthMonitor': {'type': type,
                                  'delay': int(delay),
                                  'timeout': int(timeout),
                                  'attemptsBeforeDeactivation': int(attempts_before_deactivation)}}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'healthmonitor'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response, HealthMonitor, 'healthMonitor')

    def disable_health_monitor(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'healthmonitor'])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def session_persistence(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'sessionpersistence'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, SessionPersistence,
                               'sessionPersistence')

    def enable_session_persistence(self, type):
        data = json.dumps({'sessionPersistence': {'persistenceType': type}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'sessionpersistence'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    def disable_session_persistence(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'sessionpersistence'])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def error_page(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'errorpage'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ErrorPage, 'errorpage')

    def set_error_page(self, content):
        data = json.dumps({'errorpage': {'content': content}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'errorpage'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response)

    def reset_error_page(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'errorpage'])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)

    @property
    def stats(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.id), 'stats'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, dict)

    def usage(self, start_time=None, end_time=None):
        url = [get_url('cloudloadbalancers'), 'loadbalancers',
               str(self.id), 'usage']
        if start_time is not None and end_time is not None:
            url = '/'.join(url)
            url = query(url, startTime=start_time, endTime=end_time)
        else:
            url.append('current')
            url = '/'.join(url)
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, UsageReport, 'loadBalancerUsage')


class Node(DotDict):
    def __repr__(self):
        return '<Node %s>' % self.address

    def reload(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.loadbalancer_id), 'nodes', str(self.id)])
        session = get_session()
        response = session.get(url)
        response = handle_response(response, Node, 'node',
                                   loadbalancer_id=self.loadbalancer_id)
        self = response
        return self

    def update(self, condition=None, type=None, weight=None):
        data = {'node': {}}
        if condition is not None and condition in ['ENABLED', 'DISABLED',
                'DRAINING']:
            data['node']['condition'] = condition
        if type is not None and type in ['PRIMARY', 'SECONDARY']:
            data['node']['type'] = type
        if weight is not None:
            data['node']['weight'] = int(weight)
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.loadbalancer_id), 'nodes', str(self.id)])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if response:
            if condition is not None and condition in ['ENABLED', 'DISABLED',
                    'DRAINING']:
                self.condition = condition
            if type is not None and type in ['PRIMARY', 'SECONDARY']:
                self.type = type
            if weight is None:
                self.weight = int(weight)
        return self

    def delete(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.loadbalancer_id), 'nodes', str(self.id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)


class Protocol(DotDict):
    def __repr__(self):
        return '<Protocol %s>' % self.name


class SessionPersistence(DotDict):
    def __repr__(self):
        return '<SessionPersistence %s>' % self.persistenceType


class UsageReport(DotDict):
    pass


class VirtualIP(DotDict):
    def __repr__(self):
        return '<VirtualIP %s>' % self.address

    def delete(self):
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self.loadbalancer_id), 'virtualips', str(self.id)])
        session = get_session()
        response = session.delete(url)
        return handle_response(response)


def list(limit=None, offset=None, marker=None, node=None, deleted=False):
    url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers'])
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    if deleted:
        url = query(url, status='DELETED')
    if node is not None:
        url = query(url, nodeaddress=node)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, LoadBalancer, 'loadBalancers')


def get(id):
    url = '/'.join([get_url('cloudloadbalancers'), 'flavors', str(id)])
    session = get_session()
    response = session.get(url)
    return handle_response(response, LoadBalancer, 'loadBalancer')


def create(name, protocol, port, virtual_ips, nodes, algorithm=None,
           access_list=None, connection_logging=None, connection_throttle=None,
           health_monitor=None, session_persistence=None, metadata=None):
    data = {'loadBalancer': {'name': name,
                             'protocol': protocol,
                             'port': int(port),
                             'virtualIps': [],
                             'nodes': [],
                             'metadata': metadata or {}}}
    for virtual_ip in virtual_ips:
        data['loadBalancer']['virtualIps'].append({'ipVersion': virtual_ip.version,
                                                   'type': virtual_ip.type})
    for node in nodes:
        data['loadBalancer']['nodes'].append({'address': node.address,
                                              'port': int(node.port),
                                              'condition': node.condition})
    if connection_logging is not None:
        data['loadBalancer']['connectionLogging'] = {
                'enabled': bool(connection_logging)
                }
    data = json.dumps(data)
    url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers'])
    session = get_session()
    response = session.post(url, data=data)
    return handle_response(response, LoadBalancer, 'loadBalancer')


def algorithms(limit=None, offset=None, marker=None):
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'algorithms']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Algorithm, 'algorithms')


def allowed_domains(limit=None, offset=None, marker=None):
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'alloweddomains']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, AllowedDomain, 'allowedDomains')


def protocols(limit=None, offset=None, marker=None):
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'protocols']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Protocol, 'protocols')
