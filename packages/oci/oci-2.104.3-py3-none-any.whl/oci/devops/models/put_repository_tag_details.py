# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .put_repository_ref_details import PutRepositoryRefDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PutRepositoryTagDetails(PutRepositoryRefDetails):
    """
    The information needed to create a lightweight tag.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PutRepositoryTagDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.devops.models.PutRepositoryTagDetails.ref_type` attribute
        of this class is ``TAG`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param ref_type:
            The value to assign to the ref_type property of this PutRepositoryTagDetails.
            Allowed values for this property are: "BRANCH", "TAG"
        :type ref_type: str

        :param object_id:
            The value to assign to the object_id property of this PutRepositoryTagDetails.
        :type object_id: str

        """
        self.swagger_types = {
            'ref_type': 'str',
            'object_id': 'str'
        }

        self.attribute_map = {
            'ref_type': 'refType',
            'object_id': 'objectId'
        }

        self._ref_type = None
        self._object_id = None
        self._ref_type = 'TAG'

    @property
    def object_id(self):
        """
        **[Required]** Gets the object_id of this PutRepositoryTagDetails.
        SHA-1 hash value of the object pointed to by the tag.


        :return: The object_id of this PutRepositoryTagDetails.
        :rtype: str
        """
        return self._object_id

    @object_id.setter
    def object_id(self, object_id):
        """
        Sets the object_id of this PutRepositoryTagDetails.
        SHA-1 hash value of the object pointed to by the tag.


        :param object_id: The object_id of this PutRepositoryTagDetails.
        :type: str
        """
        self._object_id = object_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
