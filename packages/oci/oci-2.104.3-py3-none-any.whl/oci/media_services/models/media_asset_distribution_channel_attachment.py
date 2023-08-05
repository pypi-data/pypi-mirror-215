# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class MediaAssetDistributionChannelAttachment(object):
    """
    Attachment between MediaAsset and streaming DistributionChannel.
    """

    #: A constant which can be used with the lifecycle_state property of a MediaAssetDistributionChannelAttachment.
    #: This constant has a value of "CREATING"
    LIFECYCLE_STATE_CREATING = "CREATING"

    #: A constant which can be used with the lifecycle_state property of a MediaAssetDistributionChannelAttachment.
    #: This constant has a value of "ACTIVE"
    LIFECYCLE_STATE_ACTIVE = "ACTIVE"

    #: A constant which can be used with the lifecycle_state property of a MediaAssetDistributionChannelAttachment.
    #: This constant has a value of "NEEDS_ATTENTION"
    LIFECYCLE_STATE_NEEDS_ATTENTION = "NEEDS_ATTENTION"

    #: A constant which can be used with the lifecycle_state property of a MediaAssetDistributionChannelAttachment.
    #: This constant has a value of "UPDATING"
    LIFECYCLE_STATE_UPDATING = "UPDATING"

    def __init__(self, **kwargs):
        """
        Initializes a new MediaAssetDistributionChannelAttachment object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param distribution_channel_id:
            The value to assign to the distribution_channel_id property of this MediaAssetDistributionChannelAttachment.
        :type distribution_channel_id: str

        :param display_name:
            The value to assign to the display_name property of this MediaAssetDistributionChannelAttachment.
        :type display_name: str

        :param version:
            The value to assign to the version property of this MediaAssetDistributionChannelAttachment.
        :type version: int

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this MediaAssetDistributionChannelAttachment.
            Allowed values for this property are: "CREATING", "ACTIVE", "NEEDS_ATTENTION", "UPDATING", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type lifecycle_state: str

        :param metadata_ref:
            The value to assign to the metadata_ref property of this MediaAssetDistributionChannelAttachment.
        :type metadata_ref: str

        :param media_workflow_job_id:
            The value to assign to the media_workflow_job_id property of this MediaAssetDistributionChannelAttachment.
        :type media_workflow_job_id: str

        """
        self.swagger_types = {
            'distribution_channel_id': 'str',
            'display_name': 'str',
            'version': 'int',
            'lifecycle_state': 'str',
            'metadata_ref': 'str',
            'media_workflow_job_id': 'str'
        }

        self.attribute_map = {
            'distribution_channel_id': 'distributionChannelId',
            'display_name': 'displayName',
            'version': 'version',
            'lifecycle_state': 'lifecycleState',
            'metadata_ref': 'metadataRef',
            'media_workflow_job_id': 'mediaWorkflowJobId'
        }

        self._distribution_channel_id = None
        self._display_name = None
        self._version = None
        self._lifecycle_state = None
        self._metadata_ref = None
        self._media_workflow_job_id = None

    @property
    def distribution_channel_id(self):
        """
        **[Required]** Gets the distribution_channel_id of this MediaAssetDistributionChannelAttachment.
        OCID of associated Distribution Channel.


        :return: The distribution_channel_id of this MediaAssetDistributionChannelAttachment.
        :rtype: str
        """
        return self._distribution_channel_id

    @distribution_channel_id.setter
    def distribution_channel_id(self, distribution_channel_id):
        """
        Sets the distribution_channel_id of this MediaAssetDistributionChannelAttachment.
        OCID of associated Distribution Channel.


        :param distribution_channel_id: The distribution_channel_id of this MediaAssetDistributionChannelAttachment.
        :type: str
        """
        self._distribution_channel_id = distribution_channel_id

    @property
    def display_name(self):
        """
        Gets the display_name of this MediaAssetDistributionChannelAttachment.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :return: The display_name of this MediaAssetDistributionChannelAttachment.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this MediaAssetDistributionChannelAttachment.
        A user-friendly name. Does not have to be unique, and it's changeable. Avoid entering confidential information.


        :param display_name: The display_name of this MediaAssetDistributionChannelAttachment.
        :type: str
        """
        self._display_name = display_name

    @property
    def version(self):
        """
        **[Required]** Gets the version of this MediaAssetDistributionChannelAttachment.
        Version of the attachment.


        :return: The version of this MediaAssetDistributionChannelAttachment.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this MediaAssetDistributionChannelAttachment.
        Version of the attachment.


        :param version: The version of this MediaAssetDistributionChannelAttachment.
        :type: int
        """
        self._version = version

    @property
    def lifecycle_state(self):
        """
        **[Required]** Gets the lifecycle_state of this MediaAssetDistributionChannelAttachment.
        Lifecycle state of the attachment.

        Allowed values for this property are: "CREATING", "ACTIVE", "NEEDS_ATTENTION", "UPDATING", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The lifecycle_state of this MediaAssetDistributionChannelAttachment.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this MediaAssetDistributionChannelAttachment.
        Lifecycle state of the attachment.


        :param lifecycle_state: The lifecycle_state of this MediaAssetDistributionChannelAttachment.
        :type: str
        """
        allowed_values = ["CREATING", "ACTIVE", "NEEDS_ATTENTION", "UPDATING"]
        if not value_allowed_none_or_none_sentinel(lifecycle_state, allowed_values):
            lifecycle_state = 'UNKNOWN_ENUM_VALUE'
        self._lifecycle_state = lifecycle_state

    @property
    def metadata_ref(self):
        """
        **[Required]** Gets the metadata_ref of this MediaAssetDistributionChannelAttachment.
        The identifier for the metadata.


        :return: The metadata_ref of this MediaAssetDistributionChannelAttachment.
        :rtype: str
        """
        return self._metadata_ref

    @metadata_ref.setter
    def metadata_ref(self, metadata_ref):
        """
        Sets the metadata_ref of this MediaAssetDistributionChannelAttachment.
        The identifier for the metadata.


        :param metadata_ref: The metadata_ref of this MediaAssetDistributionChannelAttachment.
        :type: str
        """
        self._metadata_ref = metadata_ref

    @property
    def media_workflow_job_id(self):
        """
        Gets the media_workflow_job_id of this MediaAssetDistributionChannelAttachment.
        The ingest MediaWorkflowJob ID that created this attachment.


        :return: The media_workflow_job_id of this MediaAssetDistributionChannelAttachment.
        :rtype: str
        """
        return self._media_workflow_job_id

    @media_workflow_job_id.setter
    def media_workflow_job_id(self, media_workflow_job_id):
        """
        Sets the media_workflow_job_id of this MediaAssetDistributionChannelAttachment.
        The ingest MediaWorkflowJob ID that created this attachment.


        :param media_workflow_job_id: The media_workflow_job_id of this MediaAssetDistributionChannelAttachment.
        :type: str
        """
        self._media_workflow_job_id = media_workflow_job_id

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
