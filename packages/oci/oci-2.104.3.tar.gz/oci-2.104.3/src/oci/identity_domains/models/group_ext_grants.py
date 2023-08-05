# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class GroupExtGrants(object):
    """
    Grants assigned to group

    **SCIM++ Properties:**
    - idcsSearchable: true
    - multiValued: true
    - mutability: readOnly
    - required: false
    - returned: request
    - type: complex
    - uniqueness: none
    """

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "IMPORT_APPROLE_MEMBERS"
    GRANT_MECHANISM_IMPORT_APPROLE_MEMBERS = "IMPORT_APPROLE_MEMBERS"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "ADMINISTRATOR_TO_USER"
    GRANT_MECHANISM_ADMINISTRATOR_TO_USER = "ADMINISTRATOR_TO_USER"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "ADMINISTRATOR_TO_GROUP"
    GRANT_MECHANISM_ADMINISTRATOR_TO_GROUP = "ADMINISTRATOR_TO_GROUP"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "SERVICE_MANAGER_TO_USER"
    GRANT_MECHANISM_SERVICE_MANAGER_TO_USER = "SERVICE_MANAGER_TO_USER"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "ADMINISTRATOR_TO_APP"
    GRANT_MECHANISM_ADMINISTRATOR_TO_APP = "ADMINISTRATOR_TO_APP"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "SERVICE_MANAGER_TO_APP"
    GRANT_MECHANISM_SERVICE_MANAGER_TO_APP = "SERVICE_MANAGER_TO_APP"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "OPC_INFRA_TO_APP"
    GRANT_MECHANISM_OPC_INFRA_TO_APP = "OPC_INFRA_TO_APP"

    #: A constant which can be used with the grant_mechanism property of a GroupExtGrants.
    #: This constant has a value of "GROUP_MEMBERSHIP"
    GRANT_MECHANISM_GROUP_MEMBERSHIP = "GROUP_MEMBERSHIP"

    def __init__(self, **kwargs):
        """
        Initializes a new GroupExtGrants object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param value:
            The value to assign to the value property of this GroupExtGrants.
        :type value: str

        :param ref:
            The value to assign to the ref property of this GroupExtGrants.
        :type ref: str

        :param app_id:
            The value to assign to the app_id property of this GroupExtGrants.
        :type app_id: str

        :param grant_mechanism:
            The value to assign to the grant_mechanism property of this GroupExtGrants.
            Allowed values for this property are: "IMPORT_APPROLE_MEMBERS", "ADMINISTRATOR_TO_USER", "ADMINISTRATOR_TO_GROUP", "SERVICE_MANAGER_TO_USER", "ADMINISTRATOR_TO_APP", "SERVICE_MANAGER_TO_APP", "OPC_INFRA_TO_APP", "GROUP_MEMBERSHIP", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type grant_mechanism: str

        """
        self.swagger_types = {
            'value': 'str',
            'ref': 'str',
            'app_id': 'str',
            'grant_mechanism': 'str'
        }

        self.attribute_map = {
            'value': 'value',
            'ref': '$ref',
            'app_id': 'appId',
            'grant_mechanism': 'grantMechanism'
        }

        self._value = None
        self._ref = None
        self._app_id = None
        self._grant_mechanism = None

    @property
    def value(self):
        """
        Gets the value of this GroupExtGrants.
        Grant identifier

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The value of this GroupExtGrants.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this GroupExtGrants.
        Grant identifier

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param value: The value of this GroupExtGrants.
        :type: str
        """
        self._value = value

    @property
    def ref(self):
        """
        Gets the ref of this GroupExtGrants.
        Grant URI

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :return: The ref of this GroupExtGrants.
        :rtype: str
        """
        return self._ref

    @ref.setter
    def ref(self, ref):
        """
        Sets the ref of this GroupExtGrants.
        Grant URI

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: reference
         - uniqueness: none


        :param ref: The ref of this GroupExtGrants.
        :type: str
        """
        self._ref = ref

    @property
    def app_id(self):
        """
        Gets the app_id of this GroupExtGrants.
        App identifier

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :return: The app_id of this GroupExtGrants.
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """
        Sets the app_id of this GroupExtGrants.
        App identifier

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param app_id: The app_id of this GroupExtGrants.
        :type: str
        """
        self._app_id = app_id

    @property
    def grant_mechanism(self):
        """
        Gets the grant_mechanism of this GroupExtGrants.
        Each value of grantMechanism indicates how (or by what component) some App (or App-Entitlement) was granted.\
        A customer or the UI should use only grantMechanism values that start with 'ADMINISTRATOR':\
         - 'ADMINISTRATOR_TO_USER' is for a direct grant to a specific User.\
         - 'ADMINISTRATOR_TO_GROUP' is for a grant to a specific Group, which results in indirect grants to Users who are members of that Group.\
         - 'ADMINISTRATOR_TO_APP' is for a grant to a specific App.  The grantee (client) App gains access to the granted (server) App.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none

        Allowed values for this property are: "IMPORT_APPROLE_MEMBERS", "ADMINISTRATOR_TO_USER", "ADMINISTRATOR_TO_GROUP", "SERVICE_MANAGER_TO_USER", "ADMINISTRATOR_TO_APP", "SERVICE_MANAGER_TO_APP", "OPC_INFRA_TO_APP", "GROUP_MEMBERSHIP", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The grant_mechanism of this GroupExtGrants.
        :rtype: str
        """
        return self._grant_mechanism

    @grant_mechanism.setter
    def grant_mechanism(self, grant_mechanism):
        """
        Sets the grant_mechanism of this GroupExtGrants.
        Each value of grantMechanism indicates how (or by what component) some App (or App-Entitlement) was granted.\
        A customer or the UI should use only grantMechanism values that start with 'ADMINISTRATOR':\
         - 'ADMINISTRATOR_TO_USER' is for a direct grant to a specific User.\
         - 'ADMINISTRATOR_TO_GROUP' is for a grant to a specific Group, which results in indirect grants to Users who are members of that Group.\
         - 'ADMINISTRATOR_TO_APP' is for a grant to a specific App.  The grantee (client) App gains access to the granted (server) App.

        **SCIM++ Properties:**
         - caseExact: true
         - idcsSearchable: true
         - multiValued: false
         - mutability: readOnly
         - required: false
         - returned: default
         - type: string
         - uniqueness: none


        :param grant_mechanism: The grant_mechanism of this GroupExtGrants.
        :type: str
        """
        allowed_values = ["IMPORT_APPROLE_MEMBERS", "ADMINISTRATOR_TO_USER", "ADMINISTRATOR_TO_GROUP", "SERVICE_MANAGER_TO_USER", "ADMINISTRATOR_TO_APP", "SERVICE_MANAGER_TO_APP", "OPC_INFRA_TO_APP", "GROUP_MEMBERSHIP"]
        if not value_allowed_none_or_none_sentinel(grant_mechanism, allowed_values):
            grant_mechanism = 'UNKNOWN_ENUM_VALUE'
        self._grant_mechanism = grant_mechanism

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
