# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .work_item_details import WorkItemDetails
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class ApplicationWorkItemDetails(WorkItemDetails):
    """
    The work item details with JFR related information.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new ApplicationWorkItemDetails object with values from keyword arguments. The default value of the :py:attr:`~oci.jms.models.ApplicationWorkItemDetails.kind` attribute
        of this class is ``APPLICATION`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param kind:
            The value to assign to the kind property of this ApplicationWorkItemDetails.
            Allowed values for this property are: "BASIC", "APPLICATION"
        :type kind: str

        :param work_item_type:
            The value to assign to the work_item_type property of this ApplicationWorkItemDetails.
            Allowed values for this property are: "LCM", "JFR_CAPTURE", "JFR_UPLOAD", "CRYPTO_ANALYSIS", "CRYPTO_ANALYSIS_MERGE", "ADVANCED_USAGE_TRACKING", "PERFORMANCE_TUNING", "JMIGRATE_ANALYSIS"
        :type work_item_type: str

        :param application_key:
            The value to assign to the application_key property of this ApplicationWorkItemDetails.
        :type application_key: str

        :param application_installation_key:
            The value to assign to the application_installation_key property of this ApplicationWorkItemDetails.
        :type application_installation_key: str

        :param application_name:
            The value to assign to the application_name property of this ApplicationWorkItemDetails.
        :type application_name: str

        :param application_installation_path:
            The value to assign to the application_installation_path property of this ApplicationWorkItemDetails.
        :type application_installation_path: str

        """
        self.swagger_types = {
            'kind': 'str',
            'work_item_type': 'str',
            'application_key': 'str',
            'application_installation_key': 'str',
            'application_name': 'str',
            'application_installation_path': 'str'
        }

        self.attribute_map = {
            'kind': 'kind',
            'work_item_type': 'workItemType',
            'application_key': 'applicationKey',
            'application_installation_key': 'applicationInstallationKey',
            'application_name': 'applicationName',
            'application_installation_path': 'applicationInstallationPath'
        }

        self._kind = None
        self._work_item_type = None
        self._application_key = None
        self._application_installation_key = None
        self._application_name = None
        self._application_installation_path = None
        self._kind = 'APPLICATION'

    @property
    def application_key(self):
        """
        **[Required]** Gets the application_key of this ApplicationWorkItemDetails.
        The unique key of the application of the JFR.


        :return: The application_key of this ApplicationWorkItemDetails.
        :rtype: str
        """
        return self._application_key

    @application_key.setter
    def application_key(self, application_key):
        """
        Sets the application_key of this ApplicationWorkItemDetails.
        The unique key of the application of the JFR.


        :param application_key: The application_key of this ApplicationWorkItemDetails.
        :type: str
        """
        self._application_key = application_key

    @property
    def application_installation_key(self):
        """
        Gets the application_installation_key of this ApplicationWorkItemDetails.
        The unique key of the application installation of the JFR.


        :return: The application_installation_key of this ApplicationWorkItemDetails.
        :rtype: str
        """
        return self._application_installation_key

    @application_installation_key.setter
    def application_installation_key(self, application_installation_key):
        """
        Sets the application_installation_key of this ApplicationWorkItemDetails.
        The unique key of the application installation of the JFR.


        :param application_installation_key: The application_installation_key of this ApplicationWorkItemDetails.
        :type: str
        """
        self._application_installation_key = application_installation_key

    @property
    def application_name(self):
        """
        **[Required]** Gets the application_name of this ApplicationWorkItemDetails.
        The application name.


        :return: The application_name of this ApplicationWorkItemDetails.
        :rtype: str
        """
        return self._application_name

    @application_name.setter
    def application_name(self, application_name):
        """
        Sets the application_name of this ApplicationWorkItemDetails.
        The application name.


        :param application_name: The application_name of this ApplicationWorkItemDetails.
        :type: str
        """
        self._application_name = application_name

    @property
    def application_installation_path(self):
        """
        Gets the application_installation_path of this ApplicationWorkItemDetails.
        The full path on which application installation was detected.


        :return: The application_installation_path of this ApplicationWorkItemDetails.
        :rtype: str
        """
        return self._application_installation_path

    @application_installation_path.setter
    def application_installation_path(self, application_installation_path):
        """
        Sets the application_installation_path of this ApplicationWorkItemDetails.
        The full path on which application installation was detected.


        :param application_installation_path: The application_installation_path of this ApplicationWorkItemDetails.
        :type: str
        """
        self._application_installation_path = application_installation_path

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
