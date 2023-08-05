# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .exadata_configuration_summary import ExadataConfigurationSummary
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ExadataExacsConfigurationSummary(ExadataConfigurationSummary):
    """
    Configuration summary of a Exacs exadata machine.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ExadataExacsConfigurationSummary object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.ExadataExacsConfigurationSummary.entity_source` attribute
        of this class is ``PE_COMANAGED_EXADATA`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param exadata_insight_id:
            The value to assign to the exadata_insight_id property of this ExadataExacsConfigurationSummary.
        :type exadata_insight_id: str

        :param entity_source:
            The value to assign to the entity_source property of this ExadataExacsConfigurationSummary.
            Allowed values for this property are: "EM_MANAGED_EXTERNAL_EXADATA", "PE_COMANAGED_EXADATA"
        :type entity_source: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ExadataExacsConfigurationSummary.
        :type compartment_id: str

        :param exadata_name:
            The value to assign to the exadata_name property of this ExadataExacsConfigurationSummary.
        :type exadata_name: str

        :param exadata_display_name:
            The value to assign to the exadata_display_name property of this ExadataExacsConfigurationSummary.
        :type exadata_display_name: str

        :param exadata_type:
            The value to assign to the exadata_type property of this ExadataExacsConfigurationSummary.
            Allowed values for this property are: "DBMACHINE", "EXACS", "EXACC"
        :type exadata_type: str

        :param exadata_rack_type:
            The value to assign to the exadata_rack_type property of this ExadataExacsConfigurationSummary.
            Allowed values for this property are: "FULL", "HALF", "QUARTER", "EIGHTH", "FLEX"
        :type exadata_rack_type: str

        :param defined_tags:
            The value to assign to the defined_tags property of this ExadataExacsConfigurationSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ExadataExacsConfigurationSummary.
        :type freeform_tags: dict(str, str)

        :param vmcluster_details:
            The value to assign to the vmcluster_details property of this ExadataExacsConfigurationSummary.
        :type vmcluster_details: list[oci.opsi.models.VmClusterSummary]

        :param opsi_private_endpoint_id:
            The value to assign to the opsi_private_endpoint_id property of this ExadataExacsConfigurationSummary.
        :type opsi_private_endpoint_id: str

        :param parent_id:
            The value to assign to the parent_id property of this ExadataExacsConfigurationSummary.
        :type parent_id: str

        """
        self.swagger_types = {
            'exadata_insight_id': 'str',
            'entity_source': 'str',
            'compartment_id': 'str',
            'exadata_name': 'str',
            'exadata_display_name': 'str',
            'exadata_type': 'str',
            'exadata_rack_type': 'str',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'vmcluster_details': 'list[VmClusterSummary]',
            'opsi_private_endpoint_id': 'str',
            'parent_id': 'str'
        }

        self.attribute_map = {
            'exadata_insight_id': 'exadataInsightId',
            'entity_source': 'entitySource',
            'compartment_id': 'compartmentId',
            'exadata_name': 'exadataName',
            'exadata_display_name': 'exadataDisplayName',
            'exadata_type': 'exadataType',
            'exadata_rack_type': 'exadataRackType',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'vmcluster_details': 'vmclusterDetails',
            'opsi_private_endpoint_id': 'opsiPrivateEndpointId',
            'parent_id': 'parentId'
        }

        self._exadata_insight_id = None
        self._entity_source = None
        self._compartment_id = None
        self._exadata_name = None
        self._exadata_display_name = None
        self._exadata_type = None
        self._exadata_rack_type = None
        self._defined_tags = None
        self._freeform_tags = None
        self._vmcluster_details = None
        self._opsi_private_endpoint_id = None
        self._parent_id = None
        self._entity_source = 'PE_COMANAGED_EXADATA'

    @property
    def opsi_private_endpoint_id(self):
        """
        **[Required]** Gets the opsi_private_endpoint_id of this ExadataExacsConfigurationSummary.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The opsi_private_endpoint_id of this ExadataExacsConfigurationSummary.
        :rtype: str
        """
        return self._opsi_private_endpoint_id

    @opsi_private_endpoint_id.setter
    def opsi_private_endpoint_id(self, opsi_private_endpoint_id):
        """
        Sets the opsi_private_endpoint_id of this ExadataExacsConfigurationSummary.
        The `OCID`__ of the OPSI private endpoint

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param opsi_private_endpoint_id: The opsi_private_endpoint_id of this ExadataExacsConfigurationSummary.
        :type: str
        """
        self._opsi_private_endpoint_id = opsi_private_endpoint_id

    @property
    def parent_id(self):
        """
        **[Required]** Gets the parent_id of this ExadataExacsConfigurationSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The parent_id of this ExadataExacsConfigurationSummary.
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """
        Sets the parent_id of this ExadataExacsConfigurationSummary.
        The `OCID`__ of the database.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param parent_id: The parent_id of this ExadataExacsConfigurationSummary.
        :type: str
        """
        self._parent_id = parent_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
