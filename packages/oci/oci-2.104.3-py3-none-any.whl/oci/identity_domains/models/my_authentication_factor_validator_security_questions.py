# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MyAuthenticationFactorValidatorSecurityQuestions(object):
    """
    List of security questions the user has submitted to get authenticated.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MyAuthenticationFactorValidatorSecurityQuestions object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this MyAuthenticationFactorValidatorSecurityQuestions.
        :type id: str

        :param answer:
            The value to assign to the answer property of this MyAuthenticationFactorValidatorSecurityQuestions.
        :type answer: str

        """
        self.swagger_types = {
            'id': 'str',
            'answer': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'answer': 'answer'
        }

        self._id = None
        self._answer = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this MyAuthenticationFactorValidatorSecurityQuestions.
        id of the security question

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :return: The id of this MyAuthenticationFactorValidatorSecurityQuestions.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MyAuthenticationFactorValidatorSecurityQuestions.
        id of the security question

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: true
         - returned: default
         - type: string
         - uniqueness: none


        :param id: The id of this MyAuthenticationFactorValidatorSecurityQuestions.
        :type: str
        """
        self._id = id

    @property
    def answer(self):
        """
        Gets the answer of this MyAuthenticationFactorValidatorSecurityQuestions.
        Answer of the security question the user has submitted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsSensitive: none


        :return: The answer of this MyAuthenticationFactorValidatorSecurityQuestions.
        :rtype: str
        """
        return self._answer

    @answer.setter
    def answer(self, answer):
        """
        Sets the answer of this MyAuthenticationFactorValidatorSecurityQuestions.
        Answer of the security question the user has submitted

        **SCIM++ Properties:**
         - idcsSearchable: false
         - multiValued: false
         - mutability: readWrite
         - required: false
         - returned: default
         - type: string
         - uniqueness: none
         - idcsSensitive: none


        :param answer: The answer of this MyAuthenticationFactorValidatorSecurityQuestions.
        :type: str
        """
        self._answer = answer

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
