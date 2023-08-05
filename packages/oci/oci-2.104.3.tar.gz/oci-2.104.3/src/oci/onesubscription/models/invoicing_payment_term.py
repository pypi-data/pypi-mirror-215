# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class InvoicingPaymentTerm(object):
    """
    Payment Term details
    """

    def __init__(self, **kwargs):
        """
        Initializes a new InvoicingPaymentTerm object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this InvoicingPaymentTerm.
        :type name: str

        :param value:
            The value to assign to the value property of this InvoicingPaymentTerm.
        :type value: str

        :param description:
            The value to assign to the description property of this InvoicingPaymentTerm.
        :type description: str

        :param is_active:
            The value to assign to the is_active property of this InvoicingPaymentTerm.
        :type is_active: bool

        :param time_created:
            The value to assign to the time_created property of this InvoicingPaymentTerm.
        :type time_created: datetime

        :param created_by:
            The value to assign to the created_by property of this InvoicingPaymentTerm.
        :type created_by: str

        :param time_updated:
            The value to assign to the time_updated property of this InvoicingPaymentTerm.
        :type time_updated: datetime

        :param updated_by:
            The value to assign to the updated_by property of this InvoicingPaymentTerm.
        :type updated_by: str

        """
        self.swagger_types = {
            'name': 'str',
            'value': 'str',
            'description': 'str',
            'is_active': 'bool',
            'time_created': 'datetime',
            'created_by': 'str',
            'time_updated': 'datetime',
            'updated_by': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'value': 'value',
            'description': 'description',
            'is_active': 'isActive',
            'time_created': 'timeCreated',
            'created_by': 'createdBy',
            'time_updated': 'timeUpdated',
            'updated_by': 'updatedBy'
        }

        self._name = None
        self._value = None
        self._description = None
        self._is_active = None
        self._time_created = None
        self._created_by = None
        self._time_updated = None
        self._updated_by = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this InvoicingPaymentTerm.
        Payment Term name


        :return: The name of this InvoicingPaymentTerm.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this InvoicingPaymentTerm.
        Payment Term name


        :param name: The name of this InvoicingPaymentTerm.
        :type: str
        """
        self._name = name

    @property
    def value(self):
        """
        Gets the value of this InvoicingPaymentTerm.
        Payment Term value


        :return: The value of this InvoicingPaymentTerm.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this InvoicingPaymentTerm.
        Payment Term value


        :param value: The value of this InvoicingPaymentTerm.
        :type: str
        """
        self._value = value

    @property
    def description(self):
        """
        Gets the description of this InvoicingPaymentTerm.
        Payment term Description


        :return: The description of this InvoicingPaymentTerm.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this InvoicingPaymentTerm.
        Payment term Description


        :param description: The description of this InvoicingPaymentTerm.
        :type: str
        """
        self._description = description

    @property
    def is_active(self):
        """
        Gets the is_active of this InvoicingPaymentTerm.
        Payment term active flag


        :return: The is_active of this InvoicingPaymentTerm.
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """
        Sets the is_active of this InvoicingPaymentTerm.
        Payment term active flag


        :param is_active: The is_active of this InvoicingPaymentTerm.
        :type: bool
        """
        self._is_active = is_active

    @property
    def time_created(self):
        """
        Gets the time_created of this InvoicingPaymentTerm.
        Payment term last update date


        :return: The time_created of this InvoicingPaymentTerm.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this InvoicingPaymentTerm.
        Payment term last update date


        :param time_created: The time_created of this InvoicingPaymentTerm.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def created_by(self):
        """
        Gets the created_by of this InvoicingPaymentTerm.
        User that created the Payment term


        :return: The created_by of this InvoicingPaymentTerm.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this InvoicingPaymentTerm.
        User that created the Payment term


        :param created_by: The created_by of this InvoicingPaymentTerm.
        :type: str
        """
        self._created_by = created_by

    @property
    def time_updated(self):
        """
        Gets the time_updated of this InvoicingPaymentTerm.
        Payment term last update date


        :return: The time_updated of this InvoicingPaymentTerm.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this InvoicingPaymentTerm.
        Payment term last update date


        :param time_updated: The time_updated of this InvoicingPaymentTerm.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def updated_by(self):
        """
        Gets the updated_by of this InvoicingPaymentTerm.
        User that updated the Payment term


        :return: The updated_by of this InvoicingPaymentTerm.
        :rtype: str
        """
        return self._updated_by

    @updated_by.setter
    def updated_by(self, updated_by):
        """
        Sets the updated_by of this InvoicingPaymentTerm.
        User that updated the Payment term


        :param updated_by: The updated_by of this InvoicingPaymentTerm.
        :type: str
        """
        self._updated_by = updated_by

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
