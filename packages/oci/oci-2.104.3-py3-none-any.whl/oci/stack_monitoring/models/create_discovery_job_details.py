# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDiscoveryJobDetails(object):
    """
    The request of DiscoveryJob details.
    """

    #: A constant which can be used with the discovery_type property of a CreateDiscoveryJobDetails.
    #: This constant has a value of "ADD"
    DISCOVERY_TYPE_ADD = "ADD"

    #: A constant which can be used with the discovery_type property of a CreateDiscoveryJobDetails.
    #: This constant has a value of "ADD_WITH_RETRY"
    DISCOVERY_TYPE_ADD_WITH_RETRY = "ADD_WITH_RETRY"

    #: A constant which can be used with the discovery_type property of a CreateDiscoveryJobDetails.
    #: This constant has a value of "REFRESH"
    DISCOVERY_TYPE_REFRESH = "REFRESH"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDiscoveryJobDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param discovery_type:
            The value to assign to the discovery_type property of this CreateDiscoveryJobDetails.
            Allowed values for this property are: "ADD", "ADD_WITH_RETRY", "REFRESH"
        :type discovery_type: str

        :param discovery_client:
            The value to assign to the discovery_client property of this CreateDiscoveryJobDetails.
        :type discovery_client: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateDiscoveryJobDetails.
        :type compartment_id: str

        :param discovery_details:
            The value to assign to the discovery_details property of this CreateDiscoveryJobDetails.
        :type discovery_details: oci.stack_monitoring.models.DiscoveryDetails

        :param should_propagate_tags_to_discovered_resources:
            The value to assign to the should_propagate_tags_to_discovered_resources property of this CreateDiscoveryJobDetails.
        :type should_propagate_tags_to_discovered_resources: bool

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateDiscoveryJobDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateDiscoveryJobDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'discovery_type': 'str',
            'discovery_client': 'str',
            'compartment_id': 'str',
            'discovery_details': 'DiscoveryDetails',
            'should_propagate_tags_to_discovered_resources': 'bool',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'discovery_type': 'discoveryType',
            'discovery_client': 'discoveryClient',
            'compartment_id': 'compartmentId',
            'discovery_details': 'discoveryDetails',
            'should_propagate_tags_to_discovered_resources': 'shouldPropagateTagsToDiscoveredResources',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._discovery_type = None
        self._discovery_client = None
        self._compartment_id = None
        self._discovery_details = None
        self._should_propagate_tags_to_discovered_resources = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def discovery_type(self):
        """
        Gets the discovery_type of this CreateDiscoveryJobDetails.
        Add option submits new discovery Job. Add with retry option to re-submit failed discovery job. Refresh option refreshes the existing discovered resources.

        Allowed values for this property are: "ADD", "ADD_WITH_RETRY", "REFRESH"


        :return: The discovery_type of this CreateDiscoveryJobDetails.
        :rtype: str
        """
        return self._discovery_type

    @discovery_type.setter
    def discovery_type(self, discovery_type):
        """
        Sets the discovery_type of this CreateDiscoveryJobDetails.
        Add option submits new discovery Job. Add with retry option to re-submit failed discovery job. Refresh option refreshes the existing discovered resources.


        :param discovery_type: The discovery_type of this CreateDiscoveryJobDetails.
        :type: str
        """
        allowed_values = ["ADD", "ADD_WITH_RETRY", "REFRESH"]
        if not value_allowed_none_or_none_sentinel(discovery_type, allowed_values):
            raise ValueError(
                "Invalid value for `discovery_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._discovery_type = discovery_type

    @property
    def discovery_client(self):
        """
        Gets the discovery_client of this CreateDiscoveryJobDetails.
        Client who submits discovery job.


        :return: The discovery_client of this CreateDiscoveryJobDetails.
        :rtype: str
        """
        return self._discovery_client

    @discovery_client.setter
    def discovery_client(self, discovery_client):
        """
        Sets the discovery_client of this CreateDiscoveryJobDetails.
        Client who submits discovery job.


        :param discovery_client: The discovery_client of this CreateDiscoveryJobDetails.
        :type: str
        """
        self._discovery_client = discovery_client

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateDiscoveryJobDetails.
        The OCID of Compartment


        :return: The compartment_id of this CreateDiscoveryJobDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateDiscoveryJobDetails.
        The OCID of Compartment


        :param compartment_id: The compartment_id of this CreateDiscoveryJobDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def discovery_details(self):
        """
        **[Required]** Gets the discovery_details of this CreateDiscoveryJobDetails.

        :return: The discovery_details of this CreateDiscoveryJobDetails.
        :rtype: oci.stack_monitoring.models.DiscoveryDetails
        """
        return self._discovery_details

    @discovery_details.setter
    def discovery_details(self, discovery_details):
        """
        Sets the discovery_details of this CreateDiscoveryJobDetails.

        :param discovery_details: The discovery_details of this CreateDiscoveryJobDetails.
        :type: oci.stack_monitoring.models.DiscoveryDetails
        """
        self._discovery_details = discovery_details

    @property
    def should_propagate_tags_to_discovered_resources(self):
        """
        Gets the should_propagate_tags_to_discovered_resources of this CreateDiscoveryJobDetails.
        If this parameter set to true, the specified tags will be applied
        to all resources discovered in the current request.
        Default is true.


        :return: The should_propagate_tags_to_discovered_resources of this CreateDiscoveryJobDetails.
        :rtype: bool
        """
        return self._should_propagate_tags_to_discovered_resources

    @should_propagate_tags_to_discovered_resources.setter
    def should_propagate_tags_to_discovered_resources(self, should_propagate_tags_to_discovered_resources):
        """
        Sets the should_propagate_tags_to_discovered_resources of this CreateDiscoveryJobDetails.
        If this parameter set to true, the specified tags will be applied
        to all resources discovered in the current request.
        Default is true.


        :param should_propagate_tags_to_discovered_resources: The should_propagate_tags_to_discovered_resources of this CreateDiscoveryJobDetails.
        :type: bool
        """
        self._should_propagate_tags_to_discovered_resources = should_propagate_tags_to_discovered_resources

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateDiscoveryJobDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateDiscoveryJobDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateDiscoveryJobDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateDiscoveryJobDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateDiscoveryJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateDiscoveryJobDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateDiscoveryJobDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateDiscoveryJobDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
