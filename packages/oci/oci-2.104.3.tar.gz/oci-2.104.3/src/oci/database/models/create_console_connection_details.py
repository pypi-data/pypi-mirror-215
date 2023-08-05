# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateConsoleConnectionDetails(object):
    """
    The details for creating a Db node console connection.
    The Db node console connection is created in the same compartment as the dbNode.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateConsoleConnectionDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param public_key:
            The value to assign to the public_key property of this CreateConsoleConnectionDetails.
        :type public_key: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateConsoleConnectionDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateConsoleConnectionDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'public_key': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'public_key': 'publicKey',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._public_key = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def public_key(self):
        """
        **[Required]** Gets the public_key of this CreateConsoleConnectionDetails.
        The SSH public key used to authenticate the console connection.


        :return: The public_key of this CreateConsoleConnectionDetails.
        :rtype: str
        """
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        """
        Sets the public_key of this CreateConsoleConnectionDetails.
        The SSH public key used to authenticate the console connection.


        :param public_key: The public_key of this CreateConsoleConnectionDetails.
        :type: str
        """
        self._public_key = public_key

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateConsoleConnectionDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateConsoleConnectionDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateConsoleConnectionDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateConsoleConnectionDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateConsoleConnectionDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateConsoleConnectionDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateConsoleConnectionDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateConsoleConnectionDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
