# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateOneoffPatchDetails(object):
    """
    Data to create the one-off patch for the specificed database version.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateOneoffPatchDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateOneoffPatchDetails.
        :type compartment_id: str

        :param display_name:
            The value to assign to the display_name property of this CreateOneoffPatchDetails.
        :type display_name: str

        :param db_version:
            The value to assign to the db_version property of this CreateOneoffPatchDetails.
        :type db_version: str

        :param release_update:
            The value to assign to the release_update property of this CreateOneoffPatchDetails.
        :type release_update: str

        :param one_off_patches:
            The value to assign to the one_off_patches property of this CreateOneoffPatchDetails.
        :type one_off_patches: list[str]

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateOneoffPatchDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateOneoffPatchDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'compartment_id': 'str',
            'display_name': 'str',
            'db_version': 'str',
            'release_update': 'str',
            'one_off_patches': 'list[str]',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'compartment_id': 'compartmentId',
            'display_name': 'displayName',
            'db_version': 'dbVersion',
            'release_update': 'releaseUpdate',
            'one_off_patches': 'oneOffPatches',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._compartment_id = None
        self._display_name = None
        self._db_version = None
        self._release_update = None
        self._one_off_patches = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateOneoffPatchDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateOneoffPatchDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateOneoffPatchDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateOneoffPatchDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def display_name(self):
        """
        **[Required]** Gets the display_name of this CreateOneoffPatchDetails.
        One-off patch name.


        :return: The display_name of this CreateOneoffPatchDetails.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this CreateOneoffPatchDetails.
        One-off patch name.


        :param display_name: The display_name of this CreateOneoffPatchDetails.
        :type: str
        """
        self._display_name = display_name

    @property
    def db_version(self):
        """
        **[Required]** Gets the db_version of this CreateOneoffPatchDetails.
        A valid Oracle Database version. For a list of supported versions, use the ListDbVersions operation.

        This cannot be updated in parallel with any of the following: licenseModel, dbEdition, cpuCoreCount, computeCount, computeModel, adminPassword, whitelistedIps, isMTLSConnectionRequired, openMode, permissionLevel, dbWorkload, privateEndpointLabel, nsgIds, isRefreshable, dbName, scheduledOperations, dbToolsDetails, isLocalDataGuardEnabled, or isFreeTier.


        :return: The db_version of this CreateOneoffPatchDetails.
        :rtype: str
        """
        return self._db_version

    @db_version.setter
    def db_version(self, db_version):
        """
        Sets the db_version of this CreateOneoffPatchDetails.
        A valid Oracle Database version. For a list of supported versions, use the ListDbVersions operation.

        This cannot be updated in parallel with any of the following: licenseModel, dbEdition, cpuCoreCount, computeCount, computeModel, adminPassword, whitelistedIps, isMTLSConnectionRequired, openMode, permissionLevel, dbWorkload, privateEndpointLabel, nsgIds, isRefreshable, dbName, scheduledOperations, dbToolsDetails, isLocalDataGuardEnabled, or isFreeTier.


        :param db_version: The db_version of this CreateOneoffPatchDetails.
        :type: str
        """
        self._db_version = db_version

    @property
    def release_update(self):
        """
        **[Required]** Gets the release_update of this CreateOneoffPatchDetails.
        The PSU or PBP or Release Updates. To get a list of supported versions, use the :func:`list_db_versions` operation.


        :return: The release_update of this CreateOneoffPatchDetails.
        :rtype: str
        """
        return self._release_update

    @release_update.setter
    def release_update(self, release_update):
        """
        Sets the release_update of this CreateOneoffPatchDetails.
        The PSU or PBP or Release Updates. To get a list of supported versions, use the :func:`list_db_versions` operation.


        :param release_update: The release_update of this CreateOneoffPatchDetails.
        :type: str
        """
        self._release_update = release_update

    @property
    def one_off_patches(self):
        """
        Gets the one_off_patches of this CreateOneoffPatchDetails.
        List of one-off patches for Database Homes.


        :return: The one_off_patches of this CreateOneoffPatchDetails.
        :rtype: list[str]
        """
        return self._one_off_patches

    @one_off_patches.setter
    def one_off_patches(self, one_off_patches):
        """
        Sets the one_off_patches of this CreateOneoffPatchDetails.
        List of one-off patches for Database Homes.


        :param one_off_patches: The one_off_patches of this CreateOneoffPatchDetails.
        :type: list[str]
        """
        self._one_off_patches = one_off_patches

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateOneoffPatchDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The freeform_tags of this CreateOneoffPatchDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateOneoffPatchDetails.
        Free-form tags for this resource. Each tag is a simple key-value pair with no predefined name, type, or namespace.
        For more information, see `Resource Tags`__.

        Example: `{\"Department\": \"Finance\"}`

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param freeform_tags: The freeform_tags of this CreateOneoffPatchDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateOneoffPatchDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :return: The defined_tags of this CreateOneoffPatchDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateOneoffPatchDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        For more information, see `Resource Tags`__.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/resourcetags.htm


        :param defined_tags: The defined_tags of this CreateOneoffPatchDetails.
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
