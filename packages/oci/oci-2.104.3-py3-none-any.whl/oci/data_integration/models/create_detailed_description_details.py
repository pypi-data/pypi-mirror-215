# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDetailedDescriptionDetails(object):
    """
    Properties used in detailed description create operations.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDetailedDescriptionDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param logo:
            The value to assign to the logo property of this CreateDetailedDescriptionDetails.
        :type logo: str

        :param detailed_description:
            The value to assign to the detailed_description property of this CreateDetailedDescriptionDetails.
        :type detailed_description: str

        """
        self.swagger_types = {
            'logo': 'str',
            'detailed_description': 'str'
        }

        self.attribute_map = {
            'logo': 'logo',
            'detailed_description': 'detailedDescription'
        }

        self._logo = None
        self._detailed_description = None

    @property
    def logo(self):
        """
        Gets the logo of this CreateDetailedDescriptionDetails.
        Base64 encoded image to represent logo of the object.


        :return: The logo of this CreateDetailedDescriptionDetails.
        :rtype: str
        """
        return self._logo

    @logo.setter
    def logo(self, logo):
        """
        Sets the logo of this CreateDetailedDescriptionDetails.
        Base64 encoded image to represent logo of the object.


        :param logo: The logo of this CreateDetailedDescriptionDetails.
        :type: str
        """
        self._logo = logo

    @property
    def detailed_description(self):
        """
        Gets the detailed_description of this CreateDetailedDescriptionDetails.
        Base64 encoded rich text description of the object.


        :return: The detailed_description of this CreateDetailedDescriptionDetails.
        :rtype: str
        """
        return self._detailed_description

    @detailed_description.setter
    def detailed_description(self, detailed_description):
        """
        Sets the detailed_description of this CreateDetailedDescriptionDetails.
        Base64 encoded rich text description of the object.


        :param detailed_description: The detailed_description of this CreateDetailedDescriptionDetails.
        :type: str
        """
        self._detailed_description = detailed_description

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
