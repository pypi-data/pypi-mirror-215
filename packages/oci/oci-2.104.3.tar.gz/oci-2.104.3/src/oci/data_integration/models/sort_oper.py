# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .operator import Operator
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class SortOper(Operator):
    """
    The information about the sort operator.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new SortOper object with values from keyword arguments. The default value of the :py:attr:`~oci.data_integration.models.SortOper.model_type` attribute
        of this class is ``SORT_OPERATOR`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param model_type:
            The value to assign to the model_type property of this SortOper.
            Allowed values for this property are: "SOURCE_OPERATOR", "FILTER_OPERATOR", "JOINER_OPERATOR", "AGGREGATOR_OPERATOR", "PROJECTION_OPERATOR", "TARGET_OPERATOR", "FLATTEN_OPERATOR", "DISTINCT_OPERATOR", "SORT_OPERATOR", "UNION_OPERATOR", "INTERSECT_OPERATOR", "MINUS_OPERATOR", "MERGE_OPERATOR", "FUNCTION_OPERATOR", "SPLIT_OPERATOR", "START_OPERATOR", "END_OPERATOR", "PIPELINE_OPERATOR", "DECISION_OPERATOR", "TASK_OPERATOR", "EXPRESSION_OPERATOR", "LOOKUP_OPERATOR", "PIVOT_OPERATOR"
        :type model_type: str

        :param key:
            The value to assign to the key property of this SortOper.
        :type key: str

        :param model_version:
            The value to assign to the model_version property of this SortOper.
        :type model_version: str

        :param parent_ref:
            The value to assign to the parent_ref property of this SortOper.
        :type parent_ref: oci.data_integration.models.ParentReference

        :param name:
            The value to assign to the name property of this SortOper.
        :type name: str

        :param description:
            The value to assign to the description property of this SortOper.
        :type description: str

        :param object_version:
            The value to assign to the object_version property of this SortOper.
        :type object_version: int

        :param input_ports:
            The value to assign to the input_ports property of this SortOper.
        :type input_ports: list[oci.data_integration.models.InputPort]

        :param output_ports:
            The value to assign to the output_ports property of this SortOper.
        :type output_ports: list[oci.data_integration.models.TypedObject]

        :param object_status:
            The value to assign to the object_status property of this SortOper.
        :type object_status: int

        :param identifier:
            The value to assign to the identifier property of this SortOper.
        :type identifier: str

        :param parameters:
            The value to assign to the parameters property of this SortOper.
        :type parameters: list[oci.data_integration.models.Parameter]

        :param op_config_values:
            The value to assign to the op_config_values property of this SortOper.
        :type op_config_values: oci.data_integration.models.ConfigValues

        :param sort_key:
            The value to assign to the sort_key property of this SortOper.
        :type sort_key: oci.data_integration.models.SortKey

        """
        self.swagger_types = {
            'model_type': 'str',
            'key': 'str',
            'model_version': 'str',
            'parent_ref': 'ParentReference',
            'name': 'str',
            'description': 'str',
            'object_version': 'int',
            'input_ports': 'list[InputPort]',
            'output_ports': 'list[TypedObject]',
            'object_status': 'int',
            'identifier': 'str',
            'parameters': 'list[Parameter]',
            'op_config_values': 'ConfigValues',
            'sort_key': 'SortKey'
        }

        self.attribute_map = {
            'model_type': 'modelType',
            'key': 'key',
            'model_version': 'modelVersion',
            'parent_ref': 'parentRef',
            'name': 'name',
            'description': 'description',
            'object_version': 'objectVersion',
            'input_ports': 'inputPorts',
            'output_ports': 'outputPorts',
            'object_status': 'objectStatus',
            'identifier': 'identifier',
            'parameters': 'parameters',
            'op_config_values': 'opConfigValues',
            'sort_key': 'sortKey'
        }

        self._model_type = None
        self._key = None
        self._model_version = None
        self._parent_ref = None
        self._name = None
        self._description = None
        self._object_version = None
        self._input_ports = None
        self._output_ports = None
        self._object_status = None
        self._identifier = None
        self._parameters = None
        self._op_config_values = None
        self._sort_key = None
        self._model_type = 'SORT_OPERATOR'

    @property
    def sort_key(self):
        """
        Gets the sort_key of this SortOper.

        :return: The sort_key of this SortOper.
        :rtype: oci.data_integration.models.SortKey
        """
        return self._sort_key

    @sort_key.setter
    def sort_key(self, sort_key):
        """
        Sets the sort_key of this SortOper.

        :param sort_key: The sort_key of this SortOper.
        :type: oci.data_integration.models.SortKey
        """
        self._sort_key = sort_key

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
