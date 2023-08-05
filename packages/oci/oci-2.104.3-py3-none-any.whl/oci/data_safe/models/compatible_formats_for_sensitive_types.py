# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CompatibleFormatsForSensitiveTypes(object):
    """
    The list of compatible masking formats grouped by generic sensitive types.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CompatibleFormatsForSensitiveTypes object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param formats_for_sensitive_type:
            The value to assign to the formats_for_sensitive_type property of this CompatibleFormatsForSensitiveTypes.
        :type formats_for_sensitive_type: list[oci.data_safe.models.FormatsForSensitiveType]

        """
        self.swagger_types = {
            'formats_for_sensitive_type': 'list[FormatsForSensitiveType]'
        }

        self.attribute_map = {
            'formats_for_sensitive_type': 'formatsForSensitiveType'
        }

        self._formats_for_sensitive_type = None

    @property
    def formats_for_sensitive_type(self):
        """
        **[Required]** Gets the formats_for_sensitive_type of this CompatibleFormatsForSensitiveTypes.
        An array of library masking formats compatible with the existing sensitive types.


        :return: The formats_for_sensitive_type of this CompatibleFormatsForSensitiveTypes.
        :rtype: list[oci.data_safe.models.FormatsForSensitiveType]
        """
        return self._formats_for_sensitive_type

    @formats_for_sensitive_type.setter
    def formats_for_sensitive_type(self, formats_for_sensitive_type):
        """
        Sets the formats_for_sensitive_type of this CompatibleFormatsForSensitiveTypes.
        An array of library masking formats compatible with the existing sensitive types.


        :param formats_for_sensitive_type: The formats_for_sensitive_type of this CompatibleFormatsForSensitiveTypes.
        :type: list[oci.data_safe.models.FormatsForSensitiveType]
        """
        self._formats_for_sensitive_type = formats_for_sensitive_type

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
