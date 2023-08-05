# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_source_details import CreateSourceDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateObjectStorageSourceDetails(CreateSourceDetails):
    """
    Object Storage Source Details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateObjectStorageSourceDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.data_labeling_service_dataplane.models.CreateObjectStorageSourceDetails.source_type` attribute
        of this class is ``OBJECT_STORAGE`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param source_type:
            The value to assign to the source_type property of this CreateObjectStorageSourceDetails.
            Allowed values for this property are: "OBJECT_STORAGE"
        :type source_type: str

        :param relative_path:
            The value to assign to the relative_path property of this CreateObjectStorageSourceDetails.
        :type relative_path: str

        :param offset:
            The value to assign to the offset property of this CreateObjectStorageSourceDetails.
        :type offset: float

        :param length:
            The value to assign to the length property of this CreateObjectStorageSourceDetails.
        :type length: float

        """
        self.swagger_types = {
            'source_type': 'str',
            'relative_path': 'str',
            'offset': 'float',
            'length': 'float'
        }

        self.attribute_map = {
            'source_type': 'sourceType',
            'relative_path': 'relativePath',
            'offset': 'offset',
            'length': 'length'
        }

        self._source_type = None
        self._relative_path = None
        self._offset = None
        self._length = None
        self._source_type = 'OBJECT_STORAGE'

    @property
    def relative_path(self):
        """
        **[Required]** Gets the relative_path of this CreateObjectStorageSourceDetails.
        The path relative to the prefix specified in the dataset source details (file name).


        :return: The relative_path of this CreateObjectStorageSourceDetails.
        :rtype: str
        """
        return self._relative_path

    @relative_path.setter
    def relative_path(self, relative_path):
        """
        Sets the relative_path of this CreateObjectStorageSourceDetails.
        The path relative to the prefix specified in the dataset source details (file name).


        :param relative_path: The relative_path of this CreateObjectStorageSourceDetails.
        :type: str
        """
        self._relative_path = relative_path

    @property
    def offset(self):
        """
        Gets the offset of this CreateObjectStorageSourceDetails.
        The offset into the file containing the content.


        :return: The offset of this CreateObjectStorageSourceDetails.
        :rtype: float
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """
        Sets the offset of this CreateObjectStorageSourceDetails.
        The offset into the file containing the content.


        :param offset: The offset of this CreateObjectStorageSourceDetails.
        :type: float
        """
        self._offset = offset

    @property
    def length(self):
        """
        Gets the length of this CreateObjectStorageSourceDetails.
        The length from offset into the file containing the content.


        :return: The length of this CreateObjectStorageSourceDetails.
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """
        Sets the length of this CreateObjectStorageSourceDetails.
        The length from offset into the file containing the content.


        :param length: The length of this CreateObjectStorageSourceDetails.
        :type: float
        """
        self._length = length

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
