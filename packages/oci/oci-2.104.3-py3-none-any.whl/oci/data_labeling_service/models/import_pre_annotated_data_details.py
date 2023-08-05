# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ImportPreAnnotatedDataDetails(object):
    """
    Allows user to import dataset labels, records and annotations from dataset files
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ImportPreAnnotatedDataDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param import_format:
            The value to assign to the import_format property of this ImportPreAnnotatedDataDetails.
        :type import_format: oci.data_labeling_service.models.ImportFormat

        :param import_metadata_path:
            The value to assign to the import_metadata_path property of this ImportPreAnnotatedDataDetails.
        :type import_metadata_path: oci.data_labeling_service.models.ImportMetadataPath

        """
        self.swagger_types = {
            'import_format': 'ImportFormat',
            'import_metadata_path': 'ImportMetadataPath'
        }

        self.attribute_map = {
            'import_format': 'importFormat',
            'import_metadata_path': 'importMetadataPath'
        }

        self._import_format = None
        self._import_metadata_path = None

    @property
    def import_format(self):
        """
        Gets the import_format of this ImportPreAnnotatedDataDetails.

        :return: The import_format of this ImportPreAnnotatedDataDetails.
        :rtype: oci.data_labeling_service.models.ImportFormat
        """
        return self._import_format

    @import_format.setter
    def import_format(self, import_format):
        """
        Sets the import_format of this ImportPreAnnotatedDataDetails.

        :param import_format: The import_format of this ImportPreAnnotatedDataDetails.
        :type: oci.data_labeling_service.models.ImportFormat
        """
        self._import_format = import_format

    @property
    def import_metadata_path(self):
        """
        Gets the import_metadata_path of this ImportPreAnnotatedDataDetails.

        :return: The import_metadata_path of this ImportPreAnnotatedDataDetails.
        :rtype: oci.data_labeling_service.models.ImportMetadataPath
        """
        return self._import_metadata_path

    @import_metadata_path.setter
    def import_metadata_path(self, import_metadata_path):
        """
        Sets the import_metadata_path of this ImportPreAnnotatedDataDetails.

        :param import_metadata_path: The import_metadata_path of this ImportPreAnnotatedDataDetails.
        :type: oci.data_labeling_service.models.ImportMetadataPath
        """
        self._import_metadata_path = import_metadata_path

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
