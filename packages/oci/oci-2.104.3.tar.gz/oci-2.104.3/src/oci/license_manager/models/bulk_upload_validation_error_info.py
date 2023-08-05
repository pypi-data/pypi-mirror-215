# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class BulkUploadValidationErrorInfo(object):
    """
    Detailed error information corresponding to each column for a particular supported license record that could not be uploaded.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new BulkUploadValidationErrorInfo object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param row_number:
            The value to assign to the row_number property of this BulkUploadValidationErrorInfo.
        :type row_number: int

        :param product_name:
            The value to assign to the product_name property of this BulkUploadValidationErrorInfo.
        :type product_name: str

        :param row_error:
            The value to assign to the row_error property of this BulkUploadValidationErrorInfo.
        :type row_error: list[oci.license_manager.models.BulkUploadCellInfo]

        """
        self.swagger_types = {
            'row_number': 'int',
            'product_name': 'str',
            'row_error': 'list[BulkUploadCellInfo]'
        }

        self.attribute_map = {
            'row_number': 'rowNumber',
            'product_name': 'productName',
            'row_error': 'rowError'
        }

        self._row_number = None
        self._product_name = None
        self._row_error = None

    @property
    def row_number(self):
        """
        **[Required]** Gets the row_number of this BulkUploadValidationErrorInfo.
        Refers to the license record number as provided in the bulk upload file.


        :return: The row_number of this BulkUploadValidationErrorInfo.
        :rtype: int
        """
        return self._row_number

    @row_number.setter
    def row_number(self, row_number):
        """
        Sets the row_number of this BulkUploadValidationErrorInfo.
        Refers to the license record number as provided in the bulk upload file.


        :param row_number: The row_number of this BulkUploadValidationErrorInfo.
        :type: int
        """
        self._row_number = row_number

    @property
    def product_name(self):
        """
        **[Required]** Gets the product_name of this BulkUploadValidationErrorInfo.
        Product name of invalid row.


        :return: The product_name of this BulkUploadValidationErrorInfo.
        :rtype: str
        """
        return self._product_name

    @product_name.setter
    def product_name(self, product_name):
        """
        Sets the product_name of this BulkUploadValidationErrorInfo.
        Product name of invalid row.


        :param product_name: The product_name of this BulkUploadValidationErrorInfo.
        :type: str
        """
        self._product_name = product_name

    @property
    def row_error(self):
        """
        **[Required]** Gets the row_error of this BulkUploadValidationErrorInfo.
        Error information corresponding to each column.


        :return: The row_error of this BulkUploadValidationErrorInfo.
        :rtype: list[oci.license_manager.models.BulkUploadCellInfo]
        """
        return self._row_error

    @row_error.setter
    def row_error(self, row_error):
        """
        Sets the row_error of this BulkUploadValidationErrorInfo.
        Error information corresponding to each column.


        :param row_error: The row_error of this BulkUploadValidationErrorInfo.
        :type: list[oci.license_manager.models.BulkUploadCellInfo]
        """
        self._row_error = row_error

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
