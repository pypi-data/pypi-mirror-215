# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .discovered_external_db_system_component import DiscoveredExternalDbSystemComponent
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiscoveredExternalPluggableDatabase(DiscoveredExternalDbSystemComponent):
    """
    The details of an external Pluggable Database (PDB) discovered in an external DB system discovery run.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DiscoveredExternalPluggableDatabase object with values from keyword arguments. The default value of the :py:attr:`~oci.database_management.models.DiscoveredExternalPluggableDatabase.component_type` attribute
        of this class is ``PLUGGABLE_DATABASE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param component_id:
            The value to assign to the component_id property of this DiscoveredExternalPluggableDatabase.
        :type component_id: str

        :param display_name:
            The value to assign to the display_name property of this DiscoveredExternalPluggableDatabase.
        :type display_name: str

        :param component_name:
            The value to assign to the component_name property of this DiscoveredExternalPluggableDatabase.
        :type component_name: str

        :param component_type:
            The value to assign to the component_type property of this DiscoveredExternalPluggableDatabase.
            Allowed values for this property are: "ASM", "ASM_INSTANCE", "CLUSTER", "CLUSTER_INSTANCE", "DATABASE", "DATABASE_INSTANCE", "DATABASE_HOME", "DATABASE_NODE", "DBSYSTEM", "LISTENER", "PLUGGABLE_DATABASE"
        :type component_type: str

        :param resource_id:
            The value to assign to the resource_id property of this DiscoveredExternalPluggableDatabase.
        :type resource_id: str

        :param is_selected_for_monitoring:
            The value to assign to the is_selected_for_monitoring property of this DiscoveredExternalPluggableDatabase.
        :type is_selected_for_monitoring: bool

        :param status:
            The value to assign to the status property of this DiscoveredExternalPluggableDatabase.
            Allowed values for this property are: "NEW", "EXISTING", "MARKED_FOR_DELETION", "UNKNOWN"
        :type status: str

        :param associated_components:
            The value to assign to the associated_components property of this DiscoveredExternalPluggableDatabase.
        :type associated_components: list[oci.database_management.models.AssociatedComponent]

        :param compartment_id:
            The value to assign to the compartment_id property of this DiscoveredExternalPluggableDatabase.
        :type compartment_id: str

        :param container_database_id:
            The value to assign to the container_database_id property of this DiscoveredExternalPluggableDatabase.
        :type container_database_id: str

        :param guid:
            The value to assign to the guid property of this DiscoveredExternalPluggableDatabase.
        :type guid: str

        :param connector:
            The value to assign to the connector property of this DiscoveredExternalPluggableDatabase.
        :type connector: oci.database_management.models.ExternalDbSystemDiscoveryConnector

        """
        self.swagger_types = {
            'component_id': 'str',
            'display_name': 'str',
            'component_name': 'str',
            'component_type': 'str',
            'resource_id': 'str',
            'is_selected_for_monitoring': 'bool',
            'status': 'str',
            'associated_components': 'list[AssociatedComponent]',
            'compartment_id': 'str',
            'container_database_id': 'str',
            'guid': 'str',
            'connector': 'ExternalDbSystemDiscoveryConnector'
        }

        self.attribute_map = {
            'component_id': 'componentId',
            'display_name': 'displayName',
            'component_name': 'componentName',
            'component_type': 'componentType',
            'resource_id': 'resourceId',
            'is_selected_for_monitoring': 'isSelectedForMonitoring',
            'status': 'status',
            'associated_components': 'associatedComponents',
            'compartment_id': 'compartmentId',
            'container_database_id': 'containerDatabaseId',
            'guid': 'guid',
            'connector': 'connector'
        }

        self._component_id = None
        self._display_name = None
        self._component_name = None
        self._component_type = None
        self._resource_id = None
        self._is_selected_for_monitoring = None
        self._status = None
        self._associated_components = None
        self._compartment_id = None
        self._container_database_id = None
        self._guid = None
        self._connector = None
        self._component_type = 'PLUGGABLE_DATABASE'

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this DiscoveredExternalPluggableDatabase.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this DiscoveredExternalPluggableDatabase.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this DiscoveredExternalPluggableDatabase.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this DiscoveredExternalPluggableDatabase.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def container_database_id(self):
        """
        **[Required]** Gets the container_database_id of this DiscoveredExternalPluggableDatabase.
        The unique identifier of the parent Container Database (CDB).


        :return: The container_database_id of this DiscoveredExternalPluggableDatabase.
        :rtype: str
        """
        return self._container_database_id

    @container_database_id.setter
    def container_database_id(self, container_database_id):
        """
        Sets the container_database_id of this DiscoveredExternalPluggableDatabase.
        The unique identifier of the parent Container Database (CDB).


        :param container_database_id: The container_database_id of this DiscoveredExternalPluggableDatabase.
        :type: str
        """
        self._container_database_id = container_database_id

    @property
    def guid(self):
        """
        Gets the guid of this DiscoveredExternalPluggableDatabase.
        The unique identifier of the PDB.


        :return: The guid of this DiscoveredExternalPluggableDatabase.
        :rtype: str
        """
        return self._guid

    @guid.setter
    def guid(self, guid):
        """
        Sets the guid of this DiscoveredExternalPluggableDatabase.
        The unique identifier of the PDB.


        :param guid: The guid of this DiscoveredExternalPluggableDatabase.
        :type: str
        """
        self._guid = guid

    @property
    def connector(self):
        """
        Gets the connector of this DiscoveredExternalPluggableDatabase.

        :return: The connector of this DiscoveredExternalPluggableDatabase.
        :rtype: oci.database_management.models.ExternalDbSystemDiscoveryConnector
        """
        return self._connector

    @connector.setter
    def connector(self, connector):
        """
        Sets the connector of this DiscoveredExternalPluggableDatabase.

        :param connector: The connector of this DiscoveredExternalPluggableDatabase.
        :type: oci.database_management.models.ExternalDbSystemDiscoveryConnector
        """
        self._connector = connector

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
