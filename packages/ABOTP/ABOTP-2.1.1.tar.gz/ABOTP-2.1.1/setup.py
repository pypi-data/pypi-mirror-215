from setuptools import setup

setup(
    name='ABOTP',
    version='2.1.1',
    author='mister_svinia',
    author_email='i@savnil.ru',
    description='Advanced bi-directional over TCP and UDP protocol',
    long_description='''
ABOTP
=====

ABOTP is a Python package that provides a TCP and UDP double-socket protocol for bi-directional communication between clients and servers. It allows sending and receiving byte data over TCP and UDP connections.

Features
--------

- Supports both TCP and UDP communication protocols.
- Provides a server-side implementation (Server) for accepting client connections and handling data transmission.
- Offers a client-side implementation (Client) for connecting to a server and exchanging data.
- Supports sending and receiving lists of byte objects (bytes) as data payloads.
- Provides error handling for socket-related exceptions and connection status errors.
- Works with Python 3.10, 3.11, and 3.12.

Installation
------------

You can install ABOTP using pip::

    pip install ABOTP

Usage
-----

To use ABOTP, import the necessary modules and classes::

    from ABOTP import Server
    from ABOTP import Client
    from ABOTP import By

You can also use the built-in server-side operating capabilities::

    from ABOTP import storage
'''
    ,
    packages=['ABOTP'],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ],
)
