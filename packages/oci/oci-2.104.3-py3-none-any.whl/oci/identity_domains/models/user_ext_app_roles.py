# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UserExtAppRoles(object):
    """
    A list of all AppRoles to which this User belongs directly, indirectly or implicitly. The User could belong directly because the User is a member of the AppRole, could belong indirectly because the User is a member of a Group that is a member of the AppRole, or could belong implicitly because the AppRole is public.

    **SCIM++ Properties:**
    - idcsCompositeKey: [value]
    - multiValued: true
    - mutability: readOnly
    - required: false
    - returned: request
    - type: complex
    - uniqueness: none
    """

    #: A constant which can be used with the type property of a UserExtAppRoles.
    #: This constant has a value of "direct"
    TYPE_DIRECT = "direct"

    #: A constant which can be used with the type property of a UserExtAppRoles.
    #: This constant has a value of "indirect"
    TYPE_INDIRECT = "indirect"

    #: A constant which can be used with the type property of a UserExtAppRoles.
    #: This constant has a value of "implicit"
    TYPE_IMPLICIT = "implicit"

    def __init__(self, **kwargs):
        """
        Initializes a new UserExtAppRoles object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this UserExtAppRoles.
        :type value: str

        :param ref:
            The value to assign to the ref property of this UserExtAppRoles.
        :type ref: str

        :param display:
            The value to assign to the display property of this UserExtAppRoles.
        :type display: str

        :param type:
            The value to assign to the type property of this UserExtAppRoles.
            Allowed values for this property are: "direct", "indirect", "implicit", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type type: str

        :param app_id:
            The value to assign to the app_id property of this UserExtAppRoles.
        :type app_id: str

        :param app_name:
            The value to assign to the app_name property of this UserExtAppRoles.
        :type app_name: str

        :param admin_role:
            The value to assign to the admin_role property of this UserExtAppRoles.
        :type admin_role: bool

        :param legacy_group_name:
            The value to assign to the legacy_group_name property of this UserExtAppRoles.
        :type legacy_group_name: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'display': 'str',
            'type': 'str',
            'app_id': 'str',
            'app_name': 'str',
            'admin_role': 'bool',
            'legacy_group_name': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'display': 'display',
            'type': 'type',
            'app_id': 'appId',
            'app_name': 'appName',
            'admin_role': 'adminRole',
            'legacy_group_name': 'legacyGroupName'
        }

        self._value = None
        self._ref = None
        self._display = None
        self._type = None
        self._app_id = None
        self._app_name = None
        self._admin_role = None
        self._legacy_group_name = None

    @property
    def value(self):
        """
        **[Required]** Gets the value of this UserExtAppRoles.
        The Id of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :return: The value of this UserExtAppRoles.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this UserExtAppRoles.
        The Id of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: true
         - returned: always
         - type: string
         - uniqueness: none


        :param value: The value of this UserExtAppRoles.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this UserExtAppRoles.
        The URI of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this UserExtAppRoles.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this UserExtAppRoles.
        The URI of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this UserExtAppRoles.
        :type: str
        """
        self._ref = ref

    @property
    def display(self):
        """
        Gets the display of this UserExtAppRoles.
        The display name of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The display of this UserExtAppRoles.
        :rtype: str
        """
        return self._display

    @display.setter
    def display(self, display):
        """
        Sets the display of this UserExtAppRoles.
        The display name of the AppRole assigned to the User.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param display: The display of this UserExtAppRoles.
        :type: str
        """
        self._display = display

    @property
    def type(self):
        """
        Gets the type of this UserExtAppRoles.
        The kind of membership this User has in the AppRole. A value of 'direct' indicates that the User is a member of the AppRole.  A value of  'indirect' indicates that the User is a member of a Group that is a member of the AppRole.  A value of 'implicit' indicates that the AppRole is public.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none

        Allowed values for this property are: "direct", "indirect", "implicit", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The type of this UserExtAppRoles.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this UserExtAppRoles.
        The kind of membership this User has in the AppRole. A value of 'direct' indicates that the User is a member of the AppRole.  A value of  'indirect' indicates that the User is a member of a Group that is a member of the AppRole.  A value of 'implicit' indicates that the AppRole is public.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: request
         - type: string
         - uniqueness: none


        :param type: The type of this UserExtAppRoles.
        :type: str
        """
        allowed_values = ["direct", "indirect", "implicit"]
        if not value_allowed_none_or_none_sentinel(type, allowed_values):
            type = 'UNKNOWN_ENUM_VALUE'
        self._type = type

    @property
    def app_id(self):
        """
        Gets the app_id of this UserExtAppRoles.
        The ID of the App that defines this AppRole.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The app_id of this UserExtAppRoles.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """
        Sets the app_id of this UserExtAppRoles.
        The ID of the App that defines this AppRole.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param app_id: The app_id of this UserExtAppRoles.
        :type: str
        """
        self._app_id = app_id

    @property
    def app_name(self):
        """
        Gets the app_name of this UserExtAppRoles.
        The name (Client ID) of the App that defines this AppRole.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The app_name of this UserExtAppRoles.
        :rtype: str
        """
        return self._app_name

    @app_name.setter
    def app_name(self, app_name):
        """
        Sets the app_name of this UserExtAppRoles.
        The name (Client ID) of the App that defines this AppRole.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param app_name: The app_name of this UserExtAppRoles.
        :type: str
        """
        self._app_name = app_name

    @property
    def admin_role(self):
        """
        Gets the admin_role of this UserExtAppRoles.
        If true, then the role provides administrative access privileges. READ-ONLY.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :return: The admin_role of this UserExtAppRoles.
        :rtype: bool
        """
        return self._admin_role

    @admin_role.setter
    def admin_role(self, admin_role):
        """
        Sets the admin_role of this UserExtAppRoles.
        If true, then the role provides administrative access privileges. READ-ONLY.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: boolean
         - uniqueness: none


        :param admin_role: The admin_role of this UserExtAppRoles.
        :type: bool
        """
        self._admin_role = admin_role

    @property
    def legacy_group_name(self):
        """
        Gets the legacy_group_name of this UserExtAppRoles.
        The name (if any) under which this AppRole should appear in this User's group-memberships for reasons of backward compatibility. OCI IAM distinguishes between Groups and AppRoles, but some services still expect AppRoles appear as if they were service-instance-specific Groups.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The legacy_group_name of this UserExtAppRoles.
        :rtype: str
        """
        return self._legacy_group_name

    @legacy_group_name.setter
    def legacy_group_name(self, legacy_group_name):
        """
        Sets the legacy_group_name of this UserExtAppRoles.
        The name (if any) under which this AppRole should appear in this User's group-memberships for reasons of backward compatibility. OCI IAM distinguishes between Groups and AppRoles, but some services still expect AppRoles appear as if they were service-instance-specific Groups.

        **SCIM++ Properties:**
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param legacy_group_name: The legacy_group_name of this UserExtAppRoles.
        :type: str
        """
        self._legacy_group_name = legacy_group_name

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
