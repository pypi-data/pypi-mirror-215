# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ActivateTargetDatabaseDetails(object):
    """
    The details required to reactivate a previously deactived target database in Data Safe.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ActivateTargetDatabaseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param credentials:
            The value to assign to the credentials property of this ActivateTargetDatabaseDetails.
        :type credentials: oci.data_safe.models.Credentials

        """
        self.swagger_types = {
            'credentials': 'Credentials'
        }

        self.attribute_map = {
            'credentials': 'credentials'
        }

        self._credentials = None

    @property
    def credentials(self):
        """
        **[Required]** Gets the credentials of this ActivateTargetDatabaseDetails.

        :return: The credentials of this ActivateTargetDatabaseDetails.
        :rtype: oci.data_safe.models.Credentials
        """
        return self._credentials

    @credentials.setter
    def credentials(self, credentials):
        """
        Sets the credentials of this ActivateTargetDatabaseDetails.

        :param credentials: The credentials of this ActivateTargetDatabaseDetails.
        :type: oci.data_safe.models.Credentials
        """
        self._credentials = credentials

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
