# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .function_source_details import FunctionSourceDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PreBuiltFunctionSourceDetails(FunctionSourceDetails):
    """
    The source of the Function which is based on a Pre-Built Function Listing (PbfListing).
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PreBuiltFunctionSourceDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.functions.models.PreBuiltFunctionSourceDetails.source_type` attribute
        of this class is ``PRE_BUILT_FUNCTIONS`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_type:
            The value to assign to the source_type property of this PreBuiltFunctionSourceDetails.
            Allowed values for this property are: "PRE_BUILT_FUNCTIONS"
        :type source_type: str

        :param pbf_listing_id:
            The value to assign to the pbf_listing_id property of this PreBuiltFunctionSourceDetails.
        :type pbf_listing_id: str

        """
        self.swagger_types = {
            'source_type': 'str',
            'pbf_listing_id': 'str'
        }

        self.attribute_map = {
            'source_type': 'sourceType',
            'pbf_listing_id': 'pbfListingId'
        }

        self._source_type = None
        self._pbf_listing_id = None
        self._source_type = 'PRE_BUILT_FUNCTIONS'

    @property
    def pbf_listing_id(self):
        """
        **[Required]** Gets the pbf_listing_id of this PreBuiltFunctionSourceDetails.
        The `OCID`__ of the PbfListing this
        function is sourced from.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The pbf_listing_id of this PreBuiltFunctionSourceDetails.
        :rtype: str
        """
        return self._pbf_listing_id

    @pbf_listing_id.setter
    def pbf_listing_id(self, pbf_listing_id):
        """
        Sets the pbf_listing_id of this PreBuiltFunctionSourceDetails.
        The `OCID`__ of the PbfListing this
        function is sourced from.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param pbf_listing_id: The pbf_listing_id of this PreBuiltFunctionSourceDetails.
        :type: str
        """
        self._pbf_listing_id = pbf_listing_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
