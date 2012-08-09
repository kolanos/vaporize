Vaporize
========

Vaporize is a clean and consistent library for accessing the `Rackspace Cloud API`_.
 
.. _Rackspace Cloud API: http://docs.rackspace.com/api/

Another One?
------------

There are already a number of good Python options out there for accessing the
Rackspace Cloud API. Unfortunately they have one thing in common: none of them
use the same pattern. This means a lot of wasted time looking things up in
the documentation. The other problem is that there is a library for each group
of sendpoints on the Rackspace cloud API. There's a libarry for CloudServers,
one for CloudFiles, one for CloudDNS and one for CloudLoadBalancers. Which menas
there's a lot of redundant code, requiring four imports and four instantiations 
and it's up to you to smooth over incompatibilities between them.

So Vaporize was born. One library for one API.

Installation
------------

To install Vaporize using PIP:

    pip install vaporize

Usage
-----

Vaporize is designed to be simple to use. Connect to your Rackspace Cloud in
just two lines of code:

    >>> import vaporize
    >>> vaporize.connect('username', 'apikey')

Documentation
-------------

API Documentation and a User Guide (in the works) available here_.

.. _here: http://kolanos.github.com/vaporize/

Contributing
------------

Vaporize is currently still in development. Contributors are welcome. Just fork
this repo and start making pull requests.

Features
--------

Support for the following Rackspace Cloud services:

 * CloudServers
 * CloudLoadBalancers
 * CloudDNS
 * CloudDatabases

Planned Features
----------------

Support for the following Rackspace Cloud services:

 * CloudFiles
 * CloudMonitoring

