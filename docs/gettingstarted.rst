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
