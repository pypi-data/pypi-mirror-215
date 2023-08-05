# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PeerSummary(object):
    """
    Peer summary information for returning in a list.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PeerSummary object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param peer_key:
            The value to assign to the peer_key property of this PeerSummary.
        :type peer_key: str

        :param lifecycle_state:
            The value to assign to the lifecycle_state property of this PeerSummary.
        :type lifecycle_state: str

        """
        self.swagger_types = {
            'peer_key': 'str',
            'lifecycle_state': 'str'
        }

        self.attribute_map = {
            'peer_key': 'peerKey',
            'lifecycle_state': 'lifecycleState'
        }

        self._peer_key = None
        self._lifecycle_state = None

    @property
    def peer_key(self):
        """
        Gets the peer_key of this PeerSummary.
        Peer identifier


        :return: The peer_key of this PeerSummary.
        :rtype: str
        """
        return self._peer_key

    @peer_key.setter
    def peer_key(self, peer_key):
        """
        Sets the peer_key of this PeerSummary.
        Peer identifier


        :param peer_key: The peer_key of this PeerSummary.
        :type: str
        """
        self._peer_key = peer_key

    @property
    def lifecycle_state(self):
        """
        Gets the lifecycle_state of this PeerSummary.
        The current state of the peer.


        :return: The lifecycle_state of this PeerSummary.
        :rtype: str
        """
        return self._lifecycle_state

    @lifecycle_state.setter
    def lifecycle_state(self, lifecycle_state):
        """
        Sets the lifecycle_state of this PeerSummary.
        The current state of the peer.


        :param lifecycle_state: The lifecycle_state of this PeerSummary.
        :type: str
        """
        self._lifecycle_state = lifecycle_state

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
