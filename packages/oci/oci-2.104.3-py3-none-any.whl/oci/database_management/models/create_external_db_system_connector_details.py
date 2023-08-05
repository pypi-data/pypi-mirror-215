# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateExternalDbSystemConnectorDetails(object):
    """
    The details required to create an external DB system connector.
    """

    #: A constant which can be used with the connector_type property of a CreateExternalDbSystemConnectorDetails.
    #: This constant has a value of "MACS"
    CONNECTOR_TYPE_MACS = "MACS"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateExternalDbSystemConnectorDetails object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.database_management.models.CreateExternalDbSystemMacsConnectorDetails`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param connector_type:
            The value to assign to the connector_type property of this CreateExternalDbSystemConnectorDetails.
            Allowed values for this property are: "MACS"
        :type connector_type: str

        :param display_name:
            The value to assign to the display_name property of this CreateExternalDbSystemConnectorDetails.
        :type display_name: str

        :param external_db_system_id:
            The value to assign to the external_db_system_id property of this CreateExternalDbSystemConnectorDetails.
        :type external_db_system_id: str

        """
        self.swagger_types = {
            'connector_type': 'str',
            'display_name': 'str',
            'external_db_system_id': 'str'
        }

        self.attribute_map = {
            'connector_type': 'connectorType',
            'display_name': 'displayName',
            'external_db_system_id': 'externalDbSystemId'
        }

        self._connector_type = None
        self._display_name = None
        self._external_db_system_id = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['connectorType']

        if type == 'MACS':
            return 'CreateExternalDbSystemMacsConnectorDetails'
        else:
            return 'CreateExternalDbSystemConnectorDetails'

    @property
    def connector_type(self):
        """
        **[Required]** Gets the connector_type of this CreateExternalDbSystemConnectorDetails.
        The type of connector.

        Allowed values for this property are: "MACS"


        :return: The connector_type of this CreateExternalDbSystemConnectorDetails.
        :rtype: str
        """
        return self._connector_type

    @connector_type.setter
    def connector_type(self, connector_type):
        """
        Sets the connector_type of this CreateExternalDbSystemConnectorDetails.
        The type of connector.


        :param connector_type: The connector_type of this CreateExternalDbSystemConnectorDetails.
        :type: str
        """
        allowed_values = ["MACS"]
        if not value_allowed_none_or_none_sentinel(connector_type, allowed_values):
            raise ValueError(
                "Invalid value for `connector_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._connector_type = connector_type

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateExternalDbSystemConnectorDetails.
        The user-friendly name for the external connector. The name does not have to be unique.


        :return: The display_name of this CreateExternalDbSystemConnectorDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateExternalDbSystemConnectorDetails.
        The user-friendly name for the external connector. The name does not have to be unique.


        :param display_name: The display_name of this CreateExternalDbSystemConnectorDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def external_db_system_id(self):
        """
        **[Required]** Gets the external_db_system_id of this CreateExternalDbSystemConnectorDetails.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The external_db_system_id of this CreateExternalDbSystemConnectorDetails.
        :rtype: str
        """
        return self._external_db_system_id

    @external_db_system_id.setter
    def external_db_system_id(self, external_db_system_id):
        """
        Sets the external_db_system_id of this CreateExternalDbSystemConnectorDetails.
        The `OCID`__ of the external DB system.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param external_db_system_id: The external_db_system_id of this CreateExternalDbSystemConnectorDetails.
        :type: str
        """
        self._external_db_system_id = external_db_system_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
