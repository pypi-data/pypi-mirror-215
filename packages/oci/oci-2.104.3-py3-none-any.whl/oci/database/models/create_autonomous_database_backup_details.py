# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateAutonomousDatabaseBackupDetails(object):
    """
    Details to create an Oracle Autonomous Database backup.

    **Warning:** Oracle recommends that you avoid using any confidential information when you supply string values using the API.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateAutonomousDatabaseBackupDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateAutonomousDatabaseBackupDetails.
        :type display_name: str

        :param autonomous_database_id:
            The value to assign to the autonomous_database_id property of this CreateAutonomousDatabaseBackupDetails.
        :type autonomous_database_id: str

        :param retention_period_in_days:
            The value to assign to the retention_period_in_days property of this CreateAutonomousDatabaseBackupDetails.
        :type retention_period_in_days: int

        :param is_long_term_backup:
            The value to assign to the is_long_term_backup property of this CreateAutonomousDatabaseBackupDetails.
        :type is_long_term_backup: bool

        :param backup_destination_details:
            The value to assign to the backup_destination_details property of this CreateAutonomousDatabaseBackupDetails.
        :type backup_destination_details: oci.database.models.BackupDestinationDetails

        """
        self.swagger_types = {
            'display_name': 'str',
            'autonomous_database_id': 'str',
            'retention_period_in_days': 'int',
            'is_long_term_backup': 'bool',
            'backup_destination_details': 'BackupDestinationDetails'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'autonomous_database_id': 'autonomousDatabaseId',
            'retention_period_in_days': 'retentionPeriodInDays',
            'is_long_term_backup': 'isLongTermBackup',
            'backup_destination_details': 'backupDestinationDetails'
        }

        self._display_name = None
        self._autonomous_database_id = None
        self._retention_period_in_days = None
        self._is_long_term_backup = None
        self._backup_destination_details = None

    @property
    def display_name(self):
        """
        Gets the display_name of this CreateAutonomousDatabaseBackupDetails.
        The user-friendly name for the backup. The name does not have to be unique.


        :return: The display_name of this CreateAutonomousDatabaseBackupDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateAutonomousDatabaseBackupDetails.
        The user-friendly name for the backup. The name does not have to be unique.


        :param display_name: The display_name of this CreateAutonomousDatabaseBackupDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def autonomous_database_id(self):
        """
        **[Required]** Gets the autonomous_database_id of this CreateAutonomousDatabaseBackupDetails.
        The `OCID`__ of the Autonomous Database backup.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The autonomous_database_id of this CreateAutonomousDatabaseBackupDetails.
        :rtype: str
        """
        return self._autonomous_database_id

    @autonomous_database_id.setter
    def autonomous_database_id(self, autonomous_database_id):
        """
        Sets the autonomous_database_id of this CreateAutonomousDatabaseBackupDetails.
        The `OCID`__ of the Autonomous Database backup.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param autonomous_database_id: The autonomous_database_id of this CreateAutonomousDatabaseBackupDetails.
        :type: str
        """
        self._autonomous_database_id = autonomous_database_id

    @property
    def retention_period_in_days(self):
        """
        Gets the retention_period_in_days of this CreateAutonomousDatabaseBackupDetails.
        Retention period, in days, for long-term backups


        :return: The retention_period_in_days of this CreateAutonomousDatabaseBackupDetails.
        :rtype: int
        """
        return self._retention_period_in_days

    @retention_period_in_days.setter
    def retention_period_in_days(self, retention_period_in_days):
        """
        Sets the retention_period_in_days of this CreateAutonomousDatabaseBackupDetails.
        Retention period, in days, for long-term backups


        :param retention_period_in_days: The retention_period_in_days of this CreateAutonomousDatabaseBackupDetails.
        :type: int
        """
        self._retention_period_in_days = retention_period_in_days

    @property
    def is_long_term_backup(self):
        """
        Gets the is_long_term_backup of this CreateAutonomousDatabaseBackupDetails.
        Indicates whether the backup is long-term


        :return: The is_long_term_backup of this CreateAutonomousDatabaseBackupDetails.
        :rtype: bool
        """
        return self._is_long_term_backup

    @is_long_term_backup.setter
    def is_long_term_backup(self, is_long_term_backup):
        """
        Sets the is_long_term_backup of this CreateAutonomousDatabaseBackupDetails.
        Indicates whether the backup is long-term


        :param is_long_term_backup: The is_long_term_backup of this CreateAutonomousDatabaseBackupDetails.
        :type: bool
        """
        self._is_long_term_backup = is_long_term_backup

    @property
    def backup_destination_details(self):
        """
        Gets the backup_destination_details of this CreateAutonomousDatabaseBackupDetails.

        :return: The backup_destination_details of this CreateAutonomousDatabaseBackupDetails.
        :rtype: oci.database.models.BackupDestinationDetails
        """
        return self._backup_destination_details

    @backup_destination_details.setter
    def backup_destination_details(self, backup_destination_details):
        """
        Sets the backup_destination_details of this CreateAutonomousDatabaseBackupDetails.

        :param backup_destination_details: The backup_destination_details of this CreateAutonomousDatabaseBackupDetails.
        :type: oci.database.models.BackupDestinationDetails
        """
        self._backup_destination_details = backup_destination_details

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
