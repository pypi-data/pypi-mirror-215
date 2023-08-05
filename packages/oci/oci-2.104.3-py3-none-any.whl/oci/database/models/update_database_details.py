# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class UpdateDatabaseDetails(object):
    """
    Details to update a database.

    **Warning:** Oracle recommends that you avoid using any confidential information when you supply string values using the API.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new UpdateDatabaseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param db_backup_config:
            The value to assign to the db_backup_config property of this UpdateDatabaseDetails.
        :type db_backup_config: oci.database.models.DbBackupConfig

        :param db_home_id:
            The value to assign to the db_home_id property of this UpdateDatabaseDetails.
        :type db_home_id: str

        :param new_admin_password:
            The value to assign to the new_admin_password property of this UpdateDatabaseDetails.
        :type new_admin_password: str

        :param old_tde_wallet_password:
            The value to assign to the old_tde_wallet_password property of this UpdateDatabaseDetails.
        :type old_tde_wallet_password: str

        :param new_tde_wallet_password:
            The value to assign to the new_tde_wallet_password property of this UpdateDatabaseDetails.
        :type new_tde_wallet_password: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this UpdateDatabaseDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this UpdateDatabaseDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'db_backup_config': 'DbBackupConfig',
            'db_home_id': 'str',
            'new_admin_password': 'str',
            'old_tde_wallet_password': 'str',
            'new_tde_wallet_password': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'db_backup_config': 'dbBackupConfig',
            'db_home_id': 'dbHomeId',
            'new_admin_password': 'newAdminPassword',
            'old_tde_wallet_password': 'oldTdeWalletPassword',
            'new_tde_wallet_password': 'newTdeWalletPassword',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._db_backup_config = None
        self._db_home_id = None
        self._new_admin_password = None
        self._old_tde_wallet_password = None
        self._new_tde_wallet_password = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def db_backup_config(self):
        """
        Gets the db_backup_config of this UpdateDatabaseDetails.

        :return: The db_backup_config of this UpdateDatabaseDetails.
        :rtype: oci.database.models.DbBackupConfig
        """
        return self._db_backup_config

    @db_backup_config.setter
    def db_backup_config(self, db_backup_config):
        """
        Sets the db_backup_config of this UpdateDatabaseDetails.

        :param db_backup_config: The db_backup_config of this UpdateDatabaseDetails.
        :type: oci.database.models.DbBackupConfig
        """
        self._db_backup_config = db_backup_config

    @property
    def db_home_id(self):
        """
        Gets the db_home_id of this UpdateDatabaseDetails.
        The `OCID`__ of the Database Home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The db_home_id of this UpdateDatabaseDetails.
        :rtype: str
        """
        return self._db_home_id

    @db_home_id.setter
    def db_home_id(self, db_home_id):
        """
        Sets the db_home_id of this UpdateDatabaseDetails.
        The `OCID`__ of the Database Home.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param db_home_id: The db_home_id of this UpdateDatabaseDetails.
        :type: str
        """
        self._db_home_id = db_home_id

    @property
    def new_admin_password(self):
        """
        Gets the new_admin_password of this UpdateDatabaseDetails.
        A new strong password for SYS, SYSTEM, and the plugbable database ADMIN user. The password must be at least nine characters and contain at least two uppercase, two lowercase, two numeric, and two special characters. The special characters must be _, \\#, or -.


        :return: The new_admin_password of this UpdateDatabaseDetails.
        :rtype: str
        """
        return self._new_admin_password

    @new_admin_password.setter
    def new_admin_password(self, new_admin_password):
        """
        Sets the new_admin_password of this UpdateDatabaseDetails.
        A new strong password for SYS, SYSTEM, and the plugbable database ADMIN user. The password must be at least nine characters and contain at least two uppercase, two lowercase, two numeric, and two special characters. The special characters must be _, \\#, or -.


        :param new_admin_password: The new_admin_password of this UpdateDatabaseDetails.
        :type: str
        """
        self._new_admin_password = new_admin_password

    @property
    def old_tde_wallet_password(self):
        """
        Gets the old_tde_wallet_password of this UpdateDatabaseDetails.
        The existing TDE wallet password. You must provide the existing password in order to set a new TDE wallet password.


        :return: The old_tde_wallet_password of this UpdateDatabaseDetails.
        :rtype: str
        """
        return self._old_tde_wallet_password

    @old_tde_wallet_password.setter
    def old_tde_wallet_password(self, old_tde_wallet_password):
        """
        Sets the old_tde_wallet_password of this UpdateDatabaseDetails.
        The existing TDE wallet password. You must provide the existing password in order to set a new TDE wallet password.


        :param old_tde_wallet_password: The old_tde_wallet_password of this UpdateDatabaseDetails.
        :type: str
        """
        self._old_tde_wallet_password = old_tde_wallet_password

    @property
    def new_tde_wallet_password(self):
        """
        Gets the new_tde_wallet_password of this UpdateDatabaseDetails.
        The new password to open the TDE wallet. The password must be at least nine characters and contain at least two uppercase, two lowercase, two numeric, and two special characters. The special characters must be _, \\#, or -.


        :return: The new_tde_wallet_password of this UpdateDatabaseDetails.
        :rtype: str
        """
        return self._new_tde_wallet_password

    @new_tde_wallet_password.setter
    def new_tde_wallet_password(self, new_tde_wallet_password):
        """
        Sets the new_tde_wallet_password of this UpdateDatabaseDetails.
        The new password to open the TDE wallet. The password must be at least nine characters and contain at least two uppercase, two lowercase, two numeric, and two special characters. The special characters must be _, \\#, or -.


        :param new_tde_wallet_password: The new_tde_wallet_password of this UpdateDatabaseDetails.
        :type: str
        """
        self._new_tde_wallet_password = new_tde_wallet_password

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this UpdateDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this UpdateDatabaseDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this UpdateDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this UpdateDatabaseDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this UpdateDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this UpdateDatabaseDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this UpdateDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this UpdateDatabaseDetails.
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
