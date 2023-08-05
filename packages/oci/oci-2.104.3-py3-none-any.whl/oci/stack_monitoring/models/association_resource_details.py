# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AssociationResourceDetails(object):
    """
    Association Resource Details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AssociationResourceDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this AssociationResourceDetails.
        :type name: str

        :param type:
            The value to assign to the type property of this AssociationResourceDetails.
        :type type: str

        :param compartment_id:
            The value to assign to the compartment_id property of this AssociationResourceDetails.
        :type compartment_id: str

        """
        self.swagger_types = {
            'name': 'str',
            'type': 'str',
            'compartment_id': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'type': 'type',
            'compartment_id': 'compartmentId'
        }

        self._name = None
        self._type = None
        self._compartment_id = None

    @property
    def name(self):
        """
        Gets the name of this AssociationResourceDetails.
        Monitored Resource Name.


        :return: The name of this AssociationResourceDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AssociationResourceDetails.
        Monitored Resource Name.


        :param name: The name of this AssociationResourceDetails.
        :type: str
        """
        self._name = name

    @property
    def type(self):
        """
        Gets the type of this AssociationResourceDetails.
        Monitored Resource Type.


        :return: The type of this AssociationResourceDetails.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AssociationResourceDetails.
        Monitored Resource Type.


        :param type: The type of this AssociationResourceDetails.
        :type: str
        """
        self._type = type

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this AssociationResourceDetails.
        Compartment Identifier `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this AssociationResourceDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this AssociationResourceDetails.
        Compartment Identifier `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this AssociationResourceDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
