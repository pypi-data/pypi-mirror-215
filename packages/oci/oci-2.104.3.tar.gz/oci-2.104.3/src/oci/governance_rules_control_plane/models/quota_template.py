# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .template import Template
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class QuotaTemplate(Template):
    """
    Quota template for governance rule.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new QuotaTemplate object with values from keyword arguments. The default value of the :py:attr:`~oci.governance_rules_control_plane.models.QuotaTemplate.type` attribute
        of this class is ``QUOTA`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this QuotaTemplate.
            Allowed values for this property are: "QUOTA", "TAG", "ALLOWED_REGIONS"
        :type type: str

        :param display_name:
            The value to assign to the display_name property of this QuotaTemplate.
        :type display_name: str

        :param description:
            The value to assign to the description property of this QuotaTemplate.
        :type description: str

        :param statements:
            The value to assign to the statements property of this QuotaTemplate.
        :type statements: list[str]

        """
        self.swagger_types = {
            'type': 'str',
            'display_name': 'str',
            'description': 'str',
            'statements': 'list[str]'
        }

        self.attribute_map = {
            'type': 'type',
            'display_name': 'displayName',
            'description': 'description',
            'statements': 'statements'
        }

        self._type = None
        self._display_name = None
        self._description = None
        self._statements = None
        self._type = 'QUOTA'

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this QuotaTemplate.
        Display name of the quota resource.


        :return: The display_name of this QuotaTemplate.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this QuotaTemplate.
        Display name of the quota resource.


        :param display_name: The display_name of this QuotaTemplate.
        :type: str
        """
        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this QuotaTemplate.
        Description of the quota resource.


        :return: The description of this QuotaTemplate.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this QuotaTemplate.
        Description of the quota resource.


        :param description: The description of this QuotaTemplate.
        :type: str
        """
        self._description = description

    @property
    def statements(self):
        """
        **[Required]** Gets the statements of this QuotaTemplate.
        List of quota statements.


        :return: The statements of this QuotaTemplate.
        :rtype: list[str]
        """
        return self._statements

    @statements.setter
    def statements(self, statements):
        """
        Sets the statements of this QuotaTemplate.
        List of quota statements.


        :param statements: The statements of this QuotaTemplate.
        :type: list[str]
        """
        self._statements = statements

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
