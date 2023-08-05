# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .action import Action
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CheckAction(Action):
    """
    An object that represents an action which does not stop the execution of rules in current module,
    just emits a log message documenting result of rule execution.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CheckAction object with values from keyword arguments. The default value of the :py:attr:`~oci.waf.models.CheckAction.type` attribute
        of this class is ``CHECK`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this CheckAction.
            Allowed values for this property are: "CHECK", "ALLOW", "RETURN_HTTP_RESPONSE"
        :type type: str

        :param name:
            The value to assign to the name property of this CheckAction.
        :type name: str

        """
        self.swagger_types = {
            'type': 'str',
            'name': 'str'
        }

        self.attribute_map = {
            'type': 'type',
            'name': 'name'
        }

        self._type = None
        self._name = None
        self._type = 'CHECK'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
