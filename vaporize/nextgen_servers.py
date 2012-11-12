# -*- coding: utf-8 -*-

import json

from vaporize.core import convert_datetime, get_url, handle_request, query
from vaporize.utils import DotDict

class NextGenFlavor(DotDict):
    """A CloudNextGenServers NextGenFlavor."""
    def __repr__(self):
        if 'name' in self:
            return '<NextGenFlavor %s>' % self['name']
        return super(NextGenFlavor, self).__repr__()

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of NextGenFlavors.

        :param limit: Limit the result set by a number
        :type limit: int
        :param offset: Offset the result set by a number
        :type offset: int
        :param detail: Return additional details about each NextGenFlavor
        :type: bool
        :returns: A list of CloudNextGenServers NextGenFlavors.
        :rtype: :class:`NextGenFlavor`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudserversopenstack'), 'flavors']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls, container='flavors')

    @classmethod
    def get(cls, id):
        """Returns a NextGenFlavor by ID.

        :param id: The ID of the NextGenFlavor to retrieve
        :type id: int
        :returns: A CloudNextGenServers NextGenFlavor matching the ID.
        :rtype: :class:`NextGenFlavor`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudserversopenstack'), 'flavors', str(id)])
        return handle_request('get', url, wrapper=cls, container='flavor')


class NextGenImage(DotDict):
    """A CloudNextGenServers NextGenImage."""
    def __repr__(self):
        if 'name' in self:
            return '<NextGenImage %s>' % self['name']
        return super(NextGenImage, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'serverId':
            key = 'server_id'
        elif key in ['created', 'updated']:
            value = convert_datetime(value)
        super(NextGenImage, self).__setitem__(key, value)

    def reload(self):
        """Reload this NextGenImage (an implicit :func:`get`).

        :returns: An updated CloudNextGenServers NextGenImage.
        :rtype: :class:`NextGenImage`

        .. versionadded:: 0.1.9
        """
        assert 'id' in self, "Missing NextGenImage ID"
        response = NextGenImage.get(self['id'])
        self.update(response)
        return self

    def delete(self):
        """Delete this NextGenImage.

        .. note::

            You can only delete NextGenImages you create.

        .. warning::

            There is not confirmation step for this operation. Deleting an
            image is permanent.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'images', str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """Returns a list of CloudNextGenServers NextGenImages.

        :param limit: Limit the result set by a cetain number
        :type limit: int
        :param offset: Offset the result set by a certain number
        :type offset: int
        :param detail: Return additional details about each NextGenImage
        :type detail: bool
        :returns: A list of CloudNextGenServers NextGenImages.
        :rtype: A list of :class:`NextGenImage`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudserversopenstack'), 'images']
        if detail:
            url.append('detail')
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=NextGenImage, container='images')

    @classmethod
    def get(cls, id):
        """Return an NextGenImage by ID.

        :param id: The ID of the NextGenImage to retrieve
        :type id: int
        :returns: A CloudNextGenServer NextGenImage matching the ID.
        :rtype: :class:`NextGenImage`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudserversopenstack'), 'images', str(id)])
        return handle_request('get', url, wrapper=cls, container='image')

    @classmethod
    def create(cls, name, server):
        """Create an NextGenImage.

        :param name: Name of the NextGenImage
        :type name: str
        :param server: NextGenServer or ``id`` to base the NextGenImage upon
        :type server: int or :class:`NextGenServer`
        :returns: A shiny new CloudNextGenServers NextGenImage.
        :rtype: :class:`NextGenImage`

        .. versionadded:: 0.1
        """
        if isinstance(server, NextGenServer):
            server = server.id
        server = int(server)
        data = {'image': {'serverId': server,
                          'name': name}}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'images'])
        return handle_request('post', url, data, cls, 'image')


class VolumeAttachment(DotDict):
    def __repr__(self):
        if 'volume_id' in self:
            return '<Volume %s>' % self['volume_id']
        return super(VolumeAttachment, self).__repr__()

    def __setitem__(self, key, value):
        if key == 'volumeAttachemnts':
            key = 'id'
        super(VolumeAttachment, self).__setitem__(key, value)


class NextGenServer(DotDict):
    """A CloudNextGenServers NextGenServer."""
    def __repr__(self):
        if 'name' in self:
            return "<NextGenServer %s>" % self['name']
        return super(NextGenServer, self).__repr__()

    def reload(self):
        """Reload this NextGenServer (an implicit :func:`get`).

        :returns: An updated CloudNextGenServers NextGenServer.
        :rtype: :class:`NextGenServer`

    .. versionadded:: 0.1
        """
        assert 'id' in self
        response = NextGenServer.get(self['id'])
        self.update(response)
        return self

    def ips(self):
        """Returns a list of ip addresses attached to the NextGenServer instance.

        """
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                str(self['id']), 'ips'])
        return  handle_request('get', url, wrapper=cls, container='addresses')

    def ips_by_networkid(self, network_id=None):
        """Returns the list of ip addresses attached to the NextGenServer by the
        specified network_id.

        """
        assert 'id' in self
        assert network_is is not None
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                str(self['id']), 'ips', str(network_id)])
        return  handle_request('get', url, wrapper=cls, container='network')

    def update_server(self, name=None, accessIPv4=None, accessIPv6=None):
        """Update this NextGenServer's name or ip addresses.

        :param name: Change the NextGenServer's name
        :type name: str
        :param accessIPv4: IPv4 access address
        :type name: str
        :param accessIPv6: IPv6 access address
        :type name: str
        :returns: A modified CloudNextGenServers NextGenServer.
        :rtype: :class:`NextGenServer`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = {'server': {}}
        if name is not None:
            data['server']['name'] = name
        if addressIPv4 is not None:
            data['server']['addressIPv4'] = addressIPv4
        if addressIPv6 is not None:
            data['server']['addressIPv6'] = addressIPv6
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers', str(self['id'])])
        response = handle_request('put', url, data=data)
        if response:
            if name is not None:
                self['name'] = name
        return self

    def delete(self):
        """Delete this NextGenServer.

        .. warning::

            There is no confirmation step for this operation. When you delete a
            server it is permanent. If in doubt, create a backup image
            (:func:`vaporize.images.create`) first before deleting.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'servers', str(self['id'])])
        handle_request('delete', url)

    def volumes_list(self):
        """Return the list of volumes attached to this NextGenServer.

        """
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                str(self['id']), 'os-volume_attachments'])
        self['volumes'] = handle_request('get', url, wrapper=VolumeAttachment,
                container='volumeAttachments', server_id=str(self['id']))
        return self['volumes']

    def volume_detach(self, volumeId):
        """Detach the volume specified by volume_id from this NextGenServer.

        """
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
            str(self['id']), 'os-volume_attachments', str(volumeId)])
        handle_request('delete', url)

    def volume_attach(self, volumeId, device=''):
        """Attach the volume specified by volume_id to this NextGenServer.

        """
        assert 'id' in self
        assert len(volumeId) > 0
        data = ({
                'volumeAttachment': {
                    'volumeId': str(volumeId)
                }
        })
        if len(device) > 0 :
            data['volumeAttachment']['device'] = device

        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
            str(self['id']), 'os-volume_attachments'])
        handle_request('post', url, data=data)

    def change_admin_pass(self, password):
        """Change admin password.
        """
        assert len(password) >= 8
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
            str(self['id']), 'action'])
        data = json.dumps({ "changePassword": { "adminPass" : str(password)}})
        return handle_request('post', url, data)

    def reboot(self, type='SOFT'):
        """Perform a soft/hard reboot on this NextGenServer.

        :param type: A reboot type (``SOFT`` or ``HARD``).
        :type type: str

        .. versionadded:: 0.1
        """
        assert 'id' in self, "Missing NextGenServer ID"
        assert type in ['SOFT', 'HARD'], "Reboot type must be 'SOFT' or 'HARD'"
        data = json.dumps({'reboot': {'type': type}})
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def rebuild(self, name, image, flavor, adminpass, accessIPv4=None,
            accessIPv6=None, metadata={}, personality=[], diskConfig='AUTO'):
        """Rebuild this NextGenServer using a specified NextGenImage

        :param image: The NextGenImage or ``id``
        :type image: int or :class:`NextGenImage`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'name' in self or len(name) > 0
        assert len(adminpass) > 8
        if name:
            self['name'] = name
        if isinstance(image, NextGenImage):
            image = image.id
        if isinstance(flavor, NextGenFlavor):
            flavor = flavor.id
        image = int(image)
        flavor = int(flavor)
        data = {'rebuild':{
                    'name': str(self['name']),
                    'imageRef': str(image),
                    'flavorRef': str(flavor),
                    'adminPass': str(adminpass),
                    'OS-DCF:diskConfig': str(diskConfig)
                    }}
        if accessIPv4 is not None:
            data['rebuild']['accessIPv4'] = str(accessIPv4)
        if accessIPv6 is not None:
            data['rebuild']['accessIPv6'] = str(accessIPv6)
        if isinstance(files, dict):
            for path, contents in list(files.items()):
                data['personality'].append({'path': path, 'contents': contents})
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def resize(self, name, flavor, diskConfig='AUTO'):
        """Resize this NextGenServer to a specific NextGenFlavor size

        :param flavor: The NextGenFlavor or ``id``
        :type flavor: int or :class:`NextGenFlavor`

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert 'name' in self or len(name) > 0
        if len(name) > 0:
            self['name'] = str(name)
        if isinstance(flavor, NextGenFlavor):
            flavor = flavor.id
        flavor = int(flavor)
        data = json.dumps({'resize': {'flavorId': flavor}})
        data['resize']['name'] = self['name']
        data['resize']['OS-DCF:diskConfig'] = str(diskConfig)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers', str(self['id']),
                        'action'])
        handle_request('post', url, data)

    def confirm_resize(self):
        """Confirm a successful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'confirmResize': None})
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def revert_resize(self):
        """Revert an unsuccessful resize operation

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'revertResize': None})
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        handle_request('post', url, data)

    def rescue(self):
        """Put server im rescue mode.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'rescue': None})
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        return handle_request('post', url, data)

    def unrescue(self):
        """Take server out of rescue mode

        .. versionadded:: 0.1
        """
        assert 'id' in self
        data = json.dumps({'unrescue': None})
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        return handle_request('post', url, data)

    def create_image(self, name=None, metadata={}):
        """Create a server image.

        .. versionadded:: 0.1
        """
        assert 'id' in self
        assert name is not None
        data = { 'createImage' : {
                    'name' : str(name),
                    'metadata': metadata or {}
                    }}
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers',
                        str(self['id']), 'action'])
        return handle_request('post', url, data)

    @classmethod
    def list(cls, limit=None, offset=None, detail=False):
        """
        List of CloudNextGenServer NextGenServers

        :param limit: Limit the result set to a certain number
        :type limit: int
        :param offset: Offset the result set by a certain number
        :type offset: int
        :returns: A list of CloudNextGenServers NextGenServers.
        :rtype: List of :class:`NextGenServer`

        .. versionadded:: 0.1
        """
        url = [get_url('cloudserversopenstack'), 'servers']
        if detail:
            url.append(detail)
        url = '/'.join(url)
        if limit is not None or offset is not None:
            url = query(url, limit=limit, offset=offset)
        return handle_request('get', url, wrapper=cls, container='servers')

    @classmethod
    def get(cls, id):
        """Return a NextGenServer using an ID

        :param id: The ``id`` of the NextGenServer to be retrieved
        :type id: int
        :return: A :class:`NextGenServer`

        .. versionadded:: 0.1
        """
        url = '/'.join([get_url('cloudserversopenstack'), 'servers', str(id)])
        return handle_request('get', url, wrapper=cls, container='server')

    @classmethod
    def create(cls, name, image, flavor, adminpass=None, diskConfig=None,
            metadata=None, personality=None, networksUUIDs=[], accessIPv4=None,
            accessIPv6=None):
        """Create a CloudNextGenServers NextGenServer

        :param name: A NextGenServer's name
        :type name: str
        :param image: An NextGenImage or ``id``
        :type image: int or :class:`NextGenImage`
        :param flavor: A NextGenFlavor or ``id``
        :type flavor: int or :class:`NextGenFlavor`

        .. versionadded:: 0.1
        """
        if isinstance(image, NextGenImage):
            image = image.id
        image = int(image)
        if isinstance(flavor, NextGenFlavor):
            flavor = flavor.id
        flavor = int(flavor)
        data = {'server': {'name': name,
                           'imageRef': image,
                           'flavorRef': flavor,
                           'metadata': metadata or {},
                           'personality': []
                            }}
        if isinstance(files, dict):
            for path, contents in list(files.items()):
                data['personality'].append({'path': path, 'contents': contents})
        if len(networksUUIDs) > 0:
            data['server']['networks'] = [ {'uuuid': v} for v in networksUUIDs ]
        if diskConfig:
            data['server']['OS-DCF:diskConfig'] = diskConfig
        if accessIPv4:
            data['server']['accessIPv4'] = accessIPv4
        if accessIPv6:
            data['server']['accessIPv6'] = accessIPv6
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'servers'])
        return handle_request('post', url, data, cls, 'server')


class Network(DotDict):
    """A Cloudservers v2 network."""

    def __repr__(self):
        if 'label' in self:
            return '<Network %s>' % self['label']
        return super(Network, self).__repr__()

    def delete(self):
        """Delete this Network"""
        assert 'id' in self
        url = '/'.join([get_url('cloudserversopenstack'), 'os-networksv2',
            str(self['id'])])
        handle_request('delete', url)

    @classmethod
    def list(cls):
        """Returns a list of networks.

        :param detail: Provides more details about the network
        :type: A list of :class:`Network`
        """
        url = [get_url('cloudserversopenstack'), 'os-networksv2']
        url = '/'.join(url)
        return handle_request('get', url, wrapper=cls, container='networks')

    @classmethod
    def get(cls, network_id):
        """Returns a Network by id

        :param network_id: The ``network_id`` of the Network to be retrieved
        :type id: str
        :returns: A :class:`Network`
        """
        assert len(network_id) > 0
        url = '/'.join([get_url('cloudserversopenstack'), 'os-networksv2', str(network_id)])
        return handle_request('get', url, wrapper=cls, container='network')

    @classmethod
    def create(cls, cidr, label):
        """Creates a Network.

        :param cidr: cidr network block
        :type name: str
        :param label: network label
        :type name: str
        """
        assert len(cidr) > 0
        assert len(label) > 0
        data = {'network':
                    {'cidr': cidr,
                     'label': label
                     }
                }
        data = json.dumps(data)
        url = '/'.join([get_url('cloudserversopenstack'), 'os-networksv2'])
        return handle_request('post', url, data, cls, 'network')

