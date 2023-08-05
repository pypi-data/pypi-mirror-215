# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .format_entry import FormatEntry
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class LibraryMaskingFormatEntry(FormatEntry):
    """
    A library masking format to be used for masking. It can be either a
    predefined or a user-defined library masking format. It enables reuse
    of an existing library masking format and helps avoid defining the masking
    logic again. Use the ListLibraryMaskingFormats operation to view the
    existing library masking formats.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new LibraryMaskingFormatEntry object with values from keyword arguments. The default value of the :py:attr:`~oci.data_safe.models.LibraryMaskingFormatEntry.type` attribute
        of this class is ``LIBRARY_MASKING_FORMAT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this LibraryMaskingFormatEntry.
            Allowed values for this property are: "DELETE_ROWS", "DETERMINISTIC_SUBSTITUTION", "DETERMINISTIC_ENCRYPTION", "DETERMINISTIC_ENCRYPTION_DATE", "FIXED_NUMBER", "FIXED_STRING", "LIBRARY_MASKING_FORMAT", "NULL_VALUE", "POST_PROCESSING_FUNCTION", "PRESERVE_ORIGINAL_DATA", "RANDOM_DATE", "RANDOM_DECIMAL_NUMBER", "RANDOM_DIGITS", "RANDOM_LIST", "RANDOM_NUMBER", "RANDOM_STRING", "RANDOM_SUBSTITUTION", "REGULAR_EXPRESSION", "SHUFFLE", "SQL_EXPRESSION", "SUBSTRING", "TRUNCATE_TABLE", "USER_DEFINED_FUNCTION"
        :type type: str

        :param description:
            The value to assign to the description property of this LibraryMaskingFormatEntry.
        :type description: str

        :param library_masking_format_id:
            The value to assign to the library_masking_format_id property of this LibraryMaskingFormatEntry.
        :type library_masking_format_id: str

        """
        self.swagger_types = {
            'type': 'str',
            'description': 'str',
            'library_masking_format_id': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'description': 'description',
            'library_masking_format_id': 'libraryMaskingFormatId'
        }

        self._type = None
        self._description = None
        self._library_masking_format_id = None
        self._type = 'LIBRARY_MASKING_FORMAT'

    @property
    def library_masking_format_id(self):
        """
        **[Required]** Gets the library_masking_format_id of this LibraryMaskingFormatEntry.
        The OCID of the library masking format.


        :return: The library_masking_format_id of this LibraryMaskingFormatEntry.
        :rtype: str
        """
        return self._library_masking_format_id

    @library_masking_format_id.setter
    def library_masking_format_id(self, library_masking_format_id):
        """
        Sets the library_masking_format_id of this LibraryMaskingFormatEntry.
        The OCID of the library masking format.


        :param library_masking_format_id: The library_masking_format_id of this LibraryMaskingFormatEntry.
        :type: str
        """
        self._library_masking_format_id = library_masking_format_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
