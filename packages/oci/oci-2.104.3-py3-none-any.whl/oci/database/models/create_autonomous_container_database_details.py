# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateAutonomousContainerDatabaseDetails(object):
    """
    Describes the required parameters for the creation of an Autonomous Container Database.
    """

    #: A constant which can be used with the service_level_agreement_type property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "STANDARD"
    SERVICE_LEVEL_AGREEMENT_TYPE_STANDARD = "STANDARD"

    #: A constant which can be used with the service_level_agreement_type property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "AUTONOMOUS_DATAGUARD"
    SERVICE_LEVEL_AGREEMENT_TYPE_AUTONOMOUS_DATAGUARD = "AUTONOMOUS_DATAGUARD"

    #: A constant which can be used with the protection_mode property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "MAXIMUM_AVAILABILITY"
    PROTECTION_MODE_MAXIMUM_AVAILABILITY = "MAXIMUM_AVAILABILITY"

    #: A constant which can be used with the protection_mode property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "MAXIMUM_PERFORMANCE"
    PROTECTION_MODE_MAXIMUM_PERFORMANCE = "MAXIMUM_PERFORMANCE"

    #: A constant which can be used with the patch_model property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "RELEASE_UPDATES"
    PATCH_MODEL_RELEASE_UPDATES = "RELEASE_UPDATES"

    #: A constant which can be used with the patch_model property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "RELEASE_UPDATE_REVISIONS"
    PATCH_MODEL_RELEASE_UPDATE_REVISIONS = "RELEASE_UPDATE_REVISIONS"

    #: A constant which can be used with the version_preference property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "NEXT_RELEASE_UPDATE"
    VERSION_PREFERENCE_NEXT_RELEASE_UPDATE = "NEXT_RELEASE_UPDATE"

    #: A constant which can be used with the version_preference property of a CreateAutonomousContainerDatabaseDetails.
    #: This constant has a value of "LATEST_RELEASE_UPDATE"
    VERSION_PREFERENCE_LATEST_RELEASE_UPDATE = "LATEST_RELEASE_UPDATE"

    def __init__(self, **kwargs):
        """
        Initializes a new CreateAutonomousContainerDatabaseDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param display_name:
            The value to assign to the display_name property of this CreateAutonomousContainerDatabaseDetails.
        :type display_name: str

        :param db_unique_name:
            The value to assign to the db_unique_name property of this CreateAutonomousContainerDatabaseDetails.
        :type db_unique_name: str

        :param db_name:
            The value to assign to the db_name property of this CreateAutonomousContainerDatabaseDetails.
        :type db_name: str

        :param service_level_agreement_type:
            The value to assign to the service_level_agreement_type property of this CreateAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "STANDARD", "AUTONOMOUS_DATAGUARD"
        :type service_level_agreement_type: str

        :param autonomous_exadata_infrastructure_id:
            The value to assign to the autonomous_exadata_infrastructure_id property of this CreateAutonomousContainerDatabaseDetails.
        :type autonomous_exadata_infrastructure_id: str

        :param db_version:
            The value to assign to the db_version property of this CreateAutonomousContainerDatabaseDetails.
        :type db_version: str

        :param peer_autonomous_exadata_infrastructure_id:
            The value to assign to the peer_autonomous_exadata_infrastructure_id property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_autonomous_exadata_infrastructure_id: str

        :param peer_autonomous_container_database_display_name:
            The value to assign to the peer_autonomous_container_database_display_name property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_autonomous_container_database_display_name: str

        :param protection_mode:
            The value to assign to the protection_mode property of this CreateAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"
        :type protection_mode: str

        :param fast_start_fail_over_lag_limit_in_seconds:
            The value to assign to the fast_start_fail_over_lag_limit_in_seconds property of this CreateAutonomousContainerDatabaseDetails.
        :type fast_start_fail_over_lag_limit_in_seconds: int

        :param is_automatic_failover_enabled:
            The value to assign to the is_automatic_failover_enabled property of this CreateAutonomousContainerDatabaseDetails.
        :type is_automatic_failover_enabled: bool

        :param peer_cloud_autonomous_vm_cluster_id:
            The value to assign to the peer_cloud_autonomous_vm_cluster_id property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_cloud_autonomous_vm_cluster_id: str

        :param peer_autonomous_vm_cluster_id:
            The value to assign to the peer_autonomous_vm_cluster_id property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_autonomous_vm_cluster_id: str

        :param peer_autonomous_container_database_compartment_id:
            The value to assign to the peer_autonomous_container_database_compartment_id property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_autonomous_container_database_compartment_id: str

        :param peer_autonomous_container_database_backup_config:
            The value to assign to the peer_autonomous_container_database_backup_config property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_autonomous_container_database_backup_config: oci.database.models.PeerAutonomousContainerDatabaseBackupConfig

        :param peer_db_unique_name:
            The value to assign to the peer_db_unique_name property of this CreateAutonomousContainerDatabaseDetails.
        :type peer_db_unique_name: str

        :param autonomous_vm_cluster_id:
            The value to assign to the autonomous_vm_cluster_id property of this CreateAutonomousContainerDatabaseDetails.
        :type autonomous_vm_cluster_id: str

        :param cloud_autonomous_vm_cluster_id:
            The value to assign to the cloud_autonomous_vm_cluster_id property of this CreateAutonomousContainerDatabaseDetails.
        :type cloud_autonomous_vm_cluster_id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateAutonomousContainerDatabaseDetails.
        :type compartment_id: str

        :param patch_model:
            The value to assign to the patch_model property of this CreateAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"
        :type patch_model: str

        :param maintenance_window_details:
            The value to assign to the maintenance_window_details property of this CreateAutonomousContainerDatabaseDetails.
        :type maintenance_window_details: oci.database.models.MaintenanceWindow

        :param standby_maintenance_buffer_in_days:
            The value to assign to the standby_maintenance_buffer_in_days property of this CreateAutonomousContainerDatabaseDetails.
        :type standby_maintenance_buffer_in_days: int

        :param version_preference:
            The value to assign to the version_preference property of this CreateAutonomousContainerDatabaseDetails.
            Allowed values for this property are: "NEXT_RELEASE_UPDATE", "LATEST_RELEASE_UPDATE"
        :type version_preference: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateAutonomousContainerDatabaseDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateAutonomousContainerDatabaseDetails.
        :type defined_tags: dict(str, dict(str, object))

        :param backup_config:
            The value to assign to the backup_config property of this CreateAutonomousContainerDatabaseDetails.
        :type backup_config: oci.database.models.AutonomousContainerDatabaseBackupConfig

        :param kms_key_id:
            The value to assign to the kms_key_id property of this CreateAutonomousContainerDatabaseDetails.
        :type kms_key_id: str

        :param kms_key_version_id:
            The value to assign to the kms_key_version_id property of this CreateAutonomousContainerDatabaseDetails.
        :type kms_key_version_id: str

        :param vault_id:
            The value to assign to the vault_id property of this CreateAutonomousContainerDatabaseDetails.
        :type vault_id: str

        :param key_store_id:
            The value to assign to the key_store_id property of this CreateAutonomousContainerDatabaseDetails.
        :type key_store_id: str

        """
        self.swagger_types = {
            'display_name': 'str',
            'db_unique_name': 'str',
            'db_name': 'str',
            'service_level_agreement_type': 'str',
            'autonomous_exadata_infrastructure_id': 'str',
            'db_version': 'str',
            'peer_autonomous_exadata_infrastructure_id': 'str',
            'peer_autonomous_container_database_display_name': 'str',
            'protection_mode': 'str',
            'fast_start_fail_over_lag_limit_in_seconds': 'int',
            'is_automatic_failover_enabled': 'bool',
            'peer_cloud_autonomous_vm_cluster_id': 'str',
            'peer_autonomous_vm_cluster_id': 'str',
            'peer_autonomous_container_database_compartment_id': 'str',
            'peer_autonomous_container_database_backup_config': 'PeerAutonomousContainerDatabaseBackupConfig',
            'peer_db_unique_name': 'str',
            'autonomous_vm_cluster_id': 'str',
            'cloud_autonomous_vm_cluster_id': 'str',
            'compartment_id': 'str',
            'patch_model': 'str',
            'maintenance_window_details': 'MaintenanceWindow',
            'standby_maintenance_buffer_in_days': 'int',
            'version_preference': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))',
            'backup_config': 'AutonomousContainerDatabaseBackupConfig',
            'kms_key_id': 'str',
            'kms_key_version_id': 'str',
            'vault_id': 'str',
            'key_store_id': 'str'
        }

        self.attribute_map = {
            'display_name': 'displayName',
            'db_unique_name': 'dbUniqueName',
            'db_name': 'dbName',
            'service_level_agreement_type': 'serviceLevelAgreementType',
            'autonomous_exadata_infrastructure_id': 'autonomousExadataInfrastructureId',
            'db_version': 'dbVersion',
            'peer_autonomous_exadata_infrastructure_id': 'peerAutonomousExadataInfrastructureId',
            'peer_autonomous_container_database_display_name': 'peerAutonomousContainerDatabaseDisplayName',
            'protection_mode': 'protectionMode',
            'fast_start_fail_over_lag_limit_in_seconds': 'fastStartFailOverLagLimitInSeconds',
            'is_automatic_failover_enabled': 'isAutomaticFailoverEnabled',
            'peer_cloud_autonomous_vm_cluster_id': 'peerCloudAutonomousVmClusterId',
            'peer_autonomous_vm_cluster_id': 'peerAutonomousVmClusterId',
            'peer_autonomous_container_database_compartment_id': 'peerAutonomousContainerDatabaseCompartmentId',
            'peer_autonomous_container_database_backup_config': 'peerAutonomousContainerDatabaseBackupConfig',
            'peer_db_unique_name': 'peerDbUniqueName',
            'autonomous_vm_cluster_id': 'autonomousVmClusterId',
            'cloud_autonomous_vm_cluster_id': 'cloudAutonomousVmClusterId',
            'compartment_id': 'compartmentId',
            'patch_model': 'patchModel',
            'maintenance_window_details': 'maintenanceWindowDetails',
            'standby_maintenance_buffer_in_days': 'standbyMaintenanceBufferInDays',
            'version_preference': 'versionPreference',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags',
            'backup_config': 'backupConfig',
            'kms_key_id': 'kmsKeyId',
            'kms_key_version_id': 'kmsKeyVersionId',
            'vault_id': 'vaultId',
            'key_store_id': 'keyStoreId'
        }

        self._display_name = None
        self._db_unique_name = None
        self._db_name = None
        self._service_level_agreement_type = None
        self._autonomous_exadata_infrastructure_id = None
        self._db_version = None
        self._peer_autonomous_exadata_infrastructure_id = None
        self._peer_autonomous_container_database_display_name = None
        self._protection_mode = None
        self._fast_start_fail_over_lag_limit_in_seconds = None
        self._is_automatic_failover_enabled = None
        self._peer_cloud_autonomous_vm_cluster_id = None
        self._peer_autonomous_vm_cluster_id = None
        self._peer_autonomous_container_database_compartment_id = None
        self._peer_autonomous_container_database_backup_config = None
        self._peer_db_unique_name = None
        self._autonomous_vm_cluster_id = None
        self._cloud_autonomous_vm_cluster_id = None
        self._compartment_id = None
        self._patch_model = None
        self._maintenance_window_details = None
        self._standby_maintenance_buffer_in_days = None
        self._version_preference = None
        self._freeform_tags = None
        self._defined_tags = None
        self._backup_config = None
        self._kms_key_id = None
        self._kms_key_version_id = None
        self._vault_id = None
        self._key_store_id = None

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateAutonomousContainerDatabaseDetails.
        The display name for the Autonomous Container Database.


        :return: The display_name of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateAutonomousContainerDatabaseDetails.
        The display name for the Autonomous Container Database.


        :param display_name: The display_name of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def db_unique_name(self):
        """
        Gets the db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        **Deprecated.** The `DB_UNIQUE_NAME` value is set by Oracle Cloud Infrastructure.  Do not specify a value for this parameter. Specifying a value for this field will cause Terraform operations to fail.


        :return: The db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._db_unique_name

    @db_unique_name.setter
    def db_unique_name(self, db_unique_name):
        """
        Sets the db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        **Deprecated.** The `DB_UNIQUE_NAME` value is set by Oracle Cloud Infrastructure.  Do not specify a value for this parameter. Specifying a value for this field will cause Terraform operations to fail.


        :param db_unique_name: The db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._db_unique_name = db_unique_name

    @property
    def db_name(self):
        """
        Gets the db_name of this CreateAutonomousContainerDatabaseDetails.
        The Database name for the Autonomous Container Database. The name must be unique within the Cloud Autonomous VM Cluster, starting with an alphabetic character, followed by 1 to 7 alphanumeric characters.


        :return: The db_name of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._db_name

    @db_name.setter
    def db_name(self, db_name):
        """
        Sets the db_name of this CreateAutonomousContainerDatabaseDetails.
        The Database name for the Autonomous Container Database. The name must be unique within the Cloud Autonomous VM Cluster, starting with an alphabetic character, followed by 1 to 7 alphanumeric characters.


        :param db_name: The db_name of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._db_name = db_name

    @property
    def service_level_agreement_type(self):
        """
        Gets the service_level_agreement_type of this CreateAutonomousContainerDatabaseDetails.
        The service level agreement type of the Autonomous Container Database. The default is STANDARD. For an autonomous dataguard Autonomous Container Database, the specified Autonomous Exadata Infrastructure must be associated with a remote Autonomous Exadata Infrastructure.

        Allowed values for this property are: "STANDARD", "AUTONOMOUS_DATAGUARD"


        :return: The service_level_agreement_type of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._service_level_agreement_type

    @service_level_agreement_type.setter
    def service_level_agreement_type(self, service_level_agreement_type):
        """
        Sets the service_level_agreement_type of this CreateAutonomousContainerDatabaseDetails.
        The service level agreement type of the Autonomous Container Database. The default is STANDARD. For an autonomous dataguard Autonomous Container Database, the specified Autonomous Exadata Infrastructure must be associated with a remote Autonomous Exadata Infrastructure.


        :param service_level_agreement_type: The service_level_agreement_type of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["STANDARD", "AUTONOMOUS_DATAGUARD"]
        if not value_allowed_none_or_none_sentinel(service_level_agreement_type, allowed_values):
            raise ValueError(
                "Invalid value for `service_level_agreement_type`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._service_level_agreement_type = service_level_agreement_type

    @property
    def autonomous_exadata_infrastructure_id(self):
        """
        Gets the autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        **No longer used.** This parameter is no longer used for Autonomous Database on dedicated Exadata infrasture. Specify a `cloudAutonomousVmClusterId` instead. Using this parameter will cause the operation to fail.


        :return: The autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._autonomous_exadata_infrastructure_id

    @autonomous_exadata_infrastructure_id.setter
    def autonomous_exadata_infrastructure_id(self, autonomous_exadata_infrastructure_id):
        """
        Sets the autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        **No longer used.** This parameter is no longer used for Autonomous Database on dedicated Exadata infrasture. Specify a `cloudAutonomousVmClusterId` instead. Using this parameter will cause the operation to fail.


        :param autonomous_exadata_infrastructure_id: The autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._autonomous_exadata_infrastructure_id = autonomous_exadata_infrastructure_id

    @property
    def db_version(self):
        """
        Gets the db_version of this CreateAutonomousContainerDatabaseDetails.
        The base version for the Autonomous Container Database.


        :return: The db_version of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._db_version

    @db_version.setter
    def db_version(self, db_version):
        """
        Sets the db_version of this CreateAutonomousContainerDatabaseDetails.
        The base version for the Autonomous Container Database.


        :param db_version: The db_version of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._db_version = db_version

    @property
    def peer_autonomous_exadata_infrastructure_id(self):
        """
        Gets the peer_autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        *No longer used.* This parameter is no longer used for Autonomous Database on dedicated Exadata infrasture. Specify a `peerCloudAutonomousVmClusterId` instead. Using this parameter will cause the operation to fail.


        :return: The peer_autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_autonomous_exadata_infrastructure_id

    @peer_autonomous_exadata_infrastructure_id.setter
    def peer_autonomous_exadata_infrastructure_id(self, peer_autonomous_exadata_infrastructure_id):
        """
        Sets the peer_autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        *No longer used.* This parameter is no longer used for Autonomous Database on dedicated Exadata infrasture. Specify a `peerCloudAutonomousVmClusterId` instead. Using this parameter will cause the operation to fail.


        :param peer_autonomous_exadata_infrastructure_id: The peer_autonomous_exadata_infrastructure_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_autonomous_exadata_infrastructure_id = peer_autonomous_exadata_infrastructure_id

    @property
    def peer_autonomous_container_database_display_name(self):
        """
        Gets the peer_autonomous_container_database_display_name of this CreateAutonomousContainerDatabaseDetails.
        The display name for the peer Autonomous Container Database.


        :return: The peer_autonomous_container_database_display_name of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_autonomous_container_database_display_name

    @peer_autonomous_container_database_display_name.setter
    def peer_autonomous_container_database_display_name(self, peer_autonomous_container_database_display_name):
        """
        Sets the peer_autonomous_container_database_display_name of this CreateAutonomousContainerDatabaseDetails.
        The display name for the peer Autonomous Container Database.


        :param peer_autonomous_container_database_display_name: The peer_autonomous_container_database_display_name of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_autonomous_container_database_display_name = peer_autonomous_container_database_display_name

    @property
    def protection_mode(self):
        """
        Gets the protection_mode of this CreateAutonomousContainerDatabaseDetails.
        The protection mode of this Autonomous Data Guard association. For more information, see
        `Oracle Data Guard Protection Modes`__
        in the Oracle Data Guard documentation.

        __ http://docs.oracle.com/database/122/SBYDB/oracle-data-guard-protection-modes.htm#SBYDB02000

        Allowed values for this property are: "MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"


        :return: The protection_mode of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._protection_mode

    @protection_mode.setter
    def protection_mode(self, protection_mode):
        """
        Sets the protection_mode of this CreateAutonomousContainerDatabaseDetails.
        The protection mode of this Autonomous Data Guard association. For more information, see
        `Oracle Data Guard Protection Modes`__
        in the Oracle Data Guard documentation.

        __ http://docs.oracle.com/database/122/SBYDB/oracle-data-guard-protection-modes.htm#SBYDB02000


        :param protection_mode: The protection_mode of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["MAXIMUM_AVAILABILITY", "MAXIMUM_PERFORMANCE"]
        if not value_allowed_none_or_none_sentinel(protection_mode, allowed_values):
            raise ValueError(
                "Invalid value for `protection_mode`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._protection_mode = protection_mode

    @property
    def fast_start_fail_over_lag_limit_in_seconds(self):
        """
        Gets the fast_start_fail_over_lag_limit_in_seconds of this CreateAutonomousContainerDatabaseDetails.
        The lag time for my preference based on data loss tolerance in seconds.


        :return: The fast_start_fail_over_lag_limit_in_seconds of this CreateAutonomousContainerDatabaseDetails.
        :rtype: int
        """
        return self._fast_start_fail_over_lag_limit_in_seconds

    @fast_start_fail_over_lag_limit_in_seconds.setter
    def fast_start_fail_over_lag_limit_in_seconds(self, fast_start_fail_over_lag_limit_in_seconds):
        """
        Sets the fast_start_fail_over_lag_limit_in_seconds of this CreateAutonomousContainerDatabaseDetails.
        The lag time for my preference based on data loss tolerance in seconds.


        :param fast_start_fail_over_lag_limit_in_seconds: The fast_start_fail_over_lag_limit_in_seconds of this CreateAutonomousContainerDatabaseDetails.
        :type: int
        """
        self._fast_start_fail_over_lag_limit_in_seconds = fast_start_fail_over_lag_limit_in_seconds

    @property
    def is_automatic_failover_enabled(self):
        """
        Gets the is_automatic_failover_enabled of this CreateAutonomousContainerDatabaseDetails.
        Indicates whether Automatic Failover is enabled for Autonomous Container Database Dataguard Association


        :return: The is_automatic_failover_enabled of this CreateAutonomousContainerDatabaseDetails.
        :rtype: bool
        """
        return self._is_automatic_failover_enabled

    @is_automatic_failover_enabled.setter
    def is_automatic_failover_enabled(self, is_automatic_failover_enabled):
        """
        Sets the is_automatic_failover_enabled of this CreateAutonomousContainerDatabaseDetails.
        Indicates whether Automatic Failover is enabled for Autonomous Container Database Dataguard Association


        :param is_automatic_failover_enabled: The is_automatic_failover_enabled of this CreateAutonomousContainerDatabaseDetails.
        :type: bool
        """
        self._is_automatic_failover_enabled = is_automatic_failover_enabled

    @property
    def peer_cloud_autonomous_vm_cluster_id(self):
        """
        Gets the peer_cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the peer cloud Autonomous Exadata VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The peer_cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_cloud_autonomous_vm_cluster_id

    @peer_cloud_autonomous_vm_cluster_id.setter
    def peer_cloud_autonomous_vm_cluster_id(self, peer_cloud_autonomous_vm_cluster_id):
        """
        Sets the peer_cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the peer cloud Autonomous Exadata VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param peer_cloud_autonomous_vm_cluster_id: The peer_cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_cloud_autonomous_vm_cluster_id = peer_cloud_autonomous_vm_cluster_id

    @property
    def peer_autonomous_vm_cluster_id(self):
        """
        Gets the peer_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the peer Autonomous VM cluster for Autonomous Data Guard. Required to enable Data Guard.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The peer_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_autonomous_vm_cluster_id

    @peer_autonomous_vm_cluster_id.setter
    def peer_autonomous_vm_cluster_id(self, peer_autonomous_vm_cluster_id):
        """
        Sets the peer_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the peer Autonomous VM cluster for Autonomous Data Guard. Required to enable Data Guard.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param peer_autonomous_vm_cluster_id: The peer_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_autonomous_vm_cluster_id = peer_autonomous_vm_cluster_id

    @property
    def peer_autonomous_container_database_compartment_id(self):
        """
        Gets the peer_autonomous_container_database_compartment_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the compartment where the standby Autonomous Container Database
        will be created.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The peer_autonomous_container_database_compartment_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_autonomous_container_database_compartment_id

    @peer_autonomous_container_database_compartment_id.setter
    def peer_autonomous_container_database_compartment_id(self, peer_autonomous_container_database_compartment_id):
        """
        Sets the peer_autonomous_container_database_compartment_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the compartment where the standby Autonomous Container Database
        will be created.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param peer_autonomous_container_database_compartment_id: The peer_autonomous_container_database_compartment_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_autonomous_container_database_compartment_id = peer_autonomous_container_database_compartment_id

    @property
    def peer_autonomous_container_database_backup_config(self):
        """
        Gets the peer_autonomous_container_database_backup_config of this CreateAutonomousContainerDatabaseDetails.

        :return: The peer_autonomous_container_database_backup_config of this CreateAutonomousContainerDatabaseDetails.
        :rtype: oci.database.models.PeerAutonomousContainerDatabaseBackupConfig
        """
        return self._peer_autonomous_container_database_backup_config

    @peer_autonomous_container_database_backup_config.setter
    def peer_autonomous_container_database_backup_config(self, peer_autonomous_container_database_backup_config):
        """
        Sets the peer_autonomous_container_database_backup_config of this CreateAutonomousContainerDatabaseDetails.

        :param peer_autonomous_container_database_backup_config: The peer_autonomous_container_database_backup_config of this CreateAutonomousContainerDatabaseDetails.
        :type: oci.database.models.PeerAutonomousContainerDatabaseBackupConfig
        """
        self._peer_autonomous_container_database_backup_config = peer_autonomous_container_database_backup_config

    @property
    def peer_db_unique_name(self):
        """
        Gets the peer_db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        **Deprecated.** The `DB_UNIQUE_NAME` of the peer Autonomous Container Database in a Data Guard association is set by Oracle Cloud Infrastructure.  Do not specify a value for this parameter. Specifying a value for this field will cause Terraform operations to fail.


        :return: The peer_db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._peer_db_unique_name

    @peer_db_unique_name.setter
    def peer_db_unique_name(self, peer_db_unique_name):
        """
        Sets the peer_db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        **Deprecated.** The `DB_UNIQUE_NAME` of the peer Autonomous Container Database in a Data Guard association is set by Oracle Cloud Infrastructure.  Do not specify a value for this parameter. Specifying a value for this field will cause Terraform operations to fail.


        :param peer_db_unique_name: The peer_db_unique_name of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._peer_db_unique_name = peer_db_unique_name

    @property
    def autonomous_vm_cluster_id(self):
        """
        Gets the autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the Autonomous VM Cluster.


        :return: The autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._autonomous_vm_cluster_id

    @autonomous_vm_cluster_id.setter
    def autonomous_vm_cluster_id(self, autonomous_vm_cluster_id):
        """
        Sets the autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the Autonomous VM Cluster.


        :param autonomous_vm_cluster_id: The autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._autonomous_vm_cluster_id = autonomous_vm_cluster_id

    @property
    def cloud_autonomous_vm_cluster_id(self):
        """
        Gets the cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the cloud Autonomous Exadata VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._cloud_autonomous_vm_cluster_id

    @cloud_autonomous_vm_cluster_id.setter
    def cloud_autonomous_vm_cluster_id(self, cloud_autonomous_vm_cluster_id):
        """
        Sets the cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the cloud Autonomous Exadata VM Cluster.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param cloud_autonomous_vm_cluster_id: The cloud_autonomous_vm_cluster_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._cloud_autonomous_vm_cluster_id = cloud_autonomous_vm_cluster_id

    @property
    def compartment_id(self):
        """
        Gets the compartment_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the compartment containing the Autonomous Container Database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the compartment containing the Autonomous Container Database.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def patch_model(self):
        """
        **[Required]** Gets the patch_model of this CreateAutonomousContainerDatabaseDetails.
        Database Patch model preference.

        Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"


        :return: The patch_model of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._patch_model

    @patch_model.setter
    def patch_model(self, patch_model):
        """
        Sets the patch_model of this CreateAutonomousContainerDatabaseDetails.
        Database Patch model preference.


        :param patch_model: The patch_model of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"]
        if not value_allowed_none_or_none_sentinel(patch_model, allowed_values):
            raise ValueError(
                "Invalid value for `patch_model`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._patch_model = patch_model

    @property
    def maintenance_window_details(self):
        """
        Gets the maintenance_window_details of this CreateAutonomousContainerDatabaseDetails.

        :return: The maintenance_window_details of this CreateAutonomousContainerDatabaseDetails.
        :rtype: oci.database.models.MaintenanceWindow
        """
        return self._maintenance_window_details

    @maintenance_window_details.setter
    def maintenance_window_details(self, maintenance_window_details):
        """
        Sets the maintenance_window_details of this CreateAutonomousContainerDatabaseDetails.

        :param maintenance_window_details: The maintenance_window_details of this CreateAutonomousContainerDatabaseDetails.
        :type: oci.database.models.MaintenanceWindow
        """
        self._maintenance_window_details = maintenance_window_details

    @property
    def standby_maintenance_buffer_in_days(self):
        """
        Gets the standby_maintenance_buffer_in_days of this CreateAutonomousContainerDatabaseDetails.
        The scheduling detail for the quarterly maintenance window of the standby Autonomous Container Database.
        This value represents the number of days before scheduled maintenance of the primary database.


        :return: The standby_maintenance_buffer_in_days of this CreateAutonomousContainerDatabaseDetails.
        :rtype: int
        """
        return self._standby_maintenance_buffer_in_days

    @standby_maintenance_buffer_in_days.setter
    def standby_maintenance_buffer_in_days(self, standby_maintenance_buffer_in_days):
        """
        Sets the standby_maintenance_buffer_in_days of this CreateAutonomousContainerDatabaseDetails.
        The scheduling detail for the quarterly maintenance window of the standby Autonomous Container Database.
        This value represents the number of days before scheduled maintenance of the primary database.


        :param standby_maintenance_buffer_in_days: The standby_maintenance_buffer_in_days of this CreateAutonomousContainerDatabaseDetails.
        :type: int
        """
        self._standby_maintenance_buffer_in_days = standby_maintenance_buffer_in_days

    @property
    def version_preference(self):
        """
        Gets the version_preference of this CreateAutonomousContainerDatabaseDetails.
        The next maintenance version preference.

        Allowed values for this property are: "NEXT_RELEASE_UPDATE", "LATEST_RELEASE_UPDATE"


        :return: The version_preference of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._version_preference

    @version_preference.setter
    def version_preference(self, version_preference):
        """
        Sets the version_preference of this CreateAutonomousContainerDatabaseDetails.
        The next maintenance version preference.


        :param version_preference: The version_preference of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        allowed_values = ["NEXT_RELEASE_UPDATE", "LATEST_RELEASE_UPDATE"]
        if not value_allowed_none_or_none_sentinel(version_preference, allowed_values):
            raise ValueError(
                "Invalid value for `version_preference`, must be None or one of {0}"
                .format(allowed_values)
            )
        self._version_preference = version_preference

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateAutonomousContainerDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateAutonomousContainerDatabaseDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateAutonomousContainerDatabaseDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateAutonomousContainerDatabaseDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateAutonomousContainerDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateAutonomousContainerDatabaseDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateAutonomousContainerDatabaseDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateAutonomousContainerDatabaseDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    @property
    def backup_config(self):
        """
        Gets the backup_config of this CreateAutonomousContainerDatabaseDetails.

        :return: The backup_config of this CreateAutonomousContainerDatabaseDetails.
        :rtype: oci.database.models.AutonomousContainerDatabaseBackupConfig
        """
        return self._backup_config

    @backup_config.setter
    def backup_config(self, backup_config):
        """
        Sets the backup_config of this CreateAutonomousContainerDatabaseDetails.

        :param backup_config: The backup_config of this CreateAutonomousContainerDatabaseDetails.
        :type: oci.database.models.AutonomousContainerDatabaseBackupConfig
        """
        self._backup_config = backup_config

    @property
    def kms_key_id(self):
        """
        Gets the kms_key_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the key container that is used as the master encryption key in database transparent data encryption (TDE) operations.


        :return: The kms_key_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._kms_key_id

    @kms_key_id.setter
    def kms_key_id(self, kms_key_id):
        """
        Sets the kms_key_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the key container that is used as the master encryption key in database transparent data encryption (TDE) operations.


        :param kms_key_id: The kms_key_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._kms_key_id = kms_key_id

    @property
    def kms_key_version_id(self):
        """
        Gets the kms_key_version_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the key container version that is used in database transparent data encryption (TDE) operations KMS Key can have multiple key versions. If none is specified, the current key version (latest) of the Key Id is used for the operation.


        :return: The kms_key_version_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._kms_key_version_id

    @kms_key_version_id.setter
    def kms_key_version_id(self, kms_key_version_id):
        """
        Sets the kms_key_version_id of this CreateAutonomousContainerDatabaseDetails.
        The OCID of the key container version that is used in database transparent data encryption (TDE) operations KMS Key can have multiple key versions. If none is specified, the current key version (latest) of the Key Id is used for the operation.


        :param kms_key_version_id: The kms_key_version_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._kms_key_version_id = kms_key_version_id

    @property
    def vault_id(self):
        """
        Gets the vault_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the Oracle Cloud Infrastructure `vault`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm
        __ https://docs.cloud.oracle.com/Content/KeyManagement/Concepts/keyoverview.htm#concepts


        :return: The vault_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._vault_id

    @vault_id.setter
    def vault_id(self, vault_id):
        """
        Sets the vault_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the Oracle Cloud Infrastructure `vault`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm
        __ https://docs.cloud.oracle.com/Content/KeyManagement/Concepts/keyoverview.htm#concepts


        :param vault_id: The vault_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._vault_id = vault_id

    @property
    def key_store_id(self):
        """
        Gets the key_store_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the key store.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The key_store_id of this CreateAutonomousContainerDatabaseDetails.
        :rtype: str
        """
        return self._key_store_id

    @key_store_id.setter
    def key_store_id(self, key_store_id):
        """
        Sets the key_store_id of this CreateAutonomousContainerDatabaseDetails.
        The `OCID`__ of the key store.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param key_store_id: The key_store_id of this CreateAutonomousContainerDatabaseDetails.
        :type: str
        """
        self._key_store_id = key_store_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
