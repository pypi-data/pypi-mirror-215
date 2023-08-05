# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class IdentityProviderJitUserProvGroupMappings(object):
    """
    The list of mappings between the Identity Domain Group and the IDP group.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new IdentityProviderJitUserProvGroupMappings object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this IdentityProviderJitUserProvGroupMappings.
        :type value: str

        :param ref:
            The value to assign to the ref property of this IdentityProviderJitUserProvGroupMappings.
        :type ref: str

        :param idp_group:
            The value to assign to the idp_group property of this IdentityProviderJitUserProvGroupMappings.
        :type idp_group: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'idp_group': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'idp_group': 'idpGroup'
        }

        self._value = None
        self._ref = None
        self._idp_group = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this IdentityProviderJitUserProvGroupMappings.
        Domain Group

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readWrite
         - required: true
         - idcsSearchable: true
         - type: string


        :return: The value of this IdentityProviderJitUserProvGroupMappings.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this IdentityProviderJitUserProvGroupMappings.
        Domain Group

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readWrite
         - required: true
         - idcsSearchable: true
         - type: string


        :param value: The value of this IdentityProviderJitUserProvGroupMappings.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        **[Required]** Gets the ref of this IdentityProviderJitUserProvGroupMappings.
        Group URI

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: reference


        :return: The ref of this IdentityProviderJitUserProvGroupMappings.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this IdentityProviderJitUserProvGroupMappings.
        Group URI

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: default
         - type: reference


        :param ref: The ref of this IdentityProviderJitUserProvGroupMappings.
        :type: str
        """
        self._ref = ref

    @property
    def idp_group(self):
        """
        **[Required]** Gets the idp_group of this IdentityProviderJitUserProvGroupMappings.
        IDP Group Name

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - type: string


        :return: The idp_group of this IdentityProviderJitUserProvGroupMappings.
        :rtype: str
        """
        return self._idp_group

    @idp_group.setter
    def idp_group(self, idp_group):
        """
        Sets the idp_group of this IdentityProviderJitUserProvGroupMappings.
        IDP Group Name

        **Added In:** 2205120021

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - type: string


        :param idp_group: The idp_group of this IdentityProviderJitUserProvGroupMappings.
        :type: str
        """
        self._idp_group = idp_group

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
