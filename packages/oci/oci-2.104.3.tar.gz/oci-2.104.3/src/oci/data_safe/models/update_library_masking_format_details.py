# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateLibraryMaskingFormatDetails(object):
    """
    Details to update a library masking format. Note that updating the formatEntries attribute replaces all the existing masking format
    entries with the specified format entries.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateLibraryMaskingFormatDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateLibraryMaskingFormatDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this UpdateLibraryMaskingFormatDetails.
        :type description: str

        :param sensitive_type_ids:
            The value to assign to the sensitive_type_ids property of this UpdateLibraryMaskingFormatDetails.
        :type sensitive_type_ids: list[str]

        :param format_entries:
            The value to assign to the format_entries property of this UpdateLibraryMaskingFormatDetails.
        :type format_entries: list[oci.data_safe.models.FormatEntry]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateLibraryMaskingFormatDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateLibraryMaskingFormatDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'description': 'str',
            'sensitive_type_ids': 'list[str]',
            'format_entries': 'list[FormatEntry]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'description': 'description',
            'sensitive_type_ids': 'sensitiveTypeIds',
            'format_entries': 'formatEntries',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._description = None
        self._sensitive_type_ids = None
        self._format_entries = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateLibraryMaskingFormatDetails.
        The display name of the library masking format. The name does not have to be unique, and it's changeable.


        :return: The display_name of this UpdateLibraryMaskingFormatDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateLibraryMaskingFormatDetails.
        The display name of the library masking format. The name does not have to be unique, and it's changeable.


        :param display_name: The display_name of this UpdateLibraryMaskingFormatDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this UpdateLibraryMaskingFormatDetails.
        The description of the library masking format.


        :return: The description of this UpdateLibraryMaskingFormatDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this UpdateLibraryMaskingFormatDetails.
        The description of the library masking format.


        :param description: The description of this UpdateLibraryMaskingFormatDetails.
        :type: str
        """
        self._description = description

    @property
    def sensitive_type_ids(self):
        """
        Gets the sensitive_type_ids of this UpdateLibraryMaskingFormatDetails.
        An array of OCIDs of the sensitive types compatible with the library masking format.


        :return: The sensitive_type_ids of this UpdateLibraryMaskingFormatDetails.
        :rtype: list[str]
        """
        return self._sensitive_type_ids

    @sensitive_type_ids.setter
    def sensitive_type_ids(self, sensitive_type_ids):
        """
        Sets the sensitive_type_ids of this UpdateLibraryMaskingFormatDetails.
        An array of OCIDs of the sensitive types compatible with the library masking format.


        :param sensitive_type_ids: The sensitive_type_ids of this UpdateLibraryMaskingFormatDetails.
        :type: list[str]
        """
        self._sensitive_type_ids = sensitive_type_ids

    @property
    def format_entries(self):
        """
        Gets the format_entries of this UpdateLibraryMaskingFormatDetails.
        An array of format entries. The combined output of all the format entries is used for masking.


        :return: The format_entries of this UpdateLibraryMaskingFormatDetails.
        :rtype: list[oci.data_safe.models.FormatEntry]
        """
        return self._format_entries

    @format_entries.setter
    def format_entries(self, format_entries):
        """
        Sets the format_entries of this UpdateLibraryMaskingFormatDetails.
        An array of format entries. The combined output of all the format entries is used for masking.


        :param format_entries: The format_entries of this UpdateLibraryMaskingFormatDetails.
        :type: list[oci.data_safe.models.FormatEntry]
        """
        self._format_entries = format_entries

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateLibraryMaskingFormatDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateLibraryMaskingFormatDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateLibraryMaskingFormatDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace. For more information, see `Resource Tags`__

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateLibraryMaskingFormatDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateLibraryMaskingFormatDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateLibraryMaskingFormatDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateLibraryMaskingFormatDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace. For more information, see `Resource Tags`__

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateLibraryMaskingFormatDetails.
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
