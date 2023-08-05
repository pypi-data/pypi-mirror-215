# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateUnifiedAgentConfigurationDetails(object):
    """
    Update Object for the Unified Agent configuration.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateUnifiedAgentConfigurationDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateUnifiedAgentConfigurationDetails.
        :type display_name: str

        :param is_enabled:
            The value to assign to the is_enabled property of this UpdateUnifiedAgentConfigurationDetails.
        :type is_enabled: bool

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateUnifiedAgentConfigurationDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateUnifiedAgentConfigurationDetails.
        :type freeform_tags: dict(str, str)

        :param description:
            The value to assign to the description property of this UpdateUnifiedAgentConfigurationDetails.
        :type description: str

        :param service_configuration:
            The value to assign to the service_configuration property of this UpdateUnifiedAgentConfigurationDetails.
        :type service_configuration: oci.logging.models.UnifiedAgentServiceConfigurationDetails

        :param group_association:
            The value to assign to the group_association property of this UpdateUnifiedAgentConfigurationDetails.
        :type group_association: oci.logging.models.GroupAssociationDetails

        """
        self.swagger_types = {
            'display_name': 'str',
            'is_enabled': 'bool',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)',
            'description': 'str',
            'service_configuration': 'UnifiedAgentServiceConfigurationDetails',
            'group_association': 'GroupAssociationDetails'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'is_enabled': 'isEnabled',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags',
            'description': 'description',
            'service_configuration': 'serviceConfiguration',
            'group_association': 'groupAssociation'
        }

        self._display_name = None
        self._is_enabled = None
        self._defined_tags = None
        self._freeform_tags = None
        self._description = None
        self._service_configuration = None
        self._group_association = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this UpdateUnifiedAgentConfigurationDetails.
        The user-friendly display name. This must be unique within the enclosing resource,
        and it's changeable. Avoid entering confidential information.


        :return: The display_name of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateUnifiedAgentConfigurationDetails.
        The user-friendly display name. This must be unique within the enclosing resource,
        and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this UpdateUnifiedAgentConfigurationDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def is_enabled(self):
        """
        **[Required]** Gets the is_enabled of this UpdateUnifiedAgentConfigurationDetails.
        Whether or not this resource is currently enabled.


        :return: The is_enabled of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: bool
        """
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        """
        Sets the is_enabled of this UpdateUnifiedAgentConfigurationDetails.
        Whether or not this resource is currently enabled.


        :param is_enabled: The is_enabled of this UpdateUnifiedAgentConfigurationDetails.
        :type: bool
        """
        self._is_enabled = is_enabled

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateUnifiedAgentConfigurationDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateUnifiedAgentConfigurationDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateUnifiedAgentConfigurationDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateUnifiedAgentConfigurationDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateUnifiedAgentConfigurationDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateUnifiedAgentConfigurationDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def description(self):
        """
        Gets the description of this UpdateUnifiedAgentConfigurationDetails.
        Description for this resource.


        :return: The description of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateUnifiedAgentConfigurationDetails.
        Description for this resource.


        :param description: The description of this UpdateUnifiedAgentConfigurationDetails.
        :type: str
        """
        self._description = description

    @property
    def service_configuration(self):
        """
        **[Required]** Gets the service_configuration of this UpdateUnifiedAgentConfigurationDetails.

        :return: The service_configuration of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: oci.logging.models.UnifiedAgentServiceConfigurationDetails
        """
        return self._service_configuration

    @service_configuration.setter
    def service_configuration(self, service_configuration):
        """
        Sets the service_configuration of this UpdateUnifiedAgentConfigurationDetails.

        :param service_configuration: The service_configuration of this UpdateUnifiedAgentConfigurationDetails.
        :type: oci.logging.models.UnifiedAgentServiceConfigurationDetails
        """
        self._service_configuration = service_configuration

    @property
    def group_association(self):
        """
        Gets the group_association of this UpdateUnifiedAgentConfigurationDetails.

        :return: The group_association of this UpdateUnifiedAgentConfigurationDetails.
        :rtype: oci.logging.models.GroupAssociationDetails
        """
        return self._group_association

    @group_association.setter
    def group_association(self, group_association):
        """
        Sets the group_association of this UpdateUnifiedAgentConfigurationDetails.

        :param group_association: The group_association of this UpdateUnifiedAgentConfigurationDetails.
        :type: oci.logging.models.GroupAssociationDetails
        """
        self._group_association = group_association

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
