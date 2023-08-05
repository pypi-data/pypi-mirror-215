# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import oci  # noqa: F401
from oci.util import WAIT_RESOURCE_NOT_FOUND  # noqa: F401


class DbManagementClientCompositeOperations(object):
    """
    This class provides a wrapper around :py:class:`~oci.database_management.DbManagementClient` and offers convenience methods
    for operations that would otherwise need to be chained together. For example, instead of performing an action
    on a resource (e.g. launching an instance, creating a load balancer) and then using a waiter to wait for the resource
    to enter a given state, you can call a single method in this class to accomplish the same functionality
    """

    def __init__(self, client, **kwargs):
        """
        Creates a new DbManagementClientCompositeOperations object

        :param DbManagementClient client:
            The service client which will be wrapped by this object
        """
        self.client = client

    def change_external_db_system_compartment_and_wait_for_state(self, external_db_system_id, change_external_db_system_compartment_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.change_external_db_system_compartment` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_system_id: (required)
            The `OCID`__ of the external DB system.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.ChangeExternalDbSystemCompartmentDetails change_external_db_system_compartment_details: (required)
            The `OCID`__ of the compartment to which the external DB system should be moved.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.change_external_db_system_compartment`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.change_external_db_system_compartment(external_db_system_id, change_external_db_system_compartment_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def change_external_exadata_infrastructure_compartment_and_wait_for_state(self, external_exadata_infrastructure_id, change_external_exadata_infrastructure_compartment_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.change_external_exadata_infrastructure_compartment` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_exadata_infrastructure_id: (required)
            The `OCID`__ of the Exadata infrastructure.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.ChangeExternalExadataInfrastructureCompartmentDetails change_external_exadata_infrastructure_compartment_details: (required)
            The details required to change the compartment for the Exadata infrastructure.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.change_external_exadata_infrastructure_compartment`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.change_external_exadata_infrastructure_compartment(external_exadata_infrastructure_id, change_external_exadata_infrastructure_compartment_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def check_external_db_system_connector_connection_status_and_wait_for_state(self, external_db_system_connector_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.check_external_db_system_connector_connection_status` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystemConnector` acted upon
        to enter the given state(s).

        :param str external_db_system_connector_id: (required)
            The `OCID`__ of the external connector.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystemConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.check_external_db_system_connector_connection_status`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.check_external_db_system_connector_connection_status(external_db_system_connector_id, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_db_system_connector_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_db_system_connector(external_db_system_connector_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_db_management_private_endpoint_and_wait_for_state(self, create_db_management_private_endpoint_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_db_management_private_endpoint` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param oci.database_management.models.CreateDbManagementPrivateEndpointDetails create_db_management_private_endpoint_details: (required)
            Details used to create a new Database Management private endpoint.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_db_management_private_endpoint`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_db_management_private_endpoint(create_db_management_private_endpoint_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_external_db_system_and_wait_for_state(self, create_external_db_system_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_external_db_system` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param oci.database_management.models.CreateExternalDbSystemDetails create_external_db_system_details: (required)
            The details required to create an external DB system.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_external_db_system`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_external_db_system(create_external_db_system_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_external_db_system_connector_and_wait_for_state(self, create_external_db_system_connector_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_external_db_system_connector` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystemConnector` acted upon
        to enter the given state(s).

        :param oci.database_management.models.CreateExternalDbSystemConnectorDetails create_external_db_system_connector_details: (required)
            The details required to create an external connector.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystemConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_external_db_system_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_external_db_system_connector(create_external_db_system_connector_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_db_system_connector_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_db_system_connector(external_db_system_connector_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_external_db_system_discovery_and_wait_for_state(self, create_external_db_system_discovery_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_external_db_system_discovery` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param oci.database_management.models.CreateExternalDbSystemDiscoveryDetails create_external_db_system_discovery_details: (required)
            The details required to create an external DB system discovery.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_external_db_system_discovery`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_external_db_system_discovery(create_external_db_system_discovery_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_external_exadata_infrastructure_and_wait_for_state(self, create_external_exadata_infrastructure_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_external_exadata_infrastructure` and waits for the :py:class:`~oci.database_management.models.ExternalExadataInfrastructure` acted upon
        to enter the given state(s).

        :param oci.database_management.models.CreateExternalExadataInfrastructureDetails create_external_exadata_infrastructure_details: (required)
            The details required to create the managed Exadata infrastructure resources.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalExadataInfrastructure.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_external_exadata_infrastructure`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_external_exadata_infrastructure(create_external_exadata_infrastructure_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_exadata_infrastructure_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_exadata_infrastructure(external_exadata_infrastructure_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_external_exadata_storage_connector_and_wait_for_state(self, create_external_exadata_storage_connector_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_external_exadata_storage_connector` and waits for the :py:class:`~oci.database_management.models.ExternalExadataStorageConnector` acted upon
        to enter the given state(s).

        :param oci.database_management.models.CreateExternalExadataStorageConnectorDetails create_external_exadata_storage_connector_details: (required)
            The details required to add connections to the storage servers.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalExadataStorageConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_external_exadata_storage_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_external_exadata_storage_connector(create_external_exadata_storage_connector_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_exadata_storage_connector_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_exadata_storage_connector(external_exadata_storage_connector_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_job_and_wait_for_state(self, create_job_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_job` and waits for the :py:class:`~oci.database_management.models.Job` acted upon
        to enter the given state(s).

        :param oci.database_management.models.CreateJobDetails create_job_details: (required)
            The details required to create a job.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.Job.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_job`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_job(create_job_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        job_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_job(job_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def create_managed_database_group_and_wait_for_state(self, create_managed_database_group_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.create_managed_database_group` and waits for the :py:class:`~oci.database_management.models.ManagedDatabaseGroup` acted upon
        to enter the given state(s).

        :param oci.database_management.models.CreateManagedDatabaseGroupDetails create_managed_database_group_details: (required)
            The details required to create a Managed Database Group.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ManagedDatabaseGroup.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.create_managed_database_group`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_managed_database_group(create_managed_database_group_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        managed_database_group_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_managed_database_group(managed_database_group_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_db_management_private_endpoint_and_wait_for_state(self, db_management_private_endpoint_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_db_management_private_endpoint` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str db_management_private_endpoint_id: (required)
            The `OCID`__ of the Database Management private endpoint.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_db_management_private_endpoint`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_db_management_private_endpoint(db_management_private_endpoint_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_external_db_system_and_wait_for_state(self, external_db_system_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_system_id: (required)
            The `OCID`__ of the external DB system.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_external_db_system(external_db_system_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_external_db_system_connector_and_wait_for_state(self, external_db_system_connector_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system_connector` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystemConnector` acted upon
        to enter the given state(s).

        :param str external_db_system_connector_id: (required)
            The `OCID`__ of the external connector.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystemConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        initial_get_result = self.client.get_external_db_system_connector(external_db_system_connector_id)
        operation_result = None
        try:
            operation_result = self.client.delete_external_db_system_connector(external_db_system_connector_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]

        try:
            if ("succeed_on_not_found" in waiter_kwargs) and (waiter_kwargs["succeed_on_not_found"] is False):
                self.client.base_client.logger.warning("The waiter kwarg succeed_on_not_found was passed as False for the delete composite operation delete_external_db_system_connector, this would result in the operation to fail if the resource is not found! Please, do not pass this kwarg if this was not intended")
            else:
                """
                If the user does not send in this value, we set it to True by default.
                We are doing this because during a delete resource scenario and waiting on its state, the service can
                return a 404 NOT FOUND exception as the resource was deleted and a get on its state would fail
                """
                waiter_kwargs["succeed_on_not_found"] = True
            waiter_result = oci.wait_until(
                self.client,
                initial_get_result,  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_external_db_system_discovery_and_wait_for_state(self, external_db_system_discovery_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system_discovery` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystemDiscovery` acted upon
        to enter the given state(s).

        :param str external_db_system_discovery_id: (required)
            The `OCID`__ of the external DB system discovery.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystemDiscovery.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_external_db_system_discovery`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        initial_get_result = self.client.get_external_db_system_discovery(external_db_system_discovery_id)
        operation_result = None
        try:
            operation_result = self.client.delete_external_db_system_discovery(external_db_system_discovery_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]

        try:
            if ("succeed_on_not_found" in waiter_kwargs) and (waiter_kwargs["succeed_on_not_found"] is False):
                self.client.base_client.logger.warning("The waiter kwarg succeed_on_not_found was passed as False for the delete composite operation delete_external_db_system_discovery, this would result in the operation to fail if the resource is not found! Please, do not pass this kwarg if this was not intended")
            else:
                """
                If the user does not send in this value, we set it to True by default.
                We are doing this because during a delete resource scenario and waiting on its state, the service can
                return a 404 NOT FOUND exception as the resource was deleted and a get on its state would fail
                """
                waiter_kwargs["succeed_on_not_found"] = True
            waiter_result = oci.wait_until(
                self.client,
                initial_get_result,  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_external_exadata_infrastructure_and_wait_for_state(self, external_exadata_infrastructure_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_external_exadata_infrastructure` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_exadata_infrastructure_id: (required)
            The `OCID`__ of the Exadata infrastructure.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_external_exadata_infrastructure`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_external_exadata_infrastructure(external_exadata_infrastructure_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_external_exadata_storage_connector_and_wait_for_state(self, external_exadata_storage_connector_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_external_exadata_storage_connector` and waits for the :py:class:`~oci.database_management.models.ExternalExadataStorageConnector` acted upon
        to enter the given state(s).

        :param str external_exadata_storage_connector_id: (required)
            The `OCID`__ of the connector to the Exadata storage server.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalExadataStorageConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_external_exadata_storage_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        initial_get_result = self.client.get_external_exadata_storage_connector(external_exadata_storage_connector_id)
        operation_result = None
        try:
            operation_result = self.client.delete_external_exadata_storage_connector(external_exadata_storage_connector_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]

        try:
            if ("succeed_on_not_found" in waiter_kwargs) and (waiter_kwargs["succeed_on_not_found"] is False):
                self.client.base_client.logger.warning("The waiter kwarg succeed_on_not_found was passed as False for the delete composite operation delete_external_exadata_storage_connector, this would result in the operation to fail if the resource is not found! Please, do not pass this kwarg if this was not intended")
            else:
                """
                If the user does not send in this value, we set it to True by default.
                We are doing this because during a delete resource scenario and waiting on its state, the service can
                return a 404 NOT FOUND exception as the resource was deleted and a get on its state would fail
                """
                waiter_kwargs["succeed_on_not_found"] = True
            waiter_result = oci.wait_until(
                self.client,
                initial_get_result,  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_job_and_wait_for_state(self, job_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_job` and waits for the :py:class:`~oci.database_management.models.Job` acted upon
        to enter the given state(s).

        :param str job_id: (required)
            The identifier of the job.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.Job.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_job`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        initial_get_result = self.client.get_job(job_id)
        operation_result = None
        try:
            operation_result = self.client.delete_job(job_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]

        try:
            if ("succeed_on_not_found" in waiter_kwargs) and (waiter_kwargs["succeed_on_not_found"] is False):
                self.client.base_client.logger.warning("The waiter kwarg succeed_on_not_found was passed as False for the delete composite operation delete_job, this would result in the operation to fail if the resource is not found! Please, do not pass this kwarg if this was not intended")
            else:
                """
                If the user does not send in this value, we set it to True by default.
                We are doing this because during a delete resource scenario and waiting on its state, the service can
                return a 404 NOT FOUND exception as the resource was deleted and a get on its state would fail
                """
                waiter_kwargs["succeed_on_not_found"] = True
            waiter_result = oci.wait_until(
                self.client,
                initial_get_result,  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def delete_managed_database_group_and_wait_for_state(self, managed_database_group_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.delete_managed_database_group` and waits for the :py:class:`~oci.database_management.models.ManagedDatabaseGroup` acted upon
        to enter the given state(s).

        :param str managed_database_group_id: (required)
            The `OCID`__ of the Managed Database Group.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ManagedDatabaseGroup.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.delete_managed_database_group`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        initial_get_result = self.client.get_managed_database_group(managed_database_group_id)
        operation_result = None
        try:
            operation_result = self.client.delete_managed_database_group(managed_database_group_id, **operation_kwargs)
        except oci.exceptions.ServiceError as e:
            if e.status == 404:
                return WAIT_RESOURCE_NOT_FOUND
            else:
                raise e

        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]

        try:
            if ("succeed_on_not_found" in waiter_kwargs) and (waiter_kwargs["succeed_on_not_found"] is False):
                self.client.base_client.logger.warning("The waiter kwarg succeed_on_not_found was passed as False for the delete composite operation delete_managed_database_group, this would result in the operation to fail if the resource is not found! Please, do not pass this kwarg if this was not intended")
            else:
                """
                If the user does not send in this value, we set it to True by default.
                We are doing this because during a delete resource scenario and waiting on its state, the service can
                return a 404 NOT FOUND exception as the resource was deleted and a get on its state would fail
                """
                waiter_kwargs["succeed_on_not_found"] = True
            waiter_result = oci.wait_until(
                self.client,
                initial_get_result,  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def disable_external_db_system_database_management_and_wait_for_state(self, external_db_system_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.disable_external_db_system_database_management` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_system_id: (required)
            The `OCID`__ of the external DB system.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.disable_external_db_system_database_management`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.disable_external_db_system_database_management(external_db_system_id, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def disable_external_exadata_infrastructure_management_and_wait_for_state(self, external_exadata_infrastructure_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.disable_external_exadata_infrastructure_management` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_exadata_infrastructure_id: (required)
            The `OCID`__ of the Exadata infrastructure.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.disable_external_exadata_infrastructure_management`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.disable_external_exadata_infrastructure_management(external_exadata_infrastructure_id, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def enable_external_db_system_database_management_and_wait_for_state(self, external_db_system_id, enable_external_db_system_database_management_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.enable_external_db_system_database_management` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_system_id: (required)
            The `OCID`__ of the external DB system.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.EnableExternalDbSystemDatabaseManagementDetails enable_external_db_system_database_management_details: (required)
            The details required to enable Database Management for an external DB system.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.enable_external_db_system_database_management`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.enable_external_db_system_database_management(external_db_system_id, enable_external_db_system_database_management_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def enable_external_exadata_infrastructure_management_and_wait_for_state(self, external_exadata_infrastructure_id, enable_external_exadata_infrastructure_management_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.enable_external_exadata_infrastructure_management` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_exadata_infrastructure_id: (required)
            The `OCID`__ of the Exadata infrastructure.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.EnableExternalExadataInfrastructureManagementDetails enable_external_exadata_infrastructure_management_details: (required)
            The details required to enable the management for the Exadata infrastructure.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.enable_external_exadata_infrastructure_management`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.enable_external_exadata_infrastructure_management(external_exadata_infrastructure_id, enable_external_exadata_infrastructure_management_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_db_management_private_endpoint_and_wait_for_state(self, db_management_private_endpoint_id, update_db_management_private_endpoint_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_db_management_private_endpoint` and waits for the :py:class:`~oci.database_management.models.DbManagementPrivateEndpoint` acted upon
        to enter the given state(s).

        :param str db_management_private_endpoint_id: (required)
            The `OCID`__ of the Database Management private endpoint.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateDbManagementPrivateEndpointDetails update_db_management_private_endpoint_details: (required)
            The details used to update a Database Management private endpoint.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.DbManagementPrivateEndpoint.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_db_management_private_endpoint`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_db_management_private_endpoint(db_management_private_endpoint_id, update_db_management_private_endpoint_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        db_management_private_endpoint_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_db_management_private_endpoint(db_management_private_endpoint_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_asm_and_wait_for_state(self, external_asm_id, update_external_asm_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_asm` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_asm_id: (required)
            The `OCID`__ of the external ASM.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalAsmDetails update_external_asm_details: (required)
            The details required to update an external ASM.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_asm`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_asm(external_asm_id, update_external_asm_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_cluster_and_wait_for_state(self, external_cluster_id, update_external_cluster_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_cluster` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_cluster_id: (required)
            The `OCID`__ of the external cluster.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalClusterDetails update_external_cluster_details: (required)
            The details required to update an external cluster.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_cluster`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_cluster(external_cluster_id, update_external_cluster_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_cluster_instance_and_wait_for_state(self, external_cluster_instance_id, update_external_cluster_instance_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_cluster_instance` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_cluster_instance_id: (required)
            The `OCID`__ of the external cluster instance.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalClusterInstanceDetails update_external_cluster_instance_details: (required)
            The details required to update an external cluster instance.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_cluster_instance`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_cluster_instance(external_cluster_instance_id, update_external_cluster_instance_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_db_node_and_wait_for_state(self, external_db_node_id, update_external_db_node_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_db_node` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_node_id: (required)
            The `OCID`__ of the external database node.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalDbNodeDetails update_external_db_node_details: (required)
            The details required to update an external DB node.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_db_node`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_db_node(external_db_node_id, update_external_db_node_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_db_system_and_wait_for_state(self, external_db_system_id, update_external_db_system_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_db_system` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystem` acted upon
        to enter the given state(s).

        :param str external_db_system_id: (required)
            The `OCID`__ of the external DB system.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalDbSystemDetails update_external_db_system_details: (required)
            The details required to update an external DB system.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystem.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_db_system`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_db_system(external_db_system_id, update_external_db_system_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_db_system_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_db_system(external_db_system_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_db_system_connector_and_wait_for_state(self, external_db_system_connector_id, update_external_db_system_connector_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_db_system_connector` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_db_system_connector_id: (required)
            The `OCID`__ of the external connector.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalDbSystemConnectorDetails update_external_db_system_connector_details: (required)
            The details required to update an external connector.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_db_system_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_db_system_connector(external_db_system_connector_id, update_external_db_system_connector_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_db_system_discovery_and_wait_for_state(self, external_db_system_discovery_id, update_external_db_system_discovery_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_db_system_discovery` and waits for the :py:class:`~oci.database_management.models.ExternalDbSystemDiscovery` acted upon
        to enter the given state(s).

        :param str external_db_system_discovery_id: (required)
            The `OCID`__ of the external DB system discovery.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalDbSystemDiscoveryDetails update_external_db_system_discovery_details: (required)
            The details required to update an external DB system discovery.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalDbSystemDiscovery.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_db_system_discovery`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_db_system_discovery(external_db_system_discovery_id, update_external_db_system_discovery_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_db_system_discovery_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_db_system_discovery(external_db_system_discovery_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_exadata_infrastructure_and_wait_for_state(self, external_exadata_infrastructure_id, update_external_exadata_infrastructure_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_exadata_infrastructure` and waits for the :py:class:`~oci.database_management.models.ExternalExadataInfrastructure` acted upon
        to enter the given state(s).

        :param str external_exadata_infrastructure_id: (required)
            The `OCID`__ of the Exadata infrastructure.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalExadataInfrastructureDetails update_external_exadata_infrastructure_details: (required)
            The details required to update the managed Exadata infrastructure resources.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalExadataInfrastructure.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_exadata_infrastructure`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_exadata_infrastructure(external_exadata_infrastructure_id, update_external_exadata_infrastructure_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_exadata_infrastructure_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_exadata_infrastructure(external_exadata_infrastructure_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_exadata_storage_connector_and_wait_for_state(self, external_exadata_storage_connector_id, update_external_exadata_storage_connector_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_exadata_storage_connector` and waits for the :py:class:`~oci.database_management.models.ExternalExadataStorageConnector` acted upon
        to enter the given state(s).

        :param str external_exadata_storage_connector_id: (required)
            The `OCID`__ of the connector to the Exadata storage server.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalExadataStorageConnectorDetails update_external_exadata_storage_connector_details: (required)
            The details required to add connections to the storage servers.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ExternalExadataStorageConnector.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_exadata_storage_connector`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_exadata_storage_connector(external_exadata_storage_connector_id, update_external_exadata_storage_connector_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        external_exadata_storage_connector_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_external_exadata_storage_connector(external_exadata_storage_connector_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_external_listener_and_wait_for_state(self, external_listener_id, update_external_listener_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_external_listener` and waits for the :py:class:`~oci.database_management.models.WorkRequest`
        to enter the given state(s).

        :param str external_listener_id: (required)
            The `OCID`__ of the external listener.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateExternalListenerDetails update_external_listener_details: (required)
            The details required to update an external listener.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_external_listener`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_external_listener(external_listener_id, update_external_listener_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        wait_for_resource_id = operation_result.headers['opc-work-request-id']

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_work_request(wait_for_resource_id),
                evaluate_response=lambda r: getattr(r.data, 'status') and getattr(r.data, 'status').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_job_and_wait_for_state(self, job_id, update_job_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_job` and waits for the :py:class:`~oci.database_management.models.Job` acted upon
        to enter the given state(s).

        :param str job_id: (required)
            The identifier of the job.

        :param oci.database_management.models.UpdateJobDetails update_job_details: (required)
            The details required to update a job.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.Job.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_job`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_job(job_id, update_job_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        job_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_job(job_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)

    def update_managed_database_group_and_wait_for_state(self, managed_database_group_id, update_managed_database_group_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.database_management.DbManagementClient.update_managed_database_group` and waits for the :py:class:`~oci.database_management.models.ManagedDatabaseGroup` acted upon
        to enter the given state(s).

        :param str managed_database_group_id: (required)
            The `OCID`__ of the Managed Database Group.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.database_management.models.UpdateManagedDatabaseGroupDetails update_managed_database_group_details: (required)
            The details required to update a Managed Database Group.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.database_management.models.ManagedDatabaseGroup.lifecycle_state`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.database_management.DbManagementClient.update_managed_database_group`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_managed_database_group(managed_database_group_id, update_managed_database_group_details, **operation_kwargs)
        if not wait_for_states:
            return operation_result

        lowered_wait_for_states = [w.lower() for w in wait_for_states]
        managed_database_group_id = operation_result.data.id

        try:
            waiter_result = oci.wait_until(
                self.client,
                self.client.get_managed_database_group(managed_database_group_id),  # noqa: F821
                evaluate_response=lambda r: getattr(r.data, 'lifecycle_state') and getattr(r.data, 'lifecycle_state').lower() in lowered_wait_for_states,
                **waiter_kwargs
            )
            result_to_return = waiter_result

            return result_to_return
        except (NameError, TypeError) as e:
            if not e.args:
                e.args = ('',)
            e.args = e.args + ('This composite operation is currently not supported in the SDK. Please use the operation from the service client and use waiters as an alternative. For more information on waiters, visit: "https://docs.oracle.com/en-us/iaas/tools/python/latest/api/waiters.html"', )
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
        except Exception as e:
            raise oci.exceptions.CompositeOperationError(partial_results=[operation_result], cause=e)
