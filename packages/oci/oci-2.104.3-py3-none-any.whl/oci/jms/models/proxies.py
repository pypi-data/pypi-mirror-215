# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class Proxies(object):
    """
    List of proxy properties to be configured in net.properties file.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new Proxies object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param use_system_proxies:
            The value to assign to the use_system_proxies property of this Proxies.
        :type use_system_proxies: bool

        :param http_proxy_host:
            The value to assign to the http_proxy_host property of this Proxies.
        :type http_proxy_host: str

        :param http_proxy_port:
            The value to assign to the http_proxy_port property of this Proxies.
        :type http_proxy_port: int

        :param https_proxy_host:
            The value to assign to the https_proxy_host property of this Proxies.
        :type https_proxy_host: str

        :param https_proxy_port:
            The value to assign to the https_proxy_port property of this Proxies.
        :type https_proxy_port: int

        :param ftp_proxy_host:
            The value to assign to the ftp_proxy_host property of this Proxies.
        :type ftp_proxy_host: str

        :param ftp_proxy_port:
            The value to assign to the ftp_proxy_port property of this Proxies.
        :type ftp_proxy_port: int

        :param socks_proxy_host:
            The value to assign to the socks_proxy_host property of this Proxies.
        :type socks_proxy_host: str

        :param socks_proxy_port:
            The value to assign to the socks_proxy_port property of this Proxies.
        :type socks_proxy_port: int

        """
        self.swagger_types = {
            'use_system_proxies': 'bool',
            'http_proxy_host': 'str',
            'http_proxy_port': 'int',
            'https_proxy_host': 'str',
            'https_proxy_port': 'int',
            'ftp_proxy_host': 'str',
            'ftp_proxy_port': 'int',
            'socks_proxy_host': 'str',
            'socks_proxy_port': 'int'
        }

        self.attribute_map = {
            'use_system_proxies': 'useSystemProxies',
            'http_proxy_host': 'httpProxyHost',
            'http_proxy_port': 'httpProxyPort',
            'https_proxy_host': 'httpsProxyHost',
            'https_proxy_port': 'httpsProxyPort',
            'ftp_proxy_host': 'ftpProxyHost',
            'ftp_proxy_port': 'ftpProxyPort',
            'socks_proxy_host': 'socksProxyHost',
            'socks_proxy_port': 'socksProxyPort'
        }

        self._use_system_proxies = None
        self._http_proxy_host = None
        self._http_proxy_port = None
        self._https_proxy_host = None
        self._https_proxy_port = None
        self._ftp_proxy_host = None
        self._ftp_proxy_port = None
        self._socks_proxy_host = None
        self._socks_proxy_port = None

    @property
    def use_system_proxies(self):
        """
        Gets the use_system_proxies of this Proxies.
        Sets \"java.net.useSystemProxies=true\" in net.properties when they exist.


        :return: The use_system_proxies of this Proxies.
        :rtype: bool
        """
        return self._use_system_proxies

    @use_system_proxies.setter
    def use_system_proxies(self, use_system_proxies):
        """
        Sets the use_system_proxies of this Proxies.
        Sets \"java.net.useSystemProxies=true\" in net.properties when they exist.


        :param use_system_proxies: The use_system_proxies of this Proxies.
        :type: bool
        """
        self._use_system_proxies = use_system_proxies

    @property
    def http_proxy_host(self):
        """
        Gets the http_proxy_host of this Proxies.
        Http host to be set in net.properties file.


        :return: The http_proxy_host of this Proxies.
        :rtype: str
        """
        return self._http_proxy_host

    @http_proxy_host.setter
    def http_proxy_host(self, http_proxy_host):
        """
        Sets the http_proxy_host of this Proxies.
        Http host to be set in net.properties file.


        :param http_proxy_host: The http_proxy_host of this Proxies.
        :type: str
        """
        self._http_proxy_host = http_proxy_host

    @property
    def http_proxy_port(self):
        """
        Gets the http_proxy_port of this Proxies.
        Http port number to be set in net.properties file.


        :return: The http_proxy_port of this Proxies.
        :rtype: int
        """
        return self._http_proxy_port

    @http_proxy_port.setter
    def http_proxy_port(self, http_proxy_port):
        """
        Sets the http_proxy_port of this Proxies.
        Http port number to be set in net.properties file.


        :param http_proxy_port: The http_proxy_port of this Proxies.
        :type: int
        """
        self._http_proxy_port = http_proxy_port

    @property
    def https_proxy_host(self):
        """
        Gets the https_proxy_host of this Proxies.
        Https host to be set in net.properties file.


        :return: The https_proxy_host of this Proxies.
        :rtype: str
        """
        return self._https_proxy_host

    @https_proxy_host.setter
    def https_proxy_host(self, https_proxy_host):
        """
        Sets the https_proxy_host of this Proxies.
        Https host to be set in net.properties file.


        :param https_proxy_host: The https_proxy_host of this Proxies.
        :type: str
        """
        self._https_proxy_host = https_proxy_host

    @property
    def https_proxy_port(self):
        """
        Gets the https_proxy_port of this Proxies.
        Https port number to be set in net.properties file.


        :return: The https_proxy_port of this Proxies.
        :rtype: int
        """
        return self._https_proxy_port

    @https_proxy_port.setter
    def https_proxy_port(self, https_proxy_port):
        """
        Sets the https_proxy_port of this Proxies.
        Https port number to be set in net.properties file.


        :param https_proxy_port: The https_proxy_port of this Proxies.
        :type: int
        """
        self._https_proxy_port = https_proxy_port

    @property
    def ftp_proxy_host(self):
        """
        Gets the ftp_proxy_host of this Proxies.
        Ftp host to be set in net.properties file.


        :return: The ftp_proxy_host of this Proxies.
        :rtype: str
        """
        return self._ftp_proxy_host

    @ftp_proxy_host.setter
    def ftp_proxy_host(self, ftp_proxy_host):
        """
        Sets the ftp_proxy_host of this Proxies.
        Ftp host to be set in net.properties file.


        :param ftp_proxy_host: The ftp_proxy_host of this Proxies.
        :type: str
        """
        self._ftp_proxy_host = ftp_proxy_host

    @property
    def ftp_proxy_port(self):
        """
        Gets the ftp_proxy_port of this Proxies.
        Ftp port number to be set in net.properties file.


        :return: The ftp_proxy_port of this Proxies.
        :rtype: int
        """
        return self._ftp_proxy_port

    @ftp_proxy_port.setter
    def ftp_proxy_port(self, ftp_proxy_port):
        """
        Sets the ftp_proxy_port of this Proxies.
        Ftp port number to be set in net.properties file.


        :param ftp_proxy_port: The ftp_proxy_port of this Proxies.
        :type: int
        """
        self._ftp_proxy_port = ftp_proxy_port

    @property
    def socks_proxy_host(self):
        """
        Gets the socks_proxy_host of this Proxies.
        Socks host to be set in net.properties file.


        :return: The socks_proxy_host of this Proxies.
        :rtype: str
        """
        return self._socks_proxy_host

    @socks_proxy_host.setter
    def socks_proxy_host(self, socks_proxy_host):
        """
        Sets the socks_proxy_host of this Proxies.
        Socks host to be set in net.properties file.


        :param socks_proxy_host: The socks_proxy_host of this Proxies.
        :type: str
        """
        self._socks_proxy_host = socks_proxy_host

    @property
    def socks_proxy_port(self):
        """
        Gets the socks_proxy_port of this Proxies.
        Socks port number to be set in net.properties file.


        :return: The socks_proxy_port of this Proxies.
        :rtype: int
        """
        return self._socks_proxy_port

    @socks_proxy_port.setter
    def socks_proxy_port(self, socks_proxy_port):
        """
        Sets the socks_proxy_port of this Proxies.
        Socks port number to be set in net.properties file.


        :param socks_proxy_port: The socks_proxy_port of this Proxies.
        :type: int
        """
        self._socks_proxy_port = socks_proxy_port

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
