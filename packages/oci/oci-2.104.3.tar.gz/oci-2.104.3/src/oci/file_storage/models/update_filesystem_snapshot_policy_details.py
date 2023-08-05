# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateFilesystemSnapshotPolicyDetails(object):
    """
    Details for updating the file system snapshot policy.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateFilesystemSnapshotPolicyDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this UpdateFilesystemSnapshotPolicyDetails.
        :type display_name: str

        :param policy_prefix:
            The value to assign to the policy_prefix property of this UpdateFilesystemSnapshotPolicyDetails.
        :type policy_prefix: str

        :param schedules:
            The value to assign to the schedules property of this UpdateFilesystemSnapshotPolicyDetails.
        :type schedules: list[oci.file_storage.models.SnapshotSchedule]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateFilesystemSnapshotPolicyDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateFilesystemSnapshotPolicyDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'display_name': 'str',
            'policy_prefix': 'str',
            'schedules': 'list[SnapshotSchedule]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'policy_prefix': 'policyPrefix',
            'schedules': 'schedules',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._display_name = None
        self._policy_prefix = None
        self._schedules = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def display_name(self):
        """
        Gets the display_name of this UpdateFilesystemSnapshotPolicyDetails.
        A user-friendly name. It does not have to be unique, and it is changeable.
        Avoid entering confidential information.

        Example: `policy1`


        :return: The display_name of this UpdateFilesystemSnapshotPolicyDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this UpdateFilesystemSnapshotPolicyDetails.
        A user-friendly name. It does not have to be unique, and it is changeable.
        Avoid entering confidential information.

        Example: `policy1`


        :param display_name: The display_name of this UpdateFilesystemSnapshotPolicyDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def policy_prefix(self):
        """
        Gets the policy_prefix of this UpdateFilesystemSnapshotPolicyDetails.
        The prefix to apply to all snapshots created by this policy.

        Example: `acme`


        :return: The policy_prefix of this UpdateFilesystemSnapshotPolicyDetails.
        :rtype: str
        """
        return self._policy_prefix

    @policy_prefix.setter
    def policy_prefix(self, policy_prefix):
        """
        Sets the policy_prefix of this UpdateFilesystemSnapshotPolicyDetails.
        The prefix to apply to all snapshots created by this policy.

        Example: `acme`


        :param policy_prefix: The policy_prefix of this UpdateFilesystemSnapshotPolicyDetails.
        :type: str
        """
        self._policy_prefix = policy_prefix

    @property
    def schedules(self):
        """
        Gets the schedules of this UpdateFilesystemSnapshotPolicyDetails.
        The list of associated snapshot schedules. A maximum of 10 schedules can be associated with a policy.

        If using the CLI, provide the schedule as a list of JSON strings, with the list wrapped in
        quotation marks, i.e.
        ```
          --schedules '[{\"timeZone\":\"UTC\",\"period\":\"DAILY\",\"hourOfDay\":18},{\"timeZone\":\"UTC\",\"period\":\"HOURLY\"}]'
        ```


        :return: The schedules of this UpdateFilesystemSnapshotPolicyDetails.
        :rtype: list[oci.file_storage.models.SnapshotSchedule]
        """
        return self._schedules

    @schedules.setter
    def schedules(self, schedules):
        """
        Sets the schedules of this UpdateFilesystemSnapshotPolicyDetails.
        The list of associated snapshot schedules. A maximum of 10 schedules can be associated with a policy.

        If using the CLI, provide the schedule as a list of JSON strings, with the list wrapped in
        quotation marks, i.e.
        ```
          --schedules '[{\"timeZone\":\"UTC\",\"period\":\"DAILY\",\"hourOfDay\":18},{\"timeZone\":\"UTC\",\"period\":\"HOURLY\"}]'
        ```


        :param schedules: The schedules of this UpdateFilesystemSnapshotPolicyDetails.
        :type: list[oci.file_storage.models.SnapshotSchedule]
        """
        self._schedules = schedules

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateFilesystemSnapshotPolicyDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair
         with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateFilesystemSnapshotPolicyDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateFilesystemSnapshotPolicyDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair
         with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateFilesystemSnapshotPolicyDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateFilesystemSnapshotPolicyDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateFilesystemSnapshotPolicyDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateFilesystemSnapshotPolicyDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.
        Example: `{\"Operations\": {\"CostCenter\": \"42\"}}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateFilesystemSnapshotPolicyDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
