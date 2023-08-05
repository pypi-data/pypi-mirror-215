# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class OneoffPatch(object):
    """
    One-off patches are created by specifying a database version, releaseUpdate and one-off patch number.
    """

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "AVAILABLE"
    LIFECYCLE_STATE_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "INACTIVE"
    LIFECYCLE_STATE_INACTIVE = "INACTIVE"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "EXPIRED"
    LIFECYCLE_STATE_EXPIRED = "EXPIRED"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "DELETING"
    LIFECYCLE_STATE_DELETING = "DELETING"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "DELETED"
    LIFECYCLE_STATE_DELETED = "DELETED"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "TERMINATING"
    LIFECYCLE_STATE_TERMINATING = "TERMINATING"

    #: A constant which can be used with the lifecycle_state property of a OneoffPatch.
    #: This constant has a value of "TERMINATED"
    LIFECYCLE_STATE_TERMINATED = "TERMINATED"

    def __init__(self, **kwargs):
        """
        Initializes a new OneoffPatch object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this OneoffPatch.
        :type id: str

        :param compartment_id:
            The value to assign to the compartment_id property of this OneoffPatch.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this OneoffPatch.
        :type display_name: str

        :param db_version:
            The value to assign to the db_version property of this OneoffPatch.
        :type db_version: str

        :param release_update:
            The value to assign to the release_update property of this OneoffPatch.
        :type release_update: str

        :param one_off_patches:
            The value to assign to the one_off_patches property of this OneoffPatch.
        :type one_off_patches: list[str]

        :param size_in_kbs:
            The value to assign to the size_in_kbs property of this OneoffPatch.
        :type size_in_kbs: float

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this OneoffPatch.
            Allowed values for this property are: "CREATING", "AVAILABLE", "UPDATING", "INACTIVE", "FAILED", "EXPIRED", "DELETING", "DELETED", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this OneoffPatch.
        :type lifecycle_details: str

        :param sha256_sum:
            The value to assign to the sha256_sum property of this OneoffPatch.
        :type sha256_sum: str

        :param time_updated:
            The value to assign to the time_updated property of this OneoffPatch.
        :type time_updated: datetime

        :param time_created:
            The value to assign to the time_created property of this OneoffPatch.
        :type time_created: datetime

        :param time_of_expiration:
            The value to assign to the time_of_expiration property of this OneoffPatch.
        :type time_of_expiration: datetime

        :param freeform_tags:
            The value to assign to the freeform_tags property of this OneoffPatch.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this OneoffPatch.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'id': 'str',
            'compartment_id': 'str',
            'display_name': 'str',
            'db_version': 'str',
            'release_update': 'str',
            'one_off_patches': 'list[str]',
            'size_in_kbs': 'float',
            'lifecycle_state': 'str',
            'lifecycle_details': 'str',
            'sha256_sum': 'str',
            'time_updated': 'datetime',
            'time_created': 'datetime',
            'time_of_expiration': 'datetime',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'id': 'id',
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'db_version': 'dbVersion',
            'release_update': 'releaseUpdate',
            'one_off_patches': 'oneOffPatches',
            'size_in_kbs': 'sizeInKBs',
            'lifecycle_state': 'lifecycleState',
            'lifecycle_details': 'lifecycleDetails',
            'sha256_sum': 'sha256Sum',
            'time_updated': 'timeUpdated',
            'time_created': 'timeCreated',
            'time_of_expiration': 'timeOfExpiration',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._id = None
        self._compartment_id = None
        self._display_name = None
        self._db_version = None
        self._release_update = None
        self._one_off_patches = None
        self._size_in_kbs = None
        self._lifecycle_state = None
        self._lifecycle_details = None
        self._sha256_sum = None
        self._time_updated = None
        self._time_created = None
        self._time_of_expiration = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this OneoffPatch.
        The `OCID`__ of the one-off patch.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this OneoffPatch.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this OneoffPatch.
        The `OCID`__ of the one-off patch.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this OneoffPatch.
        :type: str
        """
        self._id = id

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this OneoffPatch.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this OneoffPatch.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this OneoffPatch.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this OneoffPatch.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this OneoffPatch.
        One-off patch name.


        :return: The display_name of this OneoffPatch.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this OneoffPatch.
        One-off patch name.


        :param display_name: The display_name of this OneoffPatch.
        :type: str
        """
        self._display_name = display_name

    @property
    def db_version(self):
        """
        **[Required]** Gets the db_version of this OneoffPatch.
        A valid Oracle Database version. For a list of supported versions, use the ListDbVersions operation.

        This cannot be updated in parallel with any of the following: licenseModel, dbEdition, cpuCoreCount, computeCount, computeModel, adminPassword, whitelistedIps, isMTLSConnectionRequired, openMode, permissionLevel, dbWorkload, privateEndpointLabel, nsgIds, isRefreshable, dbName, scheduledOperations, dbToolsDetails, isLocalDataGuardEnabled, or isFreeTier.


        :return: The db_version of this OneoffPatch.
        :rtype: str
        """
        return self._db_version

    @db_version.setter
    def db_version(self, db_version):
        """
        Sets the db_version of this OneoffPatch.
        A valid Oracle Database version. For a list of supported versions, use the ListDbVersions operation.

        This cannot be updated in parallel with any of the following: licenseModel, dbEdition, cpuCoreCount, computeCount, computeModel, adminPassword, whitelistedIps, isMTLSConnectionRequired, openMode, permissionLevel, dbWorkload, privateEndpointLabel, nsgIds, isRefreshable, dbName, scheduledOperations, dbToolsDetails, isLocalDataGuardEnabled, or isFreeTier.


        :param db_version: The db_version of this OneoffPatch.
        :type: str
        """
        self._db_version = db_version

    @property
    def release_update(self):
        """
        **[Required]** Gets the release_update of this OneoffPatch.
        The PSU or PBP or Release Updates. To get a list of supported versions, use the :func:`list_db_versions` operation.


        :return: The release_update of this OneoffPatch.
        :rtype: str
        """
        return self._release_update

    @release_update.setter
    def release_update(self, release_update):
        """
        Sets the release_update of this OneoffPatch.
        The PSU or PBP or Release Updates. To get a list of supported versions, use the :func:`list_db_versions` operation.


        :param release_update: The release_update of this OneoffPatch.
        :type: str
        """
        self._release_update = release_update

    @property
    def one_off_patches(self):
        """
        Gets the one_off_patches of this OneoffPatch.
        List of one-off patches for Database Homes.


        :return: The one_off_patches of this OneoffPatch.
        :rtype: list[str]
        """
        return self._one_off_patches

    @one_off_patches.setter
    def one_off_patches(self, one_off_patches):
        """
        Sets the one_off_patches of this OneoffPatch.
        List of one-off patches for Database Homes.


        :param one_off_patches: The one_off_patches of this OneoffPatch.
        :type: list[str]
        """
        self._one_off_patches = one_off_patches

    @property
    def size_in_kbs(self):
        """
        Gets the size_in_kbs of this OneoffPatch.
        The size of one-off patch in kilobytes.


        :return: The size_in_kbs of this OneoffPatch.
        :rtype: float
        """
        return self._size_in_kbs

    @size_in_kbs.setter
    def size_in_kbs(self, size_in_kbs):
        """
        Sets the size_in_kbs of this OneoffPatch.
        The size of one-off patch in kilobytes.


        :param size_in_kbs: The size_in_kbs of this OneoffPatch.
        :type: float
        """
        self._size_in_kbs = size_in_kbs

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this OneoffPatch.
        The current state of the one-off patch.

        Allowed values for this property are: "CREATING", "AVAILABLE", "UPDATING", "INACTIVE", "FAILED", "EXPIRED", "DELETING", "DELETED", "TERMINATING", "TERMINATED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this OneoffPatch.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this OneoffPatch.
        The current state of the one-off patch.


        :param lifecycle_state: The lifecycle_state of this OneoffPatch.
        :type: str
        """
        allowed_values = ["CREATING", "AVAILABLE", "UPDATING", "INACTIVE", "FAILED", "EXPIRED", "DELETING", "DELETED", "TERMINATING", "TERMINATED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this OneoffPatch.
        Detailed message for the lifecycle state.


        :return: The lifecycle_details of this OneoffPatch.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this OneoffPatch.
        Detailed message for the lifecycle state.


        :param lifecycle_details: The lifecycle_details of this OneoffPatch.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def sha256_sum(self):
        """
        Gets the sha256_sum of this OneoffPatch.
        SHA-256 checksum of the one-off patch.


        :return: The sha256_sum of this OneoffPatch.
        :rtype: str
        """
        return self._sha256_sum

    @sha256_sum.setter
    def sha256_sum(self, sha256_sum):
        """
        Sets the sha256_sum of this OneoffPatch.
        SHA-256 checksum of the one-off patch.


        :param sha256_sum: The sha256_sum of this OneoffPatch.
        :type: str
        """
        self._sha256_sum = sha256_sum

    @property
    def time_updated(self):
        """
        Gets the time_updated of this OneoffPatch.
        The date and time one-off patch was updated.


        :return: The time_updated of this OneoffPatch.
        :rtype: datetime
        """
        return self._time_updated

    @time_updated.setter
    def time_updated(self, time_updated):
        """
        Sets the time_updated of this OneoffPatch.
        The date and time one-off patch was updated.


        :param time_updated: The time_updated of this OneoffPatch.
        :type: datetime
        """
        self._time_updated = time_updated

    @property
    def time_created(self):
        """
        **[Required]** Gets the time_created of this OneoffPatch.
        The date and time one-off patch was created.


        :return: The time_created of this OneoffPatch.
        :rtype: datetime
        """
        return self._time_created

    @time_created.setter
    def time_created(self, time_created):
        """
        Sets the time_created of this OneoffPatch.
        The date and time one-off patch was created.


        :param time_created: The time_created of this OneoffPatch.
        :type: datetime
        """
        self._time_created = time_created

    @property
    def time_of_expiration(self):
        """
        Gets the time_of_expiration of this OneoffPatch.
        The date and time until which the one-off patch will be available for download.


        :return: The time_of_expiration of this OneoffPatch.
        :rtype: datetime
        """
        return self._time_of_expiration

    @time_of_expiration.setter
    def time_of_expiration(self, time_of_expiration):
        """
        Sets the time_of_expiration of this OneoffPatch.
        The date and time until which the one-off patch will be available for download.


        :param time_of_expiration: The time_of_expiration of this OneoffPatch.
        :type: datetime
        """
        self._time_of_expiration = time_of_expiration

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this OneoffPatch.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this OneoffPatch.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this OneoffPatch.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this OneoffPatch.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this OneoffPatch.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this OneoffPatch.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this OneoffPatch.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this OneoffPatch.
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
