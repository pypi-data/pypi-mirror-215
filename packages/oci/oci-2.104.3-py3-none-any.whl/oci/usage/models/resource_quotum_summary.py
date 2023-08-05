# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ResourceQuotumSummary(object):
    """
    The resource quota balance details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ResourceQuotumSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this ResourceQuotumSummary.
        :type name: str

        :param is_allowed:
            The value to assign to the is_allowed property of this ResourceQuotumSummary.
        :type is_allowed: bool

        :param limit:
            The value to assign to the limit property of this ResourceQuotumSummary.
        :type limit: float

        :param balance:
            The value to assign to the balance property of this ResourceQuotumSummary.
        :type balance: float

        :param is_overage:
            The value to assign to the is_overage property of this ResourceQuotumSummary.
        :type is_overage: bool

        :param purchased_limit:
            The value to assign to the purchased_limit property of this ResourceQuotumSummary.
        :type purchased_limit: float

        :param service:
            The value to assign to the service property of this ResourceQuotumSummary.
        :type service: str

        :param is_dependency:
            The value to assign to the is_dependency property of this ResourceQuotumSummary.
        :type is_dependency: bool

        :param affected_resource:
            The value to assign to the affected_resource property of this ResourceQuotumSummary.
        :type affected_resource: str

        """
        self.swagger_types = {
            'name': 'str',
            'is_allowed': 'bool',
            'limit': 'float',
            'balance': 'float',
            'is_overage': 'bool',
            'purchased_limit': 'float',
            'service': 'str',
            'is_dependency': 'bool',
            'affected_resource': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'is_allowed': 'isAllowed',
            'limit': 'limit',
            'balance': 'balance',
            'is_overage': 'isOverage',
            'purchased_limit': 'purchasedLimit',
            'service': 'service',
            'is_dependency': 'isDependency',
            'affected_resource': 'affectedResource'
        }

        self._name = None
        self._is_allowed = None
        self._limit = None
        self._balance = None
        self._is_overage = None
        self._purchased_limit = None
        self._service = None
        self._is_dependency = None
        self._affected_resource = None

    @property
    def name(self):
        """
        Gets the name of this ResourceQuotumSummary.
        The resource name.


        :return: The name of this ResourceQuotumSummary.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ResourceQuotumSummary.
        The resource name.


        :param name: The name of this ResourceQuotumSummary.
        :type: str
        """
        self._name = name

    @property
    def is_allowed(self):
        """
        Gets the is_allowed of this ResourceQuotumSummary.
        Used to indicate if further quota consumption isAllowed.


        :return: The is_allowed of this ResourceQuotumSummary.
        :rtype: bool
        """
        return self._is_allowed

    @is_allowed.setter
    def is_allowed(self, is_allowed):
        """
        Sets the is_allowed of this ResourceQuotumSummary.
        Used to indicate if further quota consumption isAllowed.


        :param is_allowed: The is_allowed of this ResourceQuotumSummary.
        :type: bool
        """
        self._is_allowed = is_allowed

    @property
    def limit(self):
        """
        Gets the limit of this ResourceQuotumSummary.
        The quota limit.


        :return: The limit of this ResourceQuotumSummary.
        :rtype: float
        """
        return self._limit

    @limit.setter
    def limit(self, limit):
        """
        Sets the limit of this ResourceQuotumSummary.
        The quota limit.


        :param limit: The limit of this ResourceQuotumSummary.
        :type: float
        """
        self._limit = limit

    @property
    def balance(self):
        """
        Gets the balance of this ResourceQuotumSummary.
        The quota balance.


        :return: The balance of this ResourceQuotumSummary.
        :rtype: float
        """
        return self._balance

    @balance.setter
    def balance(self, balance):
        """
        Sets the balance of this ResourceQuotumSummary.
        The quota balance.


        :param balance: The balance of this ResourceQuotumSummary.
        :type: float
        """
        self._balance = balance

    @property
    def is_overage(self):
        """
        Gets the is_overage of this ResourceQuotumSummary.
        Used to indicate if overages are incurred.


        :return: The is_overage of this ResourceQuotumSummary.
        :rtype: bool
        """
        return self._is_overage

    @is_overage.setter
    def is_overage(self, is_overage):
        """
        Sets the is_overage of this ResourceQuotumSummary.
        Used to indicate if overages are incurred.


        :param is_overage: The is_overage of this ResourceQuotumSummary.
        :type: bool
        """
        self._is_overage = is_overage

    @property
    def purchased_limit(self):
        """
        Gets the purchased_limit of this ResourceQuotumSummary.
        The purchased quota limit.


        :return: The purchased_limit of this ResourceQuotumSummary.
        :rtype: float
        """
        return self._purchased_limit

    @purchased_limit.setter
    def purchased_limit(self, purchased_limit):
        """
        Sets the purchased_limit of this ResourceQuotumSummary.
        The purchased quota limit.


        :param purchased_limit: The purchased_limit of this ResourceQuotumSummary.
        :type: float
        """
        self._purchased_limit = purchased_limit

    @property
    def service(self):
        """
        Gets the service of this ResourceQuotumSummary.
        The service name.


        :return: The service of this ResourceQuotumSummary.
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """
        Sets the service of this ResourceQuotumSummary.
        The service name.


        :param service: The service of this ResourceQuotumSummary.
        :type: str
        """
        self._service = service

    @property
    def is_dependency(self):
        """
        Gets the is_dependency of this ResourceQuotumSummary.
        Used to indicate any resource dependencies.


        :return: The is_dependency of this ResourceQuotumSummary.
        :rtype: bool
        """
        return self._is_dependency

    @is_dependency.setter
    def is_dependency(self, is_dependency):
        """
        Sets the is_dependency of this ResourceQuotumSummary.
        Used to indicate any resource dependencies.


        :param is_dependency: The is_dependency of this ResourceQuotumSummary.
        :type: bool
        """
        self._is_dependency = is_dependency

    @property
    def affected_resource(self):
        """
        Gets the affected_resource of this ResourceQuotumSummary.
        The affected resource name.


        :return: The affected_resource of this ResourceQuotumSummary.
        :rtype: str
        """
        return self._affected_resource

    @affected_resource.setter
    def affected_resource(self, affected_resource):
        """
        Sets the affected_resource of this ResourceQuotumSummary.
        The affected resource name.


        :param affected_resource: The affected_resource of this ResourceQuotumSummary.
        :type: str
        """
        self._affected_resource = affected_resource

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
