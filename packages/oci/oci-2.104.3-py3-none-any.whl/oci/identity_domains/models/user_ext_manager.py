# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserExtManager(object):
    """
    The User's manager. A complex type that optionally allows Service Providers to represent organizational hierarchy by referencing the 'id' attribute of another User.

    **SCIM++ Properties:**
    - idcsCsvAttributeNameMappings: [[columnHeaderName:Manager, deprecatedColumnHeaderName:Manager Name, mapsTo:manager.value]]
    - idcsPii: true
    - multiValued: false
    - mutability: readWrite
    - required: false
    - returned: default
    - type: complex
    - uniqueness: none
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UserExtManager object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserExtManager.
        :type value: str

        :param ref:
            The value to assign to the ref property of this UserExtManager.
        :type ref: str

        :param display_name:
            The value to assign to the display_name property of this UserExtManager.
        :type display_name: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'display_name': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'display_name': 'displayName'
        }

        self._value = None
        self._ref = None
        self._display_name = None

    @property
    def value(self):
        """
        Gets the value of this UserExtManager.
        The id of the SCIM resource representing  the User's  manager.  RECOMMENDED.

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Manager Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this UserExtManager.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserExtManager.
        The id of the SCIM resource representing  the User's  manager.  RECOMMENDED.

        **SCIM++ Properties:**
         - idcsCsvAttributeName: Manager Name
         - idcsSearchable: true
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this UserExtManager.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this UserExtManager.
        The URI of the SCIM resource representing the User's manager.  RECOMMENDED.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this UserExtManager.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this UserExtManager.
        The URI of the SCIM resource representing the User's manager.  RECOMMENDED.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this UserExtManager.
        :type: str
        """
        self._ref = ref

    @property
    def display_name(self):
        """
        Gets the display_name of this UserExtManager.
        The displayName of the User's manager. OPTIONAL and READ-ONLY.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display_name of this UserExtManager.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UserExtManager.
        The displayName of the User's manager. OPTIONAL and READ-ONLY.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display_name: The display_name of this UserExtManager.
        :type: str
        """
        self._display_name = display_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
