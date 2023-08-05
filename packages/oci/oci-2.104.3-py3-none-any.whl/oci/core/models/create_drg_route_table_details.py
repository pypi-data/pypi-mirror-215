# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateDrgRouteTableDetails(object):
    """
    Details used in a request to create a DRG route table.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateDrgRouteTableDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateDrgRouteTableDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param display_name:
            The value to assign to the display_name property of this CreateDrgRouteTableDetails.
        :type display_name: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateDrgRouteTableDetails.
        :type freeform_tags: dict(str, str)

        :param drg_id:
            The value to assign to the drg_id property of this CreateDrgRouteTableDetails.
        :type drg_id: str

        :param import_drg_route_distribution_id:
            The value to assign to the import_drg_route_distribution_id property of this CreateDrgRouteTableDetails.
        :type import_drg_route_distribution_id: str

        :param is_ecmp_enabled:
            The value to assign to the is_ecmp_enabled property of this CreateDrgRouteTableDetails.
        :type is_ecmp_enabled: bool

        """
        self.swagger_types = {
            'defined_tags': 'dict(str, dict(str, object))',
            'display_name': 'str',
            'freeform_tags': 'dict(str, str)',
            'drg_id': 'str',
            'import_drg_route_distribution_id': 'str',
            'is_ecmp_enabled': 'bool'
        }

        self.attribute_map = {
            'defined_tags': 'definedTags',
            'display_name': 'displayName',
            'freeform_tags': 'freeformTags',
            'drg_id': 'drgId',
            'import_drg_route_distribution_id': 'importDrgRouteDistributionId',
            'is_ecmp_enabled': 'isEcmpEnabled'
        }

        self._defined_tags = None
        self._display_name = None
        self._freeform_tags = None
        self._drg_id = None
        self._import_drg_route_distribution_id = None
        self._is_ecmp_enabled = None

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateDrgRouteTableDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateDrgRouteTableDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateDrgRouteTableDetails.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateDrgRouteTableDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateDrgRouteTableDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :return: The display_name of this CreateDrgRouteTableDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateDrgRouteTableDetails.
        A user-friendly name. Does not have to be unique, and it's changeable.
        Avoid entering confidential information.


        :param display_name: The display_name of this CreateDrgRouteTableDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateDrgRouteTableDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateDrgRouteTableDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateDrgRouteTableDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateDrgRouteTableDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def drg_id(self):
        """
        **[Required]** Gets the drg_id of this CreateDrgRouteTableDetails.
        The `OCID`__ of the DRG the DRG route table belongs to.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The drg_id of this CreateDrgRouteTableDetails.
        :rtype: str
        """
        return self._drg_id

    @drg_id.setter
    def drg_id(self, drg_id):
        """
        Sets the drg_id of this CreateDrgRouteTableDetails.
        The `OCID`__ of the DRG the DRG route table belongs to.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param drg_id: The drg_id of this CreateDrgRouteTableDetails.
        :type: str
        """
        self._drg_id = drg_id

    @property
    def import_drg_route_distribution_id(self):
        """
        Gets the import_drg_route_distribution_id of this CreateDrgRouteTableDetails.
        The `OCID`__ of the import route distribution used to specify how incoming route advertisements through
        referenced attachments are inserted into the DRG route table.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :return: The import_drg_route_distribution_id of this CreateDrgRouteTableDetails.
        :rtype: str
        """
        return self._import_drg_route_distribution_id

    @import_drg_route_distribution_id.setter
    def import_drg_route_distribution_id(self, import_drg_route_distribution_id):
        """
        Sets the import_drg_route_distribution_id of this CreateDrgRouteTableDetails.
        The `OCID`__ of the import route distribution used to specify how incoming route advertisements through
        referenced attachments are inserted into the DRG route table.

        __ https://docs.cloud.oracle.com/iaas/Content/General/Concepts/identifiers.htm


        :param import_drg_route_distribution_id: The import_drg_route_distribution_id of this CreateDrgRouteTableDetails.
        :type: str
        """
        self._import_drg_route_distribution_id = import_drg_route_distribution_id

    @property
    def is_ecmp_enabled(self):
        """
        Gets the is_ecmp_enabled of this CreateDrgRouteTableDetails.
        If you want traffic to be routed using ECMP across your virtual circuits or IPSec tunnels to
        your on-premises networks, enable ECMP on the DRG route table.


        :return: The is_ecmp_enabled of this CreateDrgRouteTableDetails.
        :rtype: bool
        """
        return self._is_ecmp_enabled

    @is_ecmp_enabled.setter
    def is_ecmp_enabled(self, is_ecmp_enabled):
        """
        Sets the is_ecmp_enabled of this CreateDrgRouteTableDetails.
        If you want traffic to be routed using ECMP across your virtual circuits or IPSec tunnels to
        your on-premises networks, enable ECMP on the DRG route table.


        :param is_ecmp_enabled: The is_ecmp_enabled of this CreateDrgRouteTableDetails.
        :type: bool
        """
        self._is_ecmp_enabled = is_ecmp_enabled

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
