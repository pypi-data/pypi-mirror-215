# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AccessibleCompartmentResponse(object):
    """
    AccessibleCompartmentResponse model.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AccessibleCompartmentResponse object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartments_metadata:
            The value to assign to the compartments_metadata property of this AccessibleCompartmentResponse.
        :type compartments_metadata: list[oci.identity_data_plane.models.CompartmentMetadata]

        """
        self.swagger_types = {
            'compartments_metadata': 'list[CompartmentMetadata]'
        }

        self.attribute_map = {
            'compartments_metadata': 'compartmentsMetadata'
        }

        self._compartments_metadata = None

    @property
    def compartments_metadata(self):
        """
        **[Required]** Gets the compartments_metadata of this AccessibleCompartmentResponse.
        The compartments metadata.


        :return: The compartments_metadata of this AccessibleCompartmentResponse.
        :rtype: list[oci.identity_data_plane.models.CompartmentMetadata]
        """
        return self._compartments_metadata

    @compartments_metadata.setter
    def compartments_metadata(self, compartments_metadata):
        """
        Sets the compartments_metadata of this AccessibleCompartmentResponse.
        The compartments metadata.


        :param compartments_metadata: The compartments_metadata of this AccessibleCompartmentResponse.
        :type: list[oci.identity_data_plane.models.CompartmentMetadata]
        """
        self._compartments_metadata = compartments_metadata

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
