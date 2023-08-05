# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .create_dashboard_details import CreateDashboardDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateV1DashboardDetails(CreateDashboardDetails):
    """
    Details for creating a version 1 dashboard.
    The interpretation of the `config` and `widgets` fields depends on the runtime behavior of the Oracle Cloud Infrastructure Console.
    The sum of the `config` and `widget` fields JSON text representation cannot exceed 200 KB.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateV1DashboardDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.dashboard_service.models.CreateV1DashboardDetails.schema_version` attribute
        of this class is ``V1`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param dashboard_group_id:
            The value to assign to the dashboard_group_id property of this CreateV1DashboardDetails.
        :type dashboard_group_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateV1DashboardDetails.
        :type display_name: str

        :param description:
            The value to assign to the description property of this CreateV1DashboardDetails.
        :type description: str

        :param schema_version:
            The value to assign to the schema_version property of this CreateV1DashboardDetails.
        :type schema_version: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateV1DashboardDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateV1DashboardDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param config:
            The value to assign to the config property of this CreateV1DashboardDetails.
        :type config: object

        :param widgets:
            The value to assign to the widgets property of this CreateV1DashboardDetails.
        :type widgets: list[object]

        """
        self.swagger_types = {
            'dashboard_group_id': 'str',
            'display_name': 'str',
            'description': 'str',
            'schema_version': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'config': 'object',
            'widgets': 'list[object]'
        }

        self.attribute_map = {
            'dashboard_group_id': 'dashboardGroupId',
            'display_name': 'displayName',
            'description': 'description',
            'schema_version': 'schemaVersion',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'config': 'config',
            'widgets': 'widgets'
        }

        self._dashboard_group_id = None
        self._display_name = None
        self._description = None
        self._schema_version = None
        self._freeform_tags = None
        self._defined_tags = None
        self._config = None
        self._widgets = None
        self._schema_version = 'V1'

    @property
    def config(self):
        """
        Gets the config of this CreateV1DashboardDetails.
        The layout and widget placement for the dashboard.


        :return: The config of this CreateV1DashboardDetails.
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """
        Sets the config of this CreateV1DashboardDetails.
        The layout and widget placement for the dashboard.


        :param config: The config of this CreateV1DashboardDetails.
        :type: object
        """
        self._config = config

    @property
    def widgets(self):
        """
        **[Required]** Gets the widgets of this CreateV1DashboardDetails.
        The basic visualization building blocks of a dashboard.


        :return: The widgets of this CreateV1DashboardDetails.
        :rtype: list[object]
        """
        return self._widgets

    @widgets.setter
    def widgets(self, widgets):
        """
        Sets the widgets of this CreateV1DashboardDetails.
        The basic visualization building blocks of a dashboard.


        :param widgets: The widgets of this CreateV1DashboardDetails.
        :type: list[object]
        """
        self._widgets = widgets

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
