# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .update_opsi_configuration_details import UpdateOpsiConfigurationDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateOpsiUxConfigurationDetails(UpdateOpsiConfigurationDetails):
    """
    Information to be updated in OPSI UX configuration.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateOpsiUxConfigurationDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.opsi.models.UpdateOpsiUxConfigurationDetails.opsi_config_type` attribute
        of this class is ``UX_CONFIGURATION`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param opsi_config_type:
            The value to assign to the opsi_config_type property of this UpdateOpsiUxConfigurationDetails.
            Allowed values for this property are: "UX_CONFIGURATION"
        :type opsi_config_type: str

        :param display_name:
            The value to assign to the display_name property of this UpdateOpsiUxConfigurationDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateOpsiUxConfigurationDetails.
        :type description: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateOpsiUxConfigurationDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateOpsiUxConfigurationDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param system_tags:
            The value to assign to the system_tags property of this UpdateOpsiUxConfigurationDetails.
        :type system_tags: dict(str, dict(str, object))

        :param config_items:
            The value to assign to the config_items property of this UpdateOpsiUxConfigurationDetails.
        :type config_items: list[oci.opsi.models.UpdateConfigurationItemDetails]

        """
        self.swagger_types = {
            'opsi_config_type': 'str',
            'display_name': 'str',
            'description': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'system_tags': 'dict(str, dict(str, object))',
            'config_items': 'list[UpdateConfigurationItemDetails]'
        }

        self.attribute_map = {
            'opsi_config_type': 'opsiConfigType',
            'display_name': 'displayName',
            'description': 'description',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'system_tags': 'systemTags',
            'config_items': 'configItems'
        }

        self._opsi_config_type = None
        self._display_name = None
        self._description = None
        self._freeform_tags = None
        self._defined_tags = None
        self._system_tags = None
        self._config_items = None
        self._opsi_config_type = 'UX_CONFIGURATION'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
