Getting Started
===============

Vaporize is designed to be simple and easy to use. This documentation is
provided as a reference, but hopefully once you begin using Vaporize it should
be consistent enough that you won't need to rely upon it.

Connecting
----------

First things first, lets connect to the Rackspace Cloud.

    >>> import vaporize
    >>> vaporize.connect('username', 'apikey')

Replace ``username`` and ``apikey`` with your
Rackspace Cloud username and API key. If you don't have an API key you can
generate one on the Rackspace Cloud web site after logging in.

Calling ``vaporize.connect()`` will create a session with the Rackspace Cloud
API. This session will be used for all subsequent requests made to the API. A
session is typically good for 24 hours.

There's an optional third parameter available in the ``connect`` function as
well. It lets you choose which region you wish to work with. It accepts one of
three options: ``DFW`` (Dallas/Fort Worth), ``ORD`` (Chicago) or ``LON``
(London). Keep in mind that at the time of this writing only a few of the
Rackspace Cloud APIs support this third parameter. Vaporize uses ``DFW`` by
default.

First Request
-------------

There are many interfaces available on the Rackspace Cloud, but lets start with a
simple one. Lets get a list of all your CloudServers:

    >>> vaporize.servers.list()
    [<Server ...>, <Server ...>, ...]

Assuming you have some CloudServers already created you should see a list like
the one above. If you don't have any CloudServers yet, you'll just see an empty
list.

Creating a Server
-----------------

Shall we create a CLoudServer? It'll cost you. But for the sake of this guide,
you'll only be charged a small pro-rated fee.

Before we create a server we need to know what kind of server we want to create.
There are three things we need to know:

1. What should we name the server?
2. Which operating system should it run?
3. What should the server's specs be? (like RAM and disk space)

The first question is up to you. I recommend that you make it the intended
hostname of the server, but for the sake of this example we'll just use the name
'foo'.

The two questions can be determined using two seperate interfaces. On the
Rackspace Cloud operating systems are called "Images", as in .iso images and
server specifications care called "Flavors".

Lets get a list of Images available on the Rackspace Cloud (as of this writing):

    >>> images = vaporize.images.list()
    >>> for i, image in enumerate(images):
    ...   print i, image.name
    ... 
    0 Arch 2011.10
    1 Fedora 17
    2 Gentoo 11.0
    3 openSUSE 12
    4 Windows Server 2008 R2 x64 - SQL2K8R2 Web
    5 Red Hat Enterprise Linux 5.5
    6 Windows Server 2008 R2 x64
    7 Fedora 16
    8 Ubuntu 11.10
    9 CentOS 6.2
    10 Debian 6 (Squeeze)
    11 Windows Server 2008 R2 + SQL Server 2012 Standard
    12 Ubuntu 11.04
    13 CentOS 6.0
    14 Windows Server 2008 R2 + SQL Server 2012 Web
    15 Ubuntu 10.04 LTS
    16 Windows Server 2008 SP2 x86
    17 Windows Server 2008 SP2 x64
    18 Windows Server 2008 SP2 x64 - MSSQL2K8R2
    19 CentOS 5.8
    20 Red Hat Enterprise Linux 6
    21 Fedora 15
    22 Ubuntu 12.04 LTS
    23 Windows Server 2008 SP2 x86 - MSSQL2K8R2
    24 Windows Server 2008 R2 x64 - MSSQL2K8R2
    25 CentOS 5.6
    26 Debian 5 (Lenny)

Wow! So many to choose from! Most of them are Linux distributions. The ones that
start with the word "Windows" cost extra, check the Rackspace Cloud website for
details. I'm partial to UBuntu Server myself, so lets choose option 22.

    >>> image = images[22]

Now, what bout those Flavors?

    >>> flavors = vaporize.flavors.list()
    >>> for i, flavor in enumerate(flavors):
    ...   print i, flavor.name
    ... 
    0 256 server
    1 512 server
    2 1GB server
    3 2GB server
    4 4GB server
    5 8GB server
    6 15.5GB server
    7 30GB server

That was easy, huh? In case you're confused, the 256 and 512 servers are in MBs.
Not sure why they don't include the MB, but I digress. For the sake of this
example lets choose the smallest server type, option 0 (256MB).

    >>> flavor = flavors[0]

That's pretty much all we need to create a server. So without further ado...

    >>> server = vaporize.servers.create('foo', image, flavor)

Are we done? No, not quite yet. Rackspace still needs to build the server for
us. We can check the status of this process like so:

    >>> server.status
    u'BUILD'
    >>> server.progress
    0

And ot update it:

    >>> server.reload()
    >>> server.status
    u'BUILD'
    >>> server.progress
    25

Hey, it's 25% built! Progress! The amount of time it takes to build a server
varies. When it is done it will look like this:

    >>> server.status
    u'ACTIVE'
    >>> server.progress
    100

Until it is ``ACTIVE`` you wont be able to perform any additional operations on
your server. So sit tight until it is done.

Done? Great! Lets take a look at the server we've built:

    >>> server.name
    u'foo'
    >>> server.id
    12345678
    >>> server.addresses.public
    [u'198.101.209.35']

Yours will look a little different, obviously. Lets go ahead and change the root
password for this server (the one Rackspace created for you should have been
e-mailed to you):

    >>> server.modify(password='thisisaterriblepasswordamirite?')

Now lets check the status:

    >>> server.reload()
    >>> server.status
    u'PASSWORD'

Once it is ``ACTIVE`` again (this operation doesn't take long), you will be able
to SSH into this newly created server with your newly set password. For example:

    $ ssh root@198.101.209.35

And just like that you've got your very own Rackspace CloudServer!

Where are you going? We're not done yet! We have to clean up after ourselves.
This was just an example, afterall.

    >>> server.delete()

And just like that the server is torn back down again.

.. note::

    If you don't delete it, Rackspace will start to bill you for it. Spare me
    the angry e-mails please!