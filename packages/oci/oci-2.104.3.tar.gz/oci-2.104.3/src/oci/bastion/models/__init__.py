# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import absolute_import

from .bastion import Bastion
from .bastion_summary import BastionSummary
from .change_bastion_compartment_details import ChangeBastionCompartmentDetails
from .create_bastion_details import CreateBastionDetails
from .create_dynamic_port_forwarding_session_target_resource_details import CreateDynamicPortForwardingSessionTargetResourceDetails
from .create_managed_ssh_session_target_resource_details import CreateManagedSshSessionTargetResourceDetails
from .create_port_forwarding_session_target_resource_details import CreatePortForwardingSessionTargetResourceDetails
from .create_session_details import CreateSessionDetails
from .create_session_target_resource_details import CreateSessionTargetResourceDetails
from .dynamic_port_forwarding_session_target_resource_details import DynamicPortForwardingSessionTargetResourceDetails
from .managed_ssh_session_target_resource_details import ManagedSshSessionTargetResourceDetails
from .port_forwarding_session_target_resource_details import PortForwardingSessionTargetResourceDetails
from .public_key_details import PublicKeyDetails
from .session import Session
from .session_summary import SessionSummary
from .target_resource_details import TargetResourceDetails
from .update_bastion_details import UpdateBastionDetails
from .update_session_details import UpdateSessionDetails
from .work_request import WorkRequest
from .work_request_error import WorkRequestError
from .work_request_log_entry import WorkRequestLogEntry
from .work_request_resource import WorkRequestResource
from .work_request_summary import WorkRequestSummary

# Maps type names to classes for bastion services.
bastion_type_mapping = {
    "Bastion": Bastion,
    "BastionSummary": BastionSummary,
    "ChangeBastionCompartmentDetails": ChangeBastionCompartmentDetails,
    "CreateBastionDetails": CreateBastionDetails,
    "CreateDynamicPortForwardingSessionTargetResourceDetails": CreateDynamicPortForwardingSessionTargetResourceDetails,
    "CreateManagedSshSessionTargetResourceDetails": CreateManagedSshSessionTargetResourceDetails,
    "CreatePortForwardingSessionTargetResourceDetails": CreatePortForwardingSessionTargetResourceDetails,
    "CreateSessionDetails": CreateSessionDetails,
    "CreateSessionTargetResourceDetails": CreateSessionTargetResourceDetails,
    "DynamicPortForwardingSessionTargetResourceDetails": DynamicPortForwardingSessionTargetResourceDetails,
    "ManagedSshSessionTargetResourceDetails": ManagedSshSessionTargetResourceDetails,
    "PortForwardingSessionTargetResourceDetails": PortForwardingSessionTargetResourceDetails,
    "PublicKeyDetails": PublicKeyDetails,
    "Session": Session,
    "SessionSummary": SessionSummary,
    "TargetResourceDetails": TargetResourceDetails,
    "UpdateBastionDetails": UpdateBastionDetails,
    "UpdateSessionDetails": UpdateSessionDetails,
    "WorkRequest": WorkRequest,
    "WorkRequestError": WorkRequestError,
    "WorkRequestLogEntry": WorkRequestLogEntry,
    "WorkRequestResource": WorkRequestResource,
    "WorkRequestSummary": WorkRequestSummary
}
