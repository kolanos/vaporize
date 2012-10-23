# -*- coding: utf-8 -*-

import datetime
import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict


class AccessRule(DotDict):
    """A CloudLoadBalancer Access List Rule.

    The access list management feature allows fine-grained network access
    controls to be applied to the load balancer's virtual IP address. A single
    IP address, multiple IP addresses, or entire network subnets can be added
    as anetworkItem. Items that are configured with the ALLOW type will always
    take precedence over items with the DENY type. To reject traffic from all
    items except for those with the ALLOW type, add a networkItem with an
    address of "0.0.0.0/0" and a DENY type.
    """
    def __repr__(self):
        if 'type' in self and 'address' in self:
            return '<AccessRule %s %s>' % (self['type'], self['address'])
        return super(AccessRule, self).__repr__()

    @classmethod
    def create(cls, type, address):
        """Create an Access Rule.

        :param type: ``ACCEPT`` or ``DENY``
        :type type: str
        :param address: The IP address in which to apply the rule.
        :type address: str
        :returns: A shiny new Access Rule.
        :rtype: :class:`AccessRule`

        .. versionadded:: 0.1
        """
        return cls(type=type, address=address)

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
        handle_request('delete', url)


class Algorithm(DotDict):
    """A CloudLoadBalancer Algorithm.

    All load balancers utilize an algorithm that defines how traffic should be
    directed between back-end nodes. The default algorithm for newly created
    load balancers is RANDOM, which can be overridden at creation time or
    changed after the load balancer has been initially provisioned. The
    algorithm name is to be constant within a major revision of the load
    balancing API, though new algorithms may be created with a unique algorithm
    name within a given major revision of the service API.

    `Algorithm Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Algorithms-d1e4367.html>`_
    """
    def __repr__(self):
        if 'name' in self:
            return '<Algorithm %s>' % self['name']
        return super(Algorithm, self).__repr__()

    @classmethod
    def list(cls, limit=None, offset=None, marker=None):
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
        return handle_request('get', url, wrapper=cls,
                              container='algorithms')


class AllowedDomain(DotDict):
    """A CloudLoadBalancer Allowed Domains.

    The allowed domains are restrictions set for the allowed domain names used
    for adding load balancer nodes. In order to submit a domain name as an
    address for the load balancer node to add, the user must verify that the
    domain is valid by using the List Allowed Domains call. Once verified,
    simply supply the domain name in place of the node's address in the Add
    Nodes call.

    `Allowed Domains Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/AllowedDomains-d2f002e.html>`_
    """
    def __setitem__(self, key, value):
        if key == 'allowedDomain':
            key = 'name'
            value = value['name']
        super(AllowedDomain, self).__setitem__(key, value)

    @classmethod
    def list(cls, limit=None, offset=None, marker=None):
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
        url = [get_url('cloudloadbalancers'), 'loadbalancers',
               'alloweddomains']
        url = '/'.join(url)
        if limit is not None or offset is not None or marker is not None:
            url = query(url, limit=limit, offset=offset, marker=marker)
        return handle_request('get', url, wrapper=cls,
                              container='allowedDomains')


class ContentCaching(DotDict):
    """A CloudLoadBalancer Content Caching.

    `Content Caching Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/ContentCaching-d1e3358.html>`_
    """
    pass


class ConnectionLogging(DotDict):
    """A CloudLoadBalancer Connection Logging.

    `Connection Logging Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Log_Connections-d1e3924.html>`_
    """
    pass


class ConnectionThrottle(DotDict):
    """A CloudLoadBalancer Connection Throttle.

    The connection throttling feature imposes limits on the number of
    connections per IP address to help mitigate malicious or abusive traffic to
    your applications. The attributes in the table that follows can be
    configured based on the traffic patterns for your sites.

    `Connection Throttle Refference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Throttle_Connections-d1e4057.html>`_
    """
    @classmethod
    def create(cls, max_connections, min_connections, max_connection_rate,
               rate_interval):
        """Create a Connection Throttle setting.

        :param max_connections: Maximum number of connections to allow for a
            single IP address. Setting a value of 0 will allow unlimited
            simultaneous connections; otherwise set a value between 1 and
            100000.
        :type max_connections: int
        :param min_connections: Allow this number of connections per IP
            address before applying throttling restrictions. Setting a value of
            0 allows unlimited simultaneous connections; otherwise, set a value
            between 1 and 1000.
        :type min_connections: int
        :param max_connection_rate: Maximum number of connections allowed from
            a single IP address in the defined rateInterval. Setting a value of
            0 allows an unlimited connection rate; otherwise, set a value
            between 1 and 100000.
        :type max_connection_rate: int
        :param rate_interval: Frequency (in seconds) at which the
            maxConnectionRate is assessed. For example, a maxConnectionRate of
            30 with a rateInterval of 60 would allow a maximum of 30
            connections per minute for a single IP address. This value must be
            between 1 and 3600.
        :type rate_interval: int

        :returns: A Load Balancer Connection Throttle setting.
        :rtype: :class:`ConnectionThrottle`

        .. versionadded:: 0.1.7
        """
        return cls(max_connections=int(max_connections),
                   min_connections=int(min_connections),
                   max_connection_rate=int(max_connection_rate),
                   rate_interval=int(rate_interval))


class ErrorPage(DotDict):
    """A CloudLoadBalancer Custom Error Page."""
    pass


class HealthMonitor(DotDict):
    """A CloudLoadBalancer Health Monitor.

    The load balancing service includes a health monitoring operation which
    periodically checks your back-end nodes to ensure they are responding
    correctly. If a node is not responding, it is removed from rotation until
    the health monitor determines that the node is functional. In addition to
    being performed periodically, the health check also is performed against
    every node that is added to ensure that the node is operating properly
    before allowing it to service traffic. Only one health monitor is allowed
    to be enabled on a load balancer at a time.

    Every health monitor has a ``type`` attribute to signify what kind of
    monitor it is.

    * ``CONNECT``: Health monitor is a connect monitor.
    * ``HTTP``: Health monitor is an HTTP monitor.
    * ``HTTPS``: Health monitor is an HTTPS monitor.

    `Health Monitor Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Monitors-d1e3370.html>`_
    """
    @classmethod
    def create(cls, type, delay, timeout, attempts_before_deactivation,
               body_regex=None, path=None, status_regex=None):
        """Create a Health Monitor setting.

        :param type: Type of health monitor to create (``CONNECT``, ``HTTP`` or
            ``HTTPS``).
        :type type: str
        :param delay: The minimum number of seconds to wait before executing
            the health monitor. Must be a number between 1 and 3600.
        :type delay: int
        :param timeout: Maximum number of seconds to wait for a connection to
            be established before timing out. Must be a number between 1 and
            300.
        :type timeout: int
        :param attempts_before_deactivation: Number of permissible monitor
            failures before removing a node from rotation. Must be a number
            between 1 and 10.
        :type attempts_before_deactivation: int
        :param body_regex: A regular expression that will be used to evaluate
            the contents of the body of the response (required for ``HTTP`` and
            ``HTTPS``).
        :type body_regex: str
        :param path: The HTTP path that will be used in the sample request
            (required for ``HTTP`` and ``HTTPS``).
        :type path: str
        :param status_regex: A regular expression that will be used to evaluate
            the HTTP status code returned in the response (required for ``HTTP``
            and ``HTTPS``).
        :type status_regex: str

        :returns: A Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        .. versionadded:: 0.1.7
        """
        if type in ['HTTP', 'HTTPS']:
            assert body_regex is not None
            assert path is not None
            assert status_regex is not None
        return cls(type=type, delay=int(delay), timeout=int(timeout),
                   attempts_before_deactivation=int(attempts_before_deactivation),
                   body_regex=body_regex, path=path, status_regex=status_regex)


class LoadBalancer(DotDict):
    """A CloudLoadBalancer Load Balancer."""
    def __repr__(self):
        if 'name' in self:
            return '<LoadBalancer %s>' % self['name']
        return super(LoadBalancer, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'accessList':
            value = [AccessRule(v) for v in value]
        elif key == 'connectionLogging':
            value = ConnectionLogging(value)
        elif key == 'connectionThrottle':
            value = ConnectionThrottle(value)
        elif key == 'contentCaching':
            value = ContentCaching(value)
        elif key == 'errorpage':
            value = ErrorPage(value)
        elif key == 'healthMonitor':
            value = HealthMonitor(value)
        elif key == 'nodes':
            value = [Node(v) for v in value]
        elif key == 'sessionPersistence':
            value = SessionPersistence(value)
        elif key == 'virtualIps':
            value = [VirtualIP(v) for v in value]
        elif key in ['created', 'updated']:
            if not isinstance(value, datetime.datetime) and 'time' in value:
                    value = convert_datetime(value['time'])
        super(LoadBalancer, self).__setitem__(key, value)

    def reload(self):
        """Reload this Load Balancer (an implicit :func:`get`).

        .. versionadded:: 0.1
        """
        assert 'id' in self
        response = LoadBalancer.get(self['id'])
        self.update(response)
        return self

    def modify(self, name=None, protocol=None, port=None, algorithm=None,
               connection_logging=None):
        """Modify this Load Balancer's properties.

        This operation asynchronously updates the attributes of the specified
        load balancer. Upon successful validation of the request, the service
        will return a 202 (Accepted) response code. A caller can poll the load
        balancer with its ID to wait for the changes to be applied and the load
        balancer to return to an ACTIVE status.

        :param name: The Load Balancer's name.
        :type name: str
        :param protocol: A Load Balancer protocol, see: :func:`protocols`.
        :type protocol: str or :class:`Protocol`
        :param port: A Load Balancer port, see :func:`protocols`.
        :type port: int
        :param algorithm: A Load Balancer Algorithm, see :func:`algorithms`.
        :type algorithm: str or :class:`Algorithm`
        :param connection_logging: Enable or disable Connection Logging.
        :type connection_logging: bool
        :returns: An updated Load Balancer.
        :rtype: :class:`LoadBalancer`

        .. note::

            If you pass a :class:`Protocol` to the ``protocol`` argument, it
            will set ``port`` to the default for that protocol if ``port`` is
            unset.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(algorithm, Algorithm):
            algorithm = algorithm.name
        if isinstance(protocol, Protocol):
            if port is None:
                port = protocol.port
            protocol = protocol.name
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
        handle_request('put', url, data)
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

        The remove load balancer function removes the specified load balancer
        and its associated configuration from the account. Any and all
        configuration data is immediately purged and is not recoverable.

        .. warning::

            There is not confirmation step for this operation. Deleting a Load
            Balancer is permanent.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id'])])
        handle_request('delete', url)

    @property
    def nodes(self):
        """Returns a list of Nodes for this Load Balancer.

        :returns: A list of Nodes.
        :rtype: list of :class:`Node`

        .. versionadded:: 0.1
        """
        if 'nodes' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'nodes'])
            self['nodes'] = handle_request('get', url, wrapper=Node,
                                           container='nodes',
                                           loadbalancer_id=self['id'])
        return self['nodes']

    def add_nodes(self, *nodes):
        """Add Nodes to this Load Balancer.

            >>> loadbalancer = vaporize.loadbalancers.create(...)
            >>> node1 = vaporize.loadbalancers.Node.create(....)
            >>> node2 = vaporize.loadbalancers.Node.crete(....)
            >>> loadbalancer.add_nodes(node1, node2)

        :param nodes: Nodes to add to the Load Balancer.
        :type nodes: :class:`Node`
        :returns: A list of Nodes.
        :rtype: list of :class:`Node`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'nodes': []}
        for node in nodes:
            if isinstance(node, Node):
                data['nodes'].append({
                    'address': node.address,
                    'port': node.port,
                    'condition': node.condition,
                    'type': node.type,
                    'weight': node.weight
                    })
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'nodes'])
        self['nodes'] = handle_request('post', url, data, Node, 'nodes',
                                       loadbalancer_id=self['id'])
        return self['nodes']

    def remove_node(self, node):
        """Remove a Node from this Load Balancer.

        :param node: ``id`` or :class:`Node` to remove from Load Balancer
        :type node: int or :class:`Node`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        node = node.id if isinstance(node, Node) else int(node)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'nodes', str(node)])
        handle_request('delete', url)

    @property
    def virtual_ips(self):
        """Returns a list of VirtualIPs for this Load Balancer.

        :returns: A list of Virtual IPs on this Load Balancer.
        :rtype: list of :class:`VirtualIP`

        .. versionadded:: 0.1
        """
        if 'virtual_ips' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'virtualips'])
            response = handle_request('get', url, wrapper=VirtualIP,
                                      container='virtualIps',
                                      loadbalancer_id=self['id'])
            self['virtual_ips'] = response
        return self['virtual_ips']

    def add_virtual_ips(self, *virtual_ips):
        """Add Virtual IPs to this Load Balancer.

            >>> loadbalancer = vaporize.loadbalancers.create(...)
            >>> virtual_ip1 = vaporize.loadbalancers.VirtualIP.create(...)
            >>> virtual_ip2 = vaporize.loadbalancers.VirtualIP.create(...)
            >>> loadbalancer.add_virtual_ips(virtual_ip1, virtual_ip2)

        :param virtual_ips: Virtual IPs to add to thisLoad Balancer
        :type virtual_ips: :class:`VirtualIP`
        :returns: A list of Virtual IPs on the Load Balancer
        :rtype: list of :class:`VirtualIP`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'virtualIps': []}
        for virtual_ip in virtual_ips:
            if isinstance(virtual_ip, VirtualIP):
                data['virtualIps'].append({
                    'ipVersion': virtual_ip.version,
                    'type': virtual_ip.type
                    })
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'virtualips'])
        self['virtual_ips'] = handle_request('post', url, data, VirtualIP,
                                             'virtualIps',
                                             loadbalancer_id=self['id'])
        return self['virtual_ips']

    def remove_virtual_ip(self, virtual_ip):
        """Remove a VirtualIP from this Load Balancer.

        :param virtual_ip: ``id`` or Virtual IP to remove from Load Balancer
        :type virtual_ip: int or :class:`VirtualIP`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(virtual_ip, VirtualIP):
            virtual_ip = virtual_ip.id
        virtual_ip = int(virtual_ip)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'virtualips', str(virtual_ip)])
        handle_request('delete', url)

    @property
    def access_list(self):
        """Returns a list of AccessRules for this Load Balancer.

        :returns: A list of Access List Rules for this Load Balancer.
        :rtype: list of :class:`AccessRule`.

        .. versionadded:: 0.1
        """
        if 'access_list' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'accesslist'])
            self['access_list'] = handle_request('get', url, wrapper=AccessRule,
                                                 container='accessList',
                                                 loadbalancer_id=self['id'])
        return self['access_list']

    def add_access_rules(self, *access_rules):
        """Add AccessRules to this Load Balancer.

            >>> loadbalancer = vaporize.loadbalancers.create(...)
            >>> access_rule1 = vaporize.loadbalancers.AccessRule.create(...)
            >>> access_rule2 = vaporize.loadbalancers.AccessRule.create(....)
            >>> loadbalancer.add_access_rules(access_rule1, access_rule2)

        :param access_rules: Access Rules to add to this Load Balancer.
        :type access_rules: :class:`AccessRule`
        :returns: A list of Access Rules.
        :rtype: list of :class:`AccessRule`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'accessList': []}
        for access_rule in access_rules:
            if isinstance(access_rule, AccessRule):
                data['accessList'].append({
                    'type': access_rule.type,
                    'address': access_rule.address
                    })
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'accesslist'])
        self['access_list'] = handle_request('post', url, data, AccessRule,
                                             'accessList',
                                             loadbalancer_id=self['id'])
        return self['access_list']

    def remove_access_rule(self, access_rule):
        """Remove an AccessRule from this Load Balancer.

        :param access_rule: ``id`` or Access Rule to remove from Load Balancer
        :type access_rule: int or :class:`AccessRule`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if isinstance(access_rule, AccessRule):
            access_rule = access_rule.id
        access_rule = int(access_rule)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'accesslist', str(access_rule)])
        handle_request('delete', url)

    @property
    def connection_logging(self):
        """Returns the ConnectionLogging setting for this Load Balancer.

        This operation allows the user to view the current connection logging
        configuration, enable connection logging, or disable connection
        logging.

        :returns: This Load Balancer's Content Logging setting.
        :rtype: :class:`ConnectionLogging`

        `Connection Log Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Log_Connections-d1e3924.html>`_

        .. versionadded:: 0.1
        """
        if 'connection_logging' not in self:
            assert 'id' in self
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'connectionlogging'])
            response = handle_request('get', url, wrapper=ConnectionLogging,
                                      container='connectionLogging')
            self['connection_logging'] = response
        return self['connection_logging']

    @connection_logging.setter
    def connection_logging(self, enabled):
        """Enable/disable Connection Logging for this Load Balancer.

        To enable::

            >>> lb = vaporie.loadbalancers.get(12345)
            >>> lb.connection_logging = True

        To disable::

            >>> lb = vaporize.loadbalancers.get(12345)
            >>> lb.connection_logging = False

        :returns: This Load Balancer's Connection Logging setting.
        :rtype: :class:`ConnectionLogging`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'connectionLogging': {'enabled': bool(enabled)}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionlogging'])
        handle_request('put', url, data)
        self['connection_logging']['enabled'] = True

    @property
    def content_caching(self):
        """Returns the Connection Caching setting for this Load Balancer.

        :returns: This Load Balancer's Content Caching setting.
        :rtype: :class:`ContentCaching`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if 'content_caching' not in self:
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'contentcaching'])
            response = handle_request('get', url, wrapper=ContentCaching,
                                      container='contentCaching')
            self['content_caching'] = response
        return self['content_caching']

    @content_caching.setter
    def content_caching(self, enabled):
        """Enable/disable Content Caching for this Load Balancer.

        This operation allows the user to view the current content caching
        configuration, enable content caching, or disable content caching.

        When content caching is enabled, recently-accessed files are stored on
        the load balancer for easy retrieval by web clients. Content caching
        improves the performance of a web site by temporarily storing data that
        was recently accessed. While it's cached, requests for that data will
        be served by the load balancer instead of making another query to a web
        server behind it. The result is improved response times for those
        requests and less load on the web server.

        To enable::

            >>> lb = vaporize.loadbalancers.get(12345)
            >>> lb.content_caching = True

        To disable::

            >>> lb = vaporize.loadbalancers.get(12345)
            >>> lb.content_caching = False

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'contentCaching': {'enabled': bool(enabled)}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'contentCaching'])
        handle_request('put', url, data)
        self['content_caching']['enabled'] = bool(enabled)

    @property
    def connection_throttle(self):
        """Return the Connection Throttle setting for this Load Balancer.

        :returns: This Load Balancer's Connection Throttle setting.
        :rtype: :class:`ConnectionThrottle`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if 'connection_throttle' not in self:
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'connectionthrottle'])
            response = handle_request('get', url, wrapper=ConnectionThrottle,
                                      container='connectionThrottle')
            self['connection_throttle'] = response
        return self['connection_throttle']

    @connection_throttle.setter
    def connection_throttle(self, connection_throttle):
        """Enable Connection Throttle setting for this Load Balancer.

        :param connection_throttle: A Connection Throttle instance.
        :type connection_throttle: :class:`ConnectionThrottle`
        :returns: This Load Balancer's Connection Throttle setting.
        :rtype: :class:`ConnectionThrottle`

        To enable::

            >>> ct = vaporize.loadbalancers.ConnectionThrottle.create(...)
            >>> lb = vaporize.loadbalancers.get(12345)
            >>> lb.connection_throttle = ct

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert isinstance(connection_throttle, ConnectionThrottle)
        data = {'connectionThrottle': {
            'maxConnections': connection_throttle.max_connections,
            'minConnections': connection_throttle.min_connections,
            'maxConnectionRate': connection_throttle.max_connection_rate,
            'rateInterval': connection_throttle.rate_interval
            }}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionthrottle'])
        handle_request('put', url, data)
        self['connection_throttle'] = connection_throttle
        return self['connection_throttle']

    @connection_throttle.deleter
    def connection_throttle(self):
        """Disable Connection Throttle for this Load Balancer.

        To disable::

            >>> lb = vaporize.loadbalancers.get(12345)
            >>> del lb.connection_throttle

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'connectionthrottle'])
        handle_request('delete', url)
        del self['connection_throttle']

    @property
    def health_monitor(self):
        """Returns the Health Monitor setting for this Load Balancer.

        :returns: This Load Balancer's Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if 'health_monitor' not in self:
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'healthmonitor'])
            response = handle_request('get', url, wrapper=HealthMonitor,
                                      container='healthMonitor')
            self['health_monitor'] = response
        return self['health_monitor']

    @health_monitor.setter
    def health_monitor(self, health_monitor):
        """Enable Health Monitor for this Load Balancer.

        :returns: A Health Monitor setting.
        :rtype: :class:`HealthMonitor`

        To enable::

            >>> hm = vaporize.loadbalancers.HealthMonitor.create(...)
            >>> lb = vaporize.loadbalancers.get(12345)
            >>> lb.health_monitor = hm

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert isinstance(health_monitor, HealthMonitor)
        data = {'healthMonitor': {
            'type': health_monitor.type,
            'delay': health_monitor.delay,
            'timeout': health_monitor.timeout,
            'attemptsBeforeDeactivation': health_monitor.attempts_before_deactivation
            }}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'healthmonitor'])
        response = handle_request('put', url, data, HealthMonitor,
                                  'healthMonitor')
        self['health_monitor'] = response

    @health_monitor.deleter
    def health_monitor(self):
        """Disable Health Monitor for this Load Balancer.

        To disable::

            >>> lb = vaporize.loadbalancers.get(12345)
            >>> del lb.health_monitor

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'healthmonitor'])
        handle_request('delete', url)
        del self['health_monitor']

    @property
    def session_persistence(self):
        """Return Session Persistence setting for this Load Balancer.

        :returns: This Load Balancer's Session Persistence setting.
        :rtype: :class:`SessionPersistence`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if 'session_persistence' not in self:
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'sessionpersistence'])
            response = handle_request('get', url, wrapper=SessionPersistence,
                                      container='sessionPersistence')
            self['session_persistence'] = response
        return self['session_persistence']

    @session_persistence.setter
    def session_persistence(self, persistence_type):
        """Enable Session Persistence for this Load Balancer.

        :param persistence_type: Session persistence type (``HTTP_COOKIE`` or
            ``SOURCE_IP``).
        :type persistence_type: str

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert persistence_type in ['HTTP_COOKIE', 'SOURCE_IP']
        data = json.dumps({'sessionPersistence': {
            'persistenceType': persistence_type
            }})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'sessionpersistence'])
        handle_request('put', url, data)
        self['session_persistence'] = SessionPersistence(
                persistence_type=persistence_type
                )

    @session_persistence.deleter
    def session_persistence(self):
        """Disable Session Persistance for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'sessionpersistence'])
        handle_request('delete', url)
        del self['session_persistence']

    @property
    def error_page(self):
        """Returns the Error Page for this Load Balancer.

        An error page is the html file that is shown to an end user who is
        attempting to access a load balancer node that is offline/unavailable.

        :returns: This Load Balancer's Error Page setting.
        :rtype: :class:`ErrorPage`

        `Error Page Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Erropage-d1e666.html>`_

        .. versionadded:: 0.1
        """
        assert 'id' in self
        if 'error_page' not in self:
            url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                            str(self['id']), 'errorpage'])
            response = handle_request('get', url, wrapper=ErrorPage,
                                      container='errorpage')
            self['error_page'] = response
        return self['error_page']

    @error_page.setter
    def error_page(self, content):
        """Set a Custom Error Page for this Load Balancer.

        A single custom error page may be added per account load balancer with
        an HTTP protocol. Page updates will override existing content. If a
        custom error page is deleted, or the load balancer is changed to a
        non-HTTP protocol, the default error page will be restored.

        :param content: Specifies the HTML content for the custom error page.
            Must be 65536 characters or less.
        :type content: str

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'errorpage': {'content': content}})
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'errorpage'])
        handle_request('put', url, data)
        self['error_page'] = ErrorPage(content=content)

    @error_page.deleter
    def error_page(self):
        """Reset the Error Page for this Load Balancer.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'errorpage'])
        handle_request('delete', url)
        del self['error_page']

    @property
    def stats(self):
        """Returns stats for this Load Balancer.

        This operation provides detailed stats output, including the following
        information, for a specific load balancer configured and associated with
        the user's account:

        * ``connect_timeOut``: Connections closed by this load balancer because
            the 'connect_timeout' interval was exceeded.
        * ``connectError``: Number of transaction or protocol errors in this
            load balancer.
        * ``connect_failure``: Number of connection failures in this load
            balancer.
        * ``data_timed_out``: Connections closed by this load balancer because
            the 'timeout' interval was exceeded.
        * ``keep_alive_timed_out``: Connections closed by this load balancer
            because the 'keepalive_timeout' interval was exceeded.
        * ``max_conn``: Maximum number of simultaneous TCP connections this load
            balancer has processed at any one time.

        :returns: Stats for this Load Balancer.
        :rtype: :class:`Stat`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['id']), 'stats'])
        return handle_request('get', url, wrapper=Stat)

    def usage(self, start_time=None, end_time=None):
        """Returns Usage Report for this Load Balancer.

        :param start_time: A datetime string as a starting point.
        :type start_time: str or datetime
        :param end_time: A datetime string as an ending point.
        :type end_time: str or datetime
        :returns: A usage report for this Load Balancer.
        :rtype: :class:`UsageReport`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudloadbalancers'), 'loadbalancers',
               str(self['id']), 'usage']
        if start_time is not None and end_time is not None:
            url = '/'.join(url)
            url = query(url, startTime=str(start_time), endTime=str(end_time))
        else:
            url.append('current')
            url = '/'.join(url)
        return handle_request('get', url, wrapper=UsageReport,
                              container='loadBalancerUsage')

    @classmethod
    def list(cls, limit=None, offset=None, marker=None, node=None,
             deleted=False):
        """Returns a list of Load Balancers.

        This operation provides a list of all load balancers configured and
        associated with your account.

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
        return handle_request('get', url, wrapper=cls,
                              container='loadBalancers')

    @classmethod
    def get(cls, id):
        """Return a Load Balancer by ID.

        :param id: A Load Balancer ID.
        :type id: int
        :returns: A CloudLoadBalancer Load Balancer with this ID.
        :rtype: :class:`LoadBalancer`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers', str(id)])
        return handle_request('get', url, wrapper=cls,
                              container='loadBalancer')

    @classmethod
    def create(cls, name, protocol, virtual_ips, nodes, port=None, algorithm=None,
               access_list=None, connection_logging=None, connection_throttle=None,
               health_monitor=None, session_persistence=None, metadata=None):
        """Create a Load Balancer.

        This operation asynchronously provisions a new load balancer based on the
        configuration defined in the request object. Once the request is validated
        and progress has started on the provisioning process, a response object will
        be returned. The object will contain a unique identifier and status of the
        request. Using the identifier, the caller can check on the progress of the
        operation by performing a GET on loadbalancers/id. If the corresponding
        request cannot be fulfilled due to insufficient or invalid data, an HTTP 400
        (Bad Request) error response will be returned with information regarding the
        nature of the failure in the body of the response. Failures in the
        validation process are non-recoverable and require the caller to correct the
        cause of the failure and POST the request again.

        An HTTP load balancer will have the X-Forwarded-For (XFF) HTTP header set by
        default. This header will contain the actual originating IP address of a
        client connecting to a web server through an HTTP proxy or load balancer,
        which many web applications are already designed to use when determining the
        source address for a request. (This header is also included on the Modify
        Load Balancer request if the protocol changes to reenable it.)

        An HTTP load balancer will also include the X-Forwarded-Proto (XFP) HTTP
        header, which has been added for identifying the originating protocol of an
        HTTP request as "http" or "https" depending on what protocol the client
        requested. This is specially useful when using SSL termination.

        :param name: Name of the Load Balancer to create.
        :type name: str
        :param protocol: The Load Balancer's protocol (see: :class:`Protocol`).
        :type protocol: str or :class:`Protocol`
        :param virtual_ips: A list of Virtual IPs (see: :class:`VirtualIP`).
        :type virtual_ips: list of :class:`VirtualIP`
        :param nodes: A list of Nodes to add to add (see: :class:`Node`).
        :type nodes: list of :class:`Node`
        :param port: The port the Load Balancer should listen on.
        :type port: int
        :param algorithm: The Load Balancer's Algorithm (see: :class:`Algorithm`).
        :type algorithm: :class:`Algorithm`
        :param access_list: A list of Access Rules (see: :class:`AccessRule`).
        :type access_list: list of :class:`AccessRule`
        :param access_list: A list of Access Rules (see: :class:`AccessRule`).
        :type access_list: list of :class:`AccessRule`
        :param connection_logging: Enable or disable connection logging.
        :type connection_logging: bool
        :param connection_throttle: Connection Throttling settings (see:
            :class:`ConnectionThrottle`).
        :type connection_throttle: :class:`ConnectionThrottle`
        :param health_monitor: Health Monitor settings (see:
            :class:`HealthMonitor`).
        :type health_monitor: :class:`HealthMonitor`
        :param session_persistence: Session persistence type (``HTTP_COOKIE`` or
            ``SOURCE_IP``).
        :type session_persistence: str
        :param metadata: Meta data to store with the Load Balancer record.
        :type metadata: dict

        :returns: A shiny new CloudLoadBalancer Load Balancer.
        :rtype: :class:`LoadBalancer`

        .. note::

            If you pass a :class:`Protocol` to the ``protocol`` argument, it
            will set ``port`` to the default for that protocol if ``port`` is
            unset.

        .. versionadded:: 0.1
        """
        if isinstance(algorithm, Algorithm):
            algorithm = algorithm.name
        if isinstance(protocol, Protocol):
            if port is None:
                port = protocol.port
            protocol = protocol.name
        assert port is not None
        data = {'loadBalancer': {'name': name,
                                 'protocol': protocol,
                                 'port': port,
                                 'virtualIps': [],
                                 'nodes': []}}
        for virtual_ip in virtual_ips:
            if isinstance(virtual_ip, VirtualIP):
                data['loadBalancer']['virtualIps'].append(virtual_ip.to_dict())
        for node in nodes:
            if isinstance(node, Node):
                data['loadBalancer']['nodes'].append(node.to_dict())
        if algorithm is not None:
            data['loadBalancer']['algorithm'] = algorithm
        if connection_logging is not None:
            data['loadBalancer']['connectionLogging'] = {
                    'enabled': bool(connection_logging)
                    }
        if access_list is not None:
            data['loadBalancer']['accessList'] = []
            for access_rule in access_list:
                if isinstance(access_rule, AccessRule):
                    data['loadBalancer']['accessList'].append({
                        'type': access_rule.type,
                        'address': access_rule.address
                        })
        if connection_throttle is not None \
                and isintance(connection_throtle, ConnectionThrottle):
            data['loadBalancer']['connectionThrottle'] = {
                    'maxConnections': connection_throttle.max_connections,
                    'minConnections': connection_throttle.min_connections,
                    'maxConnectionRate': connection_throttle.max_connection_rate,
                    'rateInterval': connection_throttle.rate_interval
                    }
        if health_monitor is not None and isinstance(health_monitor, HealthMonitor):
            data['loadBalancer']['healthMonitor'] = {
                    'type': health_monitor.type,
                    'delay': health_monitor.delay,
                    'timeout': health_monitor.timeout,
                    'attemptsBeforeDeactivation': health_monitor.attempts_before_deactivation,
                    'bodyRegex': health_monitor.body_regex,
                    'path': health_monitor.path,
                    'statusRegex': health_monitor.status_regex
                    }
        if session_persistence is not None:
            data['loadBalancer']['sessionPersistence'] = {
                    'persistenceType': session_persistence
                    }
        data = json.dumps(data)
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers'])
        return handle_request('post', url, data, wrapper=cls,
                              container='loadBalancer')


class Node(DotDict):
    """A CloudLoadBalancer Node.

    The nodes defined by the load balancer are responsible for servicing the
    requests received through the load balancer's virtual IP. By default, the
    load balancer employs a basic health check that ensures the node is
    listening on its defined port. The node is checked at the time of addition
    and at regular intervals as defined by the load balancer health check
    configuration. If a back-end node is not listening on its port or does not
    meet the conditions of the defined active health check for the load
    balancer, then the load balancer will not forward connections and its status
    will be listed as OFFLINE. Only nodes that are in an ONLINE status will
    receive and be able to service traffic from the load balancer.

    All nodes have an associated status that indicates whether the node is
    ONLINE, OFFLINE, or DRAINING. Only nodes that are in ONLINE status will
    receive and be able to service traffic from the load balancer. The OFFLINE
    status represents a node that cannot accept or service traffic. A node in
    DRAINING status represents a node that stops the traffic manager from
    sending any additional new connections to the node, but honors established
    sessions. If the traffic manager receives a request and session persistence
    requires that the node is used, the traffic manager will use it. The status
    is determined by the passive or active health monitors.

    If the WEIGHTED_ROUND_ROBIN load balancer algorithm mode is selected, then
    the caller should assign the relevant weights to the node as part of the
    weight attribute of the node element. When the algorithm of the load
    balancer is changed to WEIGHTED_ROUND_ROBIN and the nodes do not already
    have an assigned weight, the service will automatically set the weight to
    "1" for all nodes.

    One or more secondary nodes can be added to a specified load balancer so
    that if all the primary nodes fail, traffic can be redirected to secondary
    nodes. The type attribute allows configuring the node as either PRIMARY or
    SECONDARY.

    `Node Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Nodes-d1e2173.html>`_
    """
    def __repr__(self):
        if 'address' in self:
            return '<Node %s>' % self['address']
        return super(Node, self).__repr__()

    @classmethod
    def create(cls, address, port, condition, type, weight):
        """Create a Load Balancer Node.

        When a node is added, it is assigned a unique identifier that can be
        used for management operations such as changing the condition or
        removing it. Every load balancer is dual-homed on both the public
        Internet and ServiceNet. As a result, nodes can either be internal
        ServiceNet addresses or addresses on the public Internet.

        One or more secondary nodes can be added to a specified load balancer so
        that if all the primary nodes fail, traffic can be redirected to
        secondary nodes. The type attribute allows configuring the node as
        either PRIMARY or SECONDARY.

        Domain names are also accepted with certain restrictions.

        :param address: IP address or domain name for the node. Refer to the
            request examples in this section for the required xml/json format.
        :type address: str
        :param port: Port number for the service you are load balancing.
        :type port: int
        :param condition: Condition for the node, which determines its role
            within the load balancer.
        :type condition: str
        :param type: Type of node to add (``PRIMARY`` or ``SECONDARY``).
        :type type: str
        :param weight: Weight of node to add. If the WEIGHTED_ROUND_ROBIN load
            balancer algorithm mode is selected, then the user should assign the
            relevant weight to the node using the weight attribute for the node.
            Must be an integer from 1 to 100.
        :type weight: int

        :returns: A shiny new Node.
        :rtype: :class:`Node`

        Node types:

        * ``PRIMARY``: Nodes defined as PRIMARY are in the normal rotation to receive traffic from the load balancer.
        * ``SECONDARY``: Nodes defined as SECONDARY are only in the rotation to receive traffic from the load balancer when all the primary nodes fail.

        .. versionadded:: 0.1
        """
        return cls(address=address, port=int(port), condition=condition,
                   type=type, weight=int(weight))

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
        response = handle_request('get', url, wrapper=Node, container='node',
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
        handle_request('put', url, data)
        if condition is not None and condition in ['ENABLED', 'DISABLED',
                                                   'DRAINING']:
            self['condition'] = condition
        if type is not None and type in ['PRIMARY', 'SECONDARY']:
            self['type'] = type
        if weight is None:
            self['weight'] = weight
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
        handle_request('delete', url)

    def to_dict(self):
        """Create a Rackspace formatted dict."""
        return dict([(k, self[k]) for k in ['address', 'condition', 'port',
                                            'type', 'weight'] if k in self])


class Protocol(DotDict):
    """A CloudLoadBalancer Protocol.

    All load balancers must define the protocol of the service which is being
    load balanced. The protocol selection should be based on the protocol of the
    back-end nodes. When configuring a load balancer, the default port for the
    given protocol will be selected unless otherwise specified.

    `Protocol Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Protocols-d1e4264.html>`_
    """
    def __repr__(self):
        if 'name' in self:
            return '<Protocol %s>' % self['name']
        return super(Protocol, self).__repr__()

    @classmethod
    def list(cls, limit=None, offset=None, marker=None):
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
        return handle_request('get', url, wrapper=cls, container='protocols')


class SessionPersistence(DotDict):
    """A CloudLoadBalancer Session Persistence.

    Session persistence is a feature of the load balancing service that forces
    multiple requests from clients to be directed to the same node. This is
    common with many web applications that do not inherently share application
    state between back-end servers. Two session persistence modes are available,
    as described in the following table:

    * ``HTTP_COOKIE``: A session persistence mechanism that inserts an HTTP
        cookie and is used to determine the destination back-end node. This is
        supported for HTTP load balancing only.
    * ``SOURCE_IP``: A session persistence mechanism that will keep track of the
        source IP address that is mapped and is able to determine the destination
        back-end node. This is supported for HTTP pass-through (SSL termination)
        and non-HTTP load balancing only.

    `Session Persistence Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/Sessions-d1e3728.html>`_
    """
    def __repr__(self):
        if 'persistenceType' in self:
            return '<SessionPersistence %s>' % self['persistenceType']
        return super(SessionPersistence, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'persistenceType':
            key = 'type'
        super(SessionPersistence, self).__setitem__(key, value)


class UsageReport(DotDict):
    """A CloudLoadBalancer Usage Report."""
    pass


class Stat(DotDict):
    """CloudLoadBalancers Load Balancer Stats.

    `Load Balancer Status Reference <http://docs.rackspace.com/loadbalancers/api/v1.0/clb-devguide/content/List_Load_Balancer_Stats-d1e1524.html>`_
    """
    pass


class VirtualIP(DotDict):
    """A CloudLoadBalancer Virtual IP.
 
    A virtual IP (VIP) makes a load balancer accessible by clients. The load
    balancing service supports either a public VIP, routable on the public
    Internet, or a ServiceNet address, routable only within the region in which
    the load balancer resides. 
    """
    def __repr__(self):
        if 'address' in self:
            return '<VirtualIP %s>' % self['address']
        return super(VirtualIP, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'ipVersion':
            key = 'version'
        super(VirtualIP, self).__setitem__(key, value)

    @classmethod
    def create(cls, version, type):
        """Create a Virtual IP.

        :param version: ``IPV4`` or ``IPV6``.
        :type version: str
        :param type: ``PUBLIC`` or ``SERVICENET``
        :type type: str
        :returns: A shiny new Virtual IP.
        :rtype: :class:`VirtualIP`

        .. versionadded:: 0.1
        """
        return cls(version=version, type=type)

    def delete(self):
        """Delete this Virtual IP.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'loadbalancer_id' in self
        url = '/'.join([get_url('cloudloadbalancers'), 'loadbalancers',
                        str(self['loadbalancer_id']), 'virtualips',
                        str(self['id'])])
        handle_request('delete', url)

    def to_dict(self):
        """Create a Rackspace formatted dict."""
        if 'id' in self:
            ret = {'id': self['id']}
        else:
            ret = {'ipVersion': self['version'],
                   'type': self['type']}
        return ret
