# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .monitoring_source_metric_details import MonitoringSourceMetricDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MonitoringSourceAllMetrics(MonitoringSourceMetricDetails):
    """
    Discriminator for metrics in the compartment-specific list.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new MonitoringSourceAllMetrics object with values from keyword arguments. The default value of the :py:attr:`~oci.sch.models.MonitoringSourceAllMetrics.kind` attribute
        of this class is ``all`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this MonitoringSourceAllMetrics.
            Allowed values for this property are: "all"
        :type kind: str

        """
        self.swagger_types = {
            'kind': 'str'
        }

        self.attribute_map = {
            'kind': 'kind'
        }

        self._kind = None
        self._kind = 'all'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
