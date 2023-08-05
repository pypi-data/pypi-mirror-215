# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AutonomousPatch(object):
    """
    AutonomousPatch model.
    """

    #: A constant which can be used with the lifecycle_state property of a AutonomousPatch.
    #: This constant has a value of "AVAILABLE"
    LIFECYCLE_STATE_AVAILABLE = "AVAILABLE"

    #: A constant which can be used with the lifecycle_state property of a AutonomousPatch.
    #: This constant has a value of "SUCCESS"
    LIFECYCLE_STATE_SUCCESS = "SUCCESS"

    #: A constant which can be used with the lifecycle_state property of a AutonomousPatch.
    #: This constant has a value of "IN_PROGRESS"
    LIFECYCLE_STATE_IN_PROGRESS = "IN_PROGRESS"

    #: A constant which can be used with the lifecycle_state property of a AutonomousPatch.
    #: This constant has a value of "FAILED"
    LIFECYCLE_STATE_FAILED = "FAILED"

    #: A constant which can be used with the patch_model property of a AutonomousPatch.
    #: This constant has a value of "RELEASE_UPDATES"
    PATCH_MODEL_RELEASE_UPDATES = "RELEASE_UPDATES"

    #: A constant which can be used with the patch_model property of a AutonomousPatch.
    #: This constant has a value of "RELEASE_UPDATE_REVISIONS"
    PATCH_MODEL_RELEASE_UPDATE_REVISIONS = "RELEASE_UPDATE_REVISIONS"

    def __init__(self, **kwargs):
        """
        Initializes a new AutonomousPatch object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param id:
            The value to assign to the id property of this AutonomousPatch.
        :type id: str

        :param description:
            The value to assign to the description property of this AutonomousPatch.
        :type description: str

        :param type:
            The value to assign to the type property of this AutonomousPatch.
        :type type: str

        :param lifecycle_details:
            The value to assign to the lifecycle_details property of this AutonomousPatch.
        :type lifecycle_details: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this AutonomousPatch.
            Allowed values for this property are: "AVAILABLE", "SUCCESS", "IN_PROGRESS", "FAILED", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param time_released:
            The value to assign to the time_released property of this AutonomousPatch.
        :type time_released: datetime

        :param version:
            The value to assign to the version property of this AutonomousPatch.
        :type version: str

        :param patch_model:
            The value to assign to the patch_model property of this AutonomousPatch.
            Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type patch_model: str

        :param quarter:
            The value to assign to the quarter property of this AutonomousPatch.
        :type quarter: str

        :param year:
            The value to assign to the year property of this AutonomousPatch.
        :type year: str

        """
        self.swagger_types = {
            'id': 'str',
            'description': 'str',
            'type': 'str',
            'lifecycle_details': 'str',
            'lifecycle_state': 'str',
            'time_released': 'datetime',
            'version': 'str',
            'patch_model': 'str',
            'quarter': 'str',
            'year': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'description': 'description',
            'type': 'type',
            'lifecycle_details': 'lifecycleDetails',
            'lifecycle_state': 'lifecycleState',
            'time_released': 'timeReleased',
            'version': 'version',
            'patch_model': 'patchModel',
            'quarter': 'quarter',
            'year': 'year'
        }

        self._id = None
        self._description = None
        self._type = None
        self._lifecycle_details = None
        self._lifecycle_state = None
        self._time_released = None
        self._version = None
        self._patch_model = None
        self._quarter = None
        self._year = None

    @property
    def id(self):
        """
        **[Required]** Gets the id of this AutonomousPatch.
        The `OCID`__ of the patch.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The id of this AutonomousPatch.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AutonomousPatch.
        The `OCID`__ of the patch.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param id: The id of this AutonomousPatch.
        :type: str
        """
        self._id = id

    @property
    def description(self):
        """
        **[Required]** Gets the description of this AutonomousPatch.
        The text describing this patch package.


        :return: The description of this AutonomousPatch.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AutonomousPatch.
        The text describing this patch package.


        :param description: The description of this AutonomousPatch.
        :type: str
        """
        self._description = description

    @property
    def type(self):
        """
        **[Required]** Gets the type of this AutonomousPatch.
        The type of patch. BUNDLE is one example.


        :return: The type of this AutonomousPatch.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AutonomousPatch.
        The type of patch. BUNDLE is one example.


        :param type: The type of this AutonomousPatch.
        :type: str
        """
        self._type = type

    @property
    def lifecycle_details(self):
        """
        Gets the lifecycle_details of this AutonomousPatch.
        A descriptive text associated with the lifecycleState.
        Typically can contain additional displayable text.


        :return: The lifecycle_details of this AutonomousPatch.
        :rtype: str
        """
        return self._lifecycle_details

    @lifecycle_details.setter
    def lifecycle_details(self, lifecycle_details):
        """
        Sets the lifecycle_details of this AutonomousPatch.
        A descriptive text associated with the lifecycleState.
        Typically can contain additional displayable text.


        :param lifecycle_details: The lifecycle_details of this AutonomousPatch.
        :type: str
        """
        self._lifecycle_details = lifecycle_details

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this AutonomousPatch.
        The current state of the patch as a result of lastAction.

        Allowed values for this property are: "AVAILABLE", "SUCCESS", "IN_PROGRESS", "FAILED", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this AutonomousPatch.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this AutonomousPatch.
        The current state of the patch as a result of lastAction.


        :param lifecycle_state: The lifecycle_state of this AutonomousPatch.
        :type: str
        """
        allowed_values = ["AVAILABLE", "SUCCESS", "IN_PROGRESS", "FAILED"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def time_released(self):
        """
        **[Required]** Gets the time_released of this AutonomousPatch.
        The date and time that the patch was released.


        :return: The time_released of this AutonomousPatch.
        :rtype: datetime
        """
        return self._time_released

    @time_released.setter
    def time_released(self, time_released):
        """
        Sets the time_released of this AutonomousPatch.
        The date and time that the patch was released.


        :param time_released: The time_released of this AutonomousPatch.
        :type: datetime
        """
        self._time_released = time_released

    @property
    def version(self):
        """
        **[Required]** Gets the version of this AutonomousPatch.
        The version of this patch package.


        :return: The version of this AutonomousPatch.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this AutonomousPatch.
        The version of this patch package.


        :param version: The version of this AutonomousPatch.
        :type: str
        """
        self._version = version

    @property
    def patch_model(self):
        """
        Gets the patch_model of this AutonomousPatch.
        Database patching model preference. See `My Oracle Support note 2285040.1`__ for information on the Release Update (RU) and Release Update Revision (RUR) patching models.

        __ https://support.oracle.com/rs?type=doc&id=2285040.1

        Allowed values for this property are: "RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The patch_model of this AutonomousPatch.
        :rtype: str
        """
        return self._patch_model

    @patch_model.setter
    def patch_model(self, patch_model):
        """
        Sets the patch_model of this AutonomousPatch.
        Database patching model preference. See `My Oracle Support note 2285040.1`__ for information on the Release Update (RU) and Release Update Revision (RUR) patching models.

        __ https://support.oracle.com/rs?type=doc&id=2285040.1


        :param patch_model: The patch_model of this AutonomousPatch.
        :type: str
        """
        allowed_values = ["RELEASE_UPDATES", "RELEASE_UPDATE_REVISIONS"]
        if not value_allowed_none_or_none_sentinel(patch_model, allowed_values):
            patch_model = 'UNKNOWN_ENUM_VALUE'
        self._patch_model = patch_model

    @property
    def quarter(self):
        """
        Gets the quarter of this AutonomousPatch.
        First month of the quarter in which the patch was released.


        :return: The quarter of this AutonomousPatch.
        :rtype: str
        """
        return self._quarter

    @quarter.setter
    def quarter(self, quarter):
        """
        Sets the quarter of this AutonomousPatch.
        First month of the quarter in which the patch was released.


        :param quarter: The quarter of this AutonomousPatch.
        :type: str
        """
        self._quarter = quarter

    @property
    def year(self):
        """
        Gets the year of this AutonomousPatch.
        Year in which the patch was released.


        :return: The year of this AutonomousPatch.
        :rtype: str
        """
        return self._year

    @year.setter
    def year(self, year):
        """
        Sets the year of this AutonomousPatch.
        Year in which the patch was released.


        :param year: The year of this AutonomousPatch.
        :type: str
        """
        self._year = year

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
