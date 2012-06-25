import json

from vaporize.core import (get_session, get_url, handle_response, munge_url,
                           query)
from vaporize.utils import DotDict


class AccessRule(DotDict):
    """A CloudLoadBalancer Access List Rule."""
    def __repr__(self):
        if 'type' in self and 'address' in self:
            return '<AccessRule %s %s>' % (self['type'], self['address'])
        return super(AccessRule, self).__repr__()

    def delete(self):
        """Delete this Access Rule.

        .. warning::

            There is no confirmation step for this operation.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['loadbalancer_id']), 'accesslist',
                        str(self['id'])])
        session = get_session()
        response = session.delete(url)
        handle_response(response)


class Algorithm(DotDict):
    """A CloudLoadBalancer Algorithm."""
    def __repr__(self):
        if 'name' in self:
            return '<Algorithm %s>' % self['name']
        return super(Algorithm, self).__repr__()


class AllowedDomain(DotDict):
    """A CloudLoadBalancer Allowed Domains."""
    pass


class ContentCaching(DotDict):
    """A CloudLoadBalancer Content Caching."""
    pass


class ConnectionLogging(DotDict):
    """A CloudLoadBalancer Connection Logging."""
    pass


class ConnectionThrottle(DotDict):
    """A CloudLoadBalancer Connection Throttle."""
    pass


class ErrorPage(DotDict):
    """A CloudLoadBalancer Custom Error Page."""
    pass


class HealthMonitor(DotDict):
    """A CloudLoadBalancer Health Monitor."""
    pass


class LoadBalancer(DotDict):
    """A CloudLoadBalancer Load Balancer."""
    def __repr__(self):
        if 'name' in self:
            return '<LoadBalancer %s>' % self['name']
        return super(LoadBalancer, self).__repr__()

    def reload(self):
        """Reload this Load Balancer (an implicit :func:`get`).
        
        .. versionadded:: 0.1
        """
        assert 'id' in self
        response = get(self['id'])
        self.update(response)
        return self

    def modify(self, name=None, protocol=None, port=None, algorithm=None,
               connection_logging=False):
        """Modify this Load Balancer's properties.

        :param name: The Load Balancer's name.
        :type name: str
        :param protocol: A Load Balancer protocol, see: :func:`protocols`.
        :type protocol: str
        :param port: A Load Balancer port, see :func:`protocols`.
        :type port: int
        :param algorithm: A Load Balancer Algorithm, see :func:`algorithms`.
        :type algorithm: str
        :param connection_logging: Enable or disable Connection Logging.
        :type connection_logging: bool
        :returns: An updated Load Balancer.
        :rtype: :class:`LoadBalancer`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'loadBalancer': {}}
        if name is not None:
            data['loadBalancer']['name'] = name
        if algorithm is not None:
            data['loadBalancer']['algorithm'] = algorithm
        if protocol is not None:
            data['loadBalancer']['protocol'] = protocol
        if port is not None:
            data['loadBalancer']['port'] = int(port)
        if connection_logging is not None:
            connection_logging = bool(connection_logging)
            data['loadBalancer']['connectionLogging'] = connection_logging
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id'])])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if name is not None:
            self['name'] = name
        if algorithm is not None:
            self['algorithm'] = algorithm
        if protocol is not None:
            self['protocol'] = protocol
        if port is not None:
            self['port'] = int(port)
        if connection_logging is not None:
            self['connectionLogging']['enabled'] = bool(connection_logging)
        return self

    def delete(self):
        """Delete this Load Balancer.

        .. warning::

            There is not confirmation step for this operation. Deleting a Load
            Balancer is permanent.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id'])])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def nodes(self):
        """Returns a list of Nodes for this Load Balancer.

        :returns: A list of :class:`Node`.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'nodes'])
        session = get_session()
        response = session.get(munge_url(url))
        response = handle_response(response, Node, 'nodes',
                               loadbalancer_id=self['id'])
        self['nodes'] = response
        return self['nodes']

    def add_node(self, address, port, condition, type, weight):
        """Add a Node to this Load Balancer.
        
        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'nodes': [{'address': address,
                           'port': int(port),
                           'condition': condition,
                           'type': type,
                           'weight': int(weight)}]}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'nodes'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response, Node, 'nodes',
                               loadbalancer_id=self['id'])

    def remove_node(self, id):
        """Remove a Node from this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'nodes', str(id)])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def virtual_ips(self):
        """Returns a list of VirtualIPs for this Load Balancer.

        :returns: A list of Virtual IPs on this Load Balancer.
        :rtype: A list of :class:`VirtualIP`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'virtualips'])
        session = get_session()
        response = session.get(munge_url(url))
        response = handle_response(response, VirtualIP, 'virtualIps',
                                   loadbalancer_id=self['id'])
        self['virtual_ips'] = response
        return self['virtual_ips']

    def add_virtual_ip(self, type):
        """Add a Virtual IP to this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'virtualIp': {'ipVersion': 'IPV6', 'type': type}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'virtualips'])
        session = get_session()
        response = session.post(url, data=data)
        return handle_response(response, VirtualIP, 'virtualIp',
                               loadbalancer_id=self['id'])

    def remove_virtual_ip(self, id):
        """Remove a VirtualIP from this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'virtualips', str(id)])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def access_list(self):
        """Returns a list of AccessRules for this Load Balancer.

        :returns: A list of Access List Rules for this Load Balancer.
        :rtype: A list of :class:`AccessRule`.
        
        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'accesslist'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, AccessRule, 'accessList',
                               loadbalancer_id=self['id'])

    def add_access_rule(self, type, address):
        """Add AccessRule to this Load Balancer.

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'accesslist'])
        session = get_session()
        response = session.post(url)
        return handle_response(response, AccessRule, 'accessList')

    def remove_access_rule(self, id):
        """Remove an AccessRule from this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'accesslist', str(id)])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def connection_logging(self):
        """Returns the ConnectionLogging setting for this Load Balancer.

        :returns: This Load Balancer's Content Logging setting.
        :rtype: :class:`ConnectionLogging`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionlogging'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ConnectionLogging,
                               'connectionLogging')

    def enable_connection_logging(self):
        """Enable Connection Logging for this Load Balancer.

        :returns: A Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'connectionLogging': {'enabled': True}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionlogging'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def disable_connection_logging(self):
        """Disable Connection Logging for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'connectionLogging': {'enabled': False}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionlogging'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def content_caching(self):
        """Returns the Connection Caching setting for this Load Balancer.

        :returns: A Content Caching setting.
        :rtype: :class:`ContentCaching`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'contentcaching'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ContentCaching, 'contentCaching')

    def enable_content_caching(self):
        """Enable Content Caching for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'contentCaching': {'enabled': True}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'contentCaching'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def disable_content_caching(self):
        """Disable Content Caching for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'contentCaching': {'enabled': False}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'contentcaching'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def connection_throttle(self):
        """Return the Connection Throttle setting for this Load Balancer.

        :returns: A Connection Throttle setting.
        :rtype: :class:`ConnectionThrottle`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionthrottle'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ConnectionThrottle,
                               'connectionThrottle')

    def enable_connection_throttle(self, max_connections, min_connections,
                                   max_connection_rate, rate_interval):
        """Enable Connection Throttle setting for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'connectionThrottle': {
            'maxConnections': int(max_connections),
            'minConnections': int(min_connections),
            'maxConnectionRate': int(max_connection_rate),
            'rateInterval': int(rate_interval)
            }}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionthrottle'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def disable_connection_throttle(self):
        """Disable Connection Throttle for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionthrottle'])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def health_monitor(self):
        """Returns the Health Monitor setting for this Load Balancer.

        :returns: A Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'healthmonitor'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, HealthMonitor, 'healthMonitor')

    def enable_health_monitor(self, type, delay, timeout,
                              attempts_before_deactivation):
        """Enable Health Monitor for this Load Balancer.

        :returns: A Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'healthMonitor': {
            'type': type,
            'delay': int(delay),
            'timeout': int(timeout),
            'attemptsBeforeDeactivation': int(attempts_before_deactivation)
            }}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'healthmonitor'])
        session = get_session()
        response = session.put(url, data=data)
        return handle_response(response, HealthMonitor, 'healthMonitor')

    def disable_health_monitor(self):
        """Disable Health Monitor for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'healthmonitor'])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def session_persistence(self):
        """Return Session Persistence setting for this Load Balancer.

        :returns: A Session Persistence setting.
        :rtype: :class:`SessionPersistence`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'sessionpersistence'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, SessionPersistence,
                               'sessionPersistence')

    def enable_session_persistence(self, type):
        """Enable Session Persistence for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'sessionPersistence': {'persistenceType': type}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'sessionpersistence'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def disable_session_persistence(self):
        """Disable Session Persistance for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'sessionpersistence'])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def error_page(self):
        """Returns the Error Page for this Load Balancer.

        :returns: A Error Page setting.
        :rtype: :class:`ErrorPage`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'errorpage'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, ErrorPage, 'errorpage')

    def set_error_page(self, content):
        """Set a Custom Error Page for this Load Balancer.

        :param content: Contents of the custom error page.
        :type content: str

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'errorpage': {'content': content}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'errorpage'])
        session = get_session()
        response = session.put(url, data=data)
        handle_response(response)

    def reset_error_page(self):
        """Reset the Error Page for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'errorpage'])
        session = get_session()
        response = session.delete(url)
        handle_response(response)

    def stats(self):
        """Returns stats for this Load Balancer.

        :returns: Stats for this Load Balancer.
        :rtype: dict
        
        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'stats'])
        session = get_session()
        response = session.get(munge_url(url))
        return handle_response(response, dict)

    def usage(self, start_time=None, end_time=None):
        """Returns Usage Report for this Load Balancer.

        :param start_time: A datetime string as a starting point.
        :type start_time: str
        :param end_time: A datetime string as an ending point.
        :type end_time: str
        :returns: A usage report for this Load Balancer.
        :rtype: :class:`UsageReport`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudloadbalancers'), 'loadbalancers',
               str(self['id']), 'usage']
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
    """A CloudLoadBalancer Node."""
    def __repr__(self):
        if 'address' in self:
            return '<Node %s>' % self['address']
        return super(Node, self).__repr__()

    def reload(self):
        """Reload this Node.

        :returns: An pudated Node.
        :rtype: :class:`Node`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['loadbalancer_id']), 'nodes',
                        str(self['id'])])
        session = get_session()
        response = session.get(url)
        response = handle_response(response, Node, 'node',
                                   loadbalancer_id=self['loadbalancer_id'])
        self.update(response)
        return self

    def modify(self, condition=None, type=None, weight=None):
        """Modify a Node's properties.

        :param condition: A Node condition; ``ENABLED``, ``DISABLED`` or
            ``DRAINING``.
        :type condition: str
        :param type: A Node type.
        :type type: str
        :param weight: A Node weight.
        :type weight: int
        :returns: An updated Node.
        :rtype: :class:`Node`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
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
                        str(self['loadbalancer_id']), 'nodes',
                        str(self['id'])])
        session = get_session()
        response = session.put(url, data=data)
        response = handle_response(response)
        if response:
            if condition is not None and condition in ['ENABLED', 'DISABLED',
                    'DRAINING']:
                self['condition'] = condition
            if type is not None and type in ['PRIMARY', 'SECONDARY']:
                self['type'] = type
            if weight is None:
                self['weight'] = int(weight)
        return self

    def delete(self):
        """Delete this Node.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['loadbalancer_id']), 'nodes',
                        str(self['id'])])
        session = get_session()
        response = session.delete(url)
        handle_response(response)


class Protocol(DotDict):
    """A CloudLoadBalancer Protocol."""
    def __repr__(self):
        if 'name' in self:
            return '<Protocol %s>' % self['name']
        return super(Protocol, self).__repr__()


class SessionPersistence(DotDict):
    """A CloudLoadBalancer Session Persistence."""
    def __repr__(self):
        if 'persistenceType' in self:
            return '<SessionPersistence %s>' % self['persistenceType']
        return super(SessionPersistence, self).__repr__()


class UsageReport(DotDict):
    """A CloudLoadBalancer Usage Report."""
    pass


class VirtualIP(DotDict):
    """A CloudLoadBalancer Virtual IP."""
    def __repr__(self):
        if 'address' in self:
            return '<VirtualIP %s>' % self['address']
        return super(VirtualIP, self).__repr__()

    def delete(self):
        """Delete this Virtual IP.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['loadbalancer_id']), 'virtualips',
                        str(self['id'])])
        session = get_session()
        response = session.delete(url)
        handle_response(response)


def list(limit=None, offset=None, marker=None, node=None, deleted=False):
    """Returns a list of Load Balancers.

    :returns: A list of CloudLoadBalancer Load Balancers.
    :rtype: A list of :class:`LoadBalancer`.

    .. versionadded:: 0.1
    """
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
    """Return a Load Balancer by ID.

    :param id: A Load Balancer ID.
    :type id: int
    :returns: A CloudLoadBalancer Load Balancer with this ID.
    :rtype: :class:`LoadBalancer`

    .. versionadded:: 0.1
    """
    url = '/'.join([get_url('cloudloadbalancers'), 'flavors', str(id)])
    session = get_session()
    response = session.get(url)
    return handle_response(response, LoadBalancer, 'loadBalancer')


def create(name, protocol, port, virtual_ips, nodes, algorithm=None,
           access_list=None, connection_logging=None, connection_throttle=None,
           health_monitor=None, session_persistence=None, metadata=None):
    """Create a Load Balancer.

    :returns: A shiny new CloudLoadBalancer Load Balancer.
    :rtype: :class:`LoadBalancer`

    .. versionadded:: 0.1
    """
    data = {'loadBalancer': {'name': name,
                             'protocol': protocol,
                             'port': int(port),
                             'virtualIps': [],
                             'nodes': [],
                             'metadata': metadata or {}}}
    for virtual_ip in virtual_ips:
        data['loadBalancer']['virtualIps'].append({
            'ipVersion': virtual_ip.version,
            'type': virtual_ip.type
            })
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
    """Return a list of supported algorithms.

    :param limit: Limit the result set by a certain amount.
    :type limit: int
    :param offset: Offset the result set by a certain amount.
    :type offset: int
    :param marker: Start result set at a specific marker (ID).
    :type marker: int
    :returns: A list of supported CloudLoadBalancer algorithms.
    :rtype: A list of :class:`Algorithm`.

    .. versionadded:: 0.1
    """
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'algorithms']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Algorithm, 'algorithms')


def allowed_domains(limit=None, offset=None, marker=None):
    """Return a list of allowed domains.

    :param limit: Limit the result set by a certain amount.
    :type limit: int
    :param offset: Offset the result set by a certain amount.
    :type offset: int
    :param marker: Start result set at a specific marker (ID).
    :type marker: int
    :returns: A list of CloudLoadBalancer allowed domains.
    :rtype: A list of :class:`AllowedDomain`.

    .. versionadded:: 0.1
    """
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'alloweddomains']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, AllowedDomain, 'allowedDomains')


def protocols(limit=None, offset=None, marker=None):
    """Return a list of supported protocols.

    :param limit: Limit the result set by a certain amount.
    :type limit: int
    :param offset: Offset the result set by a certain amount.
    :type offset: int
    :param marker: Start result set at a specific marker (ID).
    :type marker: int
    :returns: A list of supported CloudLoadBalancer protocols.
    :rtype: A list of :class:`Protocol`.

    .. versionadded:: 0.1
    """
    url = [get_url('cloudloadbalancers'), 'loadbalancers', 'protocols']
    url = '/'.join(url)
    if limit is not None or offset is not None or marker is not None:
        url = query(url, limit=limit, offset=offset, marker=marker)
    session = get_session()
    response = session.get(munge_url(url))
    return handle_response(response, Protocol, 'protocols')
