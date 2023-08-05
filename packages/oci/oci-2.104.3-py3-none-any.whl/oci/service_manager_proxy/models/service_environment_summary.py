# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ServiceEnvironmentSummary(object):
    """
    Summary of service environment details.
    """

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "INITIALIZED"
    STATUS_INITIALIZED = "INITIALIZED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_ACTIVATION"
    STATUS_BEGIN_ACTIVATION = "BEGIN_ACTIVATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "ACTIVE"
    STATUS_ACTIVE = "ACTIVE"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_SOFT_TERMINATION"
    STATUS_BEGIN_SOFT_TERMINATION = "BEGIN_SOFT_TERMINATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "SOFT_TERMINATED"
    STATUS_SOFT_TERMINATED = "SOFT_TERMINATED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_TERMINATION"
    STATUS_BEGIN_TERMINATION = "BEGIN_TERMINATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "CANCELED"
    STATUS_CANCELED = "CANCELED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "TERMINATED"
    STATUS_TERMINATED = "TERMINATED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_DISABLING"
    STATUS_BEGIN_DISABLING = "BEGIN_DISABLING"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_ENABLING"
    STATUS_BEGIN_ENABLING = "BEGIN_ENABLING"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_MIGRATION"
    STATUS_BEGIN_MIGRATION = "BEGIN_MIGRATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "DISABLED"
    STATUS_DISABLED = "DISABLED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_SUSPENSION"
    STATUS_BEGIN_SUSPENSION = "BEGIN_SUSPENSION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_RESUMPTION"
    STATUS_BEGIN_RESUMPTION = "BEGIN_RESUMPTION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "SUSPENDED"
    STATUS_SUSPENDED = "SUSPENDED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_LOCK_RELOCATION"
    STATUS_BEGIN_LOCK_RELOCATION = "BEGIN_LOCK_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "LOCKED_RELOCATION"
    STATUS_LOCKED_RELOCATION = "LOCKED_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_RELOCATION"
    STATUS_BEGIN_RELOCATION = "BEGIN_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "RELOCATED"
    STATUS_RELOCATED = "RELOCATED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_UNLOCK_RELOCATION"
    STATUS_BEGIN_UNLOCK_RELOCATION = "BEGIN_UNLOCK_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "UNLOCKED_RELOCATION"
    STATUS_UNLOCKED_RELOCATION = "UNLOCKED_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "FAILED_LOCK_RELOCATION"
    STATUS_FAILED_LOCK_RELOCATION = "FAILED_LOCK_RELOCATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "FAILED_ACTIVATION"
    STATUS_FAILED_ACTIVATION = "FAILED_ACTIVATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "FAILED_MIGRATION"
    STATUS_FAILED_MIGRATION = "FAILED_MIGRATION"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "ACCESS_DISABLED"
    STATUS_ACCESS_DISABLED = "ACCESS_DISABLED"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_DISABLING_ACCESS"
    STATUS_BEGIN_DISABLING_ACCESS = "BEGIN_DISABLING_ACCESS"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "BEGIN_ENABLING_ACCESS"
    STATUS_BEGIN_ENABLING_ACCESS = "BEGIN_ENABLING_ACCESS"

    #: A constant which can be used with the status property of a ServiceEnvironmentSummary.
    #: This constant has a value of "TRA_UNKNOWN"
    STATUS_TRA_UNKNOWN = "TRA_UNKNOWN"

    def __init__(self, **kwargs):
        """
        Initializes a new ServiceEnvironmentSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this ServiceEnvironmentSummary.
        :type id: str

        :param subscription_id:
            The value to assign to the subscription_id property of this ServiceEnvironmentSummary.
        :type subscription_id: str

        :param status:
            The value to assign to the status property of this ServiceEnvironmentSummary.
            Allowed values for this property are: "INITIALIZED", "BEGIN_ACTIVATION", "ACTIVE", "BEGIN_SOFT_TERMINATION", "SOFT_TERMINATED", "BEGIN_TERMINATION", "CANCELED", "TERMINATED", "BEGIN_DISABLING", "BEGIN_ENABLING", "BEGIN_MIGRATION", "DISABLED", "BEGIN_SUSPENSION", "BEGIN_RESUMPTION", "SUSPENDED", "BEGIN_LOCK_RELOCATION", "LOCKED_RELOCATION", "BEGIN_RELOCATION", "RELOCATED", "BEGIN_UNLOCK_RELOCATION", "UNLOCKED_RELOCATION", "FAILED_LOCK_RELOCATION", "FAILED_ACTIVATION", "FAILED_MIGRATION", "ACCESS_DISABLED", "BEGIN_DISABLING_ACCESS", "BEGIN_ENABLING_ACCESS", "TRA_UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type status: str

        :param compartment_id:
            The value to assign to the compartment_id property of this ServiceEnvironmentSummary.
        :type compartment_id: str

        :param service_definition:
            The value to assign to the service_definition property of this ServiceEnvironmentSummary.
        :type service_definition: oci.service_manager_proxy.models.ServiceDefinition

        :param console_url:
            The value to assign to the console_url property of this ServiceEnvironmentSummary.
        :type console_url: str

        :param service_environment_endpoints:
            The value to assign to the service_environment_endpoints property of this ServiceEnvironmentSummary.
        :type service_environment_endpoints: list[oci.service_manager_proxy.models.ServiceEnvironmentEndPointOverview]

        :param defined_tags:
            The value to assign to the defined_tags property of this ServiceEnvironmentSummary.
        :type defined_tags: dict(str, dict(str, object))

        :param freeform_tags:
            The value to assign to the freeform_tags property of this ServiceEnvironmentSummary.
        :type freeform_tags: dict(str, str)

        """
        self.swagger_types = {
            'id': 'str',
            'subscription_id': 'str',
            'status': 'str',
            'compartment_id': 'str',
            'service_definition': 'ServiceDefinition',
            'console_url': 'str',
            'service_environment_endpoints': 'list[ServiceEnvironmentEndPointOverview]',
            'defined_tags': 'dict(str, dict(str, object))',
            'freeform_tags': 'dict(str, str)'
        }

        self.attribute_map = {
            'id': 'id',
            'subscription_id': 'subscriptionId',
            'status': 'status',
            'compartment_id': 'compartmentId',
            'service_definition': 'serviceDefinition',
            'console_url': 'consoleUrl',
            'service_environment_endpoints': 'serviceEnvironmentEndpoints',
            'defined_tags': 'definedTags',
            'freeform_tags': 'freeformTags'
        }

        self._id = None
        self._subscription_id = None
        self._status = None
        self._compartment_id = None
        self._service_definition = None
        self._console_url = None
        self._service_environment_endpoints = None
        self._defined_tags = None
        self._freeform_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this ServiceEnvironmentSummary.
        Unqiue identifier for the entitlement related to the environment.

        **Note:** Not an `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this ServiceEnvironmentSummary.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ServiceEnvironmentSummary.
        Unqiue identifier for the entitlement related to the environment.

        **Note:** Not an `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this ServiceEnvironmentSummary.
        :type: str
        """
        self._id = id

    @property
    def subscription_id(self):
        """
        **[Required]** Gets the subscription_id of this ServiceEnvironmentSummary.
        The unique subscription ID associated with the service environment ID.

        **Note:** Not an `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The subscription_id of this ServiceEnvironmentSummary.
        :rtype: str
        """
        return self._subscription_id

    @subscription_id.setter
    def subscription_id(self, subscription_id):
        """
        Sets the subscription_id of this ServiceEnvironmentSummary.
        The unique subscription ID associated with the service environment ID.

        **Note:** Not an `OCID`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param subscription_id: The subscription_id of this ServiceEnvironmentSummary.
        :type: str
        """
        self._subscription_id = subscription_id

    @property
    def status(self):
        """
        **[Required]** Gets the status of this ServiceEnvironmentSummary.
        Status of the entitlement registration for the service.

        Allowed values for this property are: "INITIALIZED", "BEGIN_ACTIVATION", "ACTIVE", "BEGIN_SOFT_TERMINATION", "SOFT_TERMINATED", "BEGIN_TERMINATION", "CANCELED", "TERMINATED", "BEGIN_DISABLING", "BEGIN_ENABLING", "BEGIN_MIGRATION", "DISABLED", "BEGIN_SUSPENSION", "BEGIN_RESUMPTION", "SUSPENDED", "BEGIN_LOCK_RELOCATION", "LOCKED_RELOCATION", "BEGIN_RELOCATION", "RELOCATED", "BEGIN_UNLOCK_RELOCATION", "UNLOCKED_RELOCATION", "FAILED_LOCK_RELOCATION", "FAILED_ACTIVATION", "FAILED_MIGRATION", "ACCESS_DISABLED", "BEGIN_DISABLING_ACCESS", "BEGIN_ENABLING_ACCESS", "TRA_UNKNOWN", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The status of this ServiceEnvironmentSummary.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ServiceEnvironmentSummary.
        Status of the entitlement registration for the service.


        :param status: The status of this ServiceEnvironmentSummary.
        :type: str
        """
        allowed_values = ["INITIALIZED", "BEGIN_ACTIVATION", "ACTIVE", "BEGIN_SOFT_TERMINATION", "SOFT_TERMINATED", "BEGIN_TERMINATION", "CANCELED", "TERMINATED", "BEGIN_DISABLING", "BEGIN_ENABLING", "BEGIN_MIGRATION", "DISABLED", "BEGIN_SUSPENSION", "BEGIN_RESUMPTION", "SUSPENDED", "BEGIN_LOCK_RELOCATION", "LOCKED_RELOCATION", "BEGIN_RELOCATION", "RELOCATED", "BEGIN_UNLOCK_RELOCATION", "UNLOCKED_RELOCATION", "FAILED_LOCK_RELOCATION", "FAILED_ACTIVATION", "FAILED_MIGRATION", "ACCESS_DISABLED", "BEGIN_DISABLING_ACCESS", "BEGIN_ENABLING_ACCESS", "TRA_UNKNOWN"]
        if not value_allowed_none_or_none_sentinel(status, allowed_values):
            status = 'UNKNOWN_ENUM_VALUE'
        self._status = status

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this ServiceEnvironmentSummary.
        The `OCID`__ for the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this ServiceEnvironmentSummary.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this ServiceEnvironmentSummary.
        The `OCID`__ for the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this ServiceEnvironmentSummary.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def service_definition(self):
        """
        **[Required]** Gets the service_definition of this ServiceEnvironmentSummary.

        :return: The service_definition of this ServiceEnvironmentSummary.
        :rtype: oci.service_manager_proxy.models.ServiceDefinition
        """
        return self._service_definition

    @service_definition.setter
    def service_definition(self, service_definition):
        """
        Sets the service_definition of this ServiceEnvironmentSummary.

        :param service_definition: The service_definition of this ServiceEnvironmentSummary.
        :type: oci.service_manager_proxy.models.ServiceDefinition
        """
        self._service_definition = service_definition

    @property
    def console_url(self):
        """
        Gets the console_url of this ServiceEnvironmentSummary.
        The URL for the console.


        :return: The console_url of this ServiceEnvironmentSummary.
        :rtype: str
        """
        return self._console_url

    @console_url.setter
    def console_url(self, console_url):
        """
        Sets the console_url of this ServiceEnvironmentSummary.
        The URL for the console.


        :param console_url: The console_url of this ServiceEnvironmentSummary.
        :type: str
        """
        self._console_url = console_url

    @property
    def service_environment_endpoints(self):
        """
        Gets the service_environment_endpoints of this ServiceEnvironmentSummary.
        Array of service environment end points.


        :return: The service_environment_endpoints of this ServiceEnvironmentSummary.
        :rtype: list[oci.service_manager_proxy.models.ServiceEnvironmentEndPointOverview]
        """
        return self._service_environment_endpoints

    @service_environment_endpoints.setter
    def service_environment_endpoints(self, service_environment_endpoints):
        """
        Sets the service_environment_endpoints of this ServiceEnvironmentSummary.
        Array of service environment end points.


        :param service_environment_endpoints: The service_environment_endpoints of this ServiceEnvironmentSummary.
        :type: list[oci.service_manager_proxy.models.ServiceEnvironmentEndPointOverview]
        """
        self._service_environment_endpoints = service_environment_endpoints

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this ServiceEnvironmentSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this ServiceEnvironmentSummary.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this ServiceEnvironmentSummary.
        Defined tags for this resource. Each key is predefined and scoped to a
        namespace. For more information, see `Resource Tags`__.

        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this ServiceEnvironmentSummary.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this ServiceEnvironmentSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"CostCenter\": \"42\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this ServiceEnvironmentSummary.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this ServiceEnvironmentSummary.
        Free-form tags for this resource. Each tag is a simple key-value pair with no
        predefined name, type, or namespace. For more information, see `Resource Tags`__.

        Example: `{\"CostCenter\": \"42\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this ServiceEnvironmentSummary.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
