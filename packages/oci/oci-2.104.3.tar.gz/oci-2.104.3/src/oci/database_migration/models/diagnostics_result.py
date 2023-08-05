# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DiagnosticsResult(object):
    """
    Result from Database Connection Diagnostic action.
    """

    #: A constant which can be used with the result_type property of a DiagnosticsResult.
    #: This constant has a value of "SUCCEEDED"
    RESULT_TYPE_SUCCEEDED = "SUCCEEDED"

    #: A constant which can be used with the result_type property of a DiagnosticsResult.
    #: This constant has a value of "FAILED"
    RESULT_TYPE_FAILED = "FAILED"

    #: A constant which can be used with the result_type property of a DiagnosticsResult.
    #: This constant has a value of "TIMED_OUT"
    RESULT_TYPE_TIMED_OUT = "TIMED_OUT"

    def __init__(self, **kwargs):
        """
        Initializes a new DiagnosticsResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param result_type:
            The value to assign to the result_type property of this DiagnosticsResult.
            Allowed values for this property are: "SUCCEEDED", "FAILED", "TIMED_OUT", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type result_type: str

        :param error:
            The value to assign to the error property of this DiagnosticsResult.
        :type error: oci.database_migration.models.ResultError

        """
        self.swagger_types = {
            'result_type': 'str',
            'error': 'ResultError'
        }

        self.attribute_map = {
            'result_type': 'resultType',
            'error': 'error'
        }

        self._result_type = None
        self._error = None

    @property
    def result_type(self):
        """
        **[Required]** Gets the result_type of this DiagnosticsResult.
        Type of the Result (i.e. Success or Failure).

        Allowed values for this property are: "SUCCEEDED", "FAILED", "TIMED_OUT", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The result_type of this DiagnosticsResult.
        :rtype: str
        """
        return self._result_type

    @result_type.setter
    def result_type(self, result_type):
        """
        Sets the result_type of this DiagnosticsResult.
        Type of the Result (i.e. Success or Failure).


        :param result_type: The result_type of this DiagnosticsResult.
        :type: str
        """
        allowed_values = ["SUCCEEDED", "FAILED", "TIMED_OUT"]
        if not value_allowed_none_or_none_sentinel(result_type, allowed_values):
            result_type = 'UNKNOWN_ENUM_VALUE'
        self._result_type = result_type

    @property
    def error(self):
        """
        Gets the error of this DiagnosticsResult.

        :return: The error of this DiagnosticsResult.
        :rtype: oci.database_migration.models.ResultError
        """
        return self._error

    @error.setter
    def error(self, error):
        """
        Sets the error of this DiagnosticsResult.

        :param error: The error of this DiagnosticsResult.
        :type: oci.database_migration.models.ResultError
        """
        self._error = error

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
