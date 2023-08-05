# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .function_provisioned_concurrency_config import FunctionProvisionedConcurrencyConfig
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ConstantProvisionedConcurrencyConfig(FunctionProvisionedConcurrencyConfig):
    """
    Configuration specifying a constant amount of provisioned concurrency.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ConstantProvisionedConcurrencyConfig object with values from keyword arguments. The default value of the :py:attr:`~oci.functions.models.ConstantProvisionedConcurrencyConfig.strategy` attribute
        of this class is ``CONSTANT`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param strategy:
            The value to assign to the strategy property of this ConstantProvisionedConcurrencyConfig.
            Allowed values for this property are: "CONSTANT", "NONE"
        :type strategy: str

        :param count:
            The value to assign to the count property of this ConstantProvisionedConcurrencyConfig.
        :type count: int

        """
        self.swagger_types = {
            'strategy': 'str',
            'count': 'int'
        }

        self.attribute_map = {
            'strategy': 'strategy',
            'count': 'count'
        }

        self._strategy = None
        self._count = None
        self._strategy = 'CONSTANT'

    @property
    def count(self):
        """
        **[Required]** Gets the count of this ConstantProvisionedConcurrencyConfig.
        Configuration specifying a constant amount of provisioned concurrency.


        :return: The count of this ConstantProvisionedConcurrencyConfig.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this ConstantProvisionedConcurrencyConfig.
        Configuration specifying a constant amount of provisioned concurrency.


        :param count: The count of this ConstantProvisionedConcurrencyConfig.
        :type: int
        """
        self._count = count

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
