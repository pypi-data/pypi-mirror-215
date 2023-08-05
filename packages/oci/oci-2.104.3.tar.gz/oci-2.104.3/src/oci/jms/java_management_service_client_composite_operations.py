# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

import oci  # noqa: F401
from oci.util import WAIT_RESOURCE_NOT_FOUND  # noqa: F401


class JavaManagementServiceClientCompositeOperations(object):
    """
    This class provides a wrapper around :py:class:`~oci.jms.JavaManagementServiceClient` and offers convenience methods
    for operations that would otherwise need to be chained together. For example, instead of performing an action
    on a resource (e.g. launching an instance, creating a load balancer) and then using a waiter to wait for the resource
    to enter a given state, you can call a single method in this class to accomplish the same functionality
    """

    def __init__(self, client, **kwargs):
        """
        Creates a new JavaManagementServiceClientCompositeOperations object

        :param JavaManagementServiceClient client:
            The service client which will be wrapped by this object
        """
        self.client = client

    def add_fleet_installation_sites_and_wait_for_state(self, fleet_id, add_fleet_installation_sites_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.add_fleet_installation_sites` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.AddFleetInstallationSitesDetails add_fleet_installation_sites_details: (required)
            List of installation sites to be added.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.add_fleet_installation_sites`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.add_fleet_installation_sites(fleet_id, add_fleet_installation_sites_details, **operation_kwargs)
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

    def change_fleet_compartment_and_wait_for_state(self, fleet_id, change_fleet_compartment_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.change_fleet_compartment` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.ChangeFleetCompartmentDetails change_fleet_compartment_details: (required)
            Compartment identifier.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.change_fleet_compartment`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.change_fleet_compartment(fleet_id, change_fleet_compartment_details, **operation_kwargs)
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

    def create_fleet_and_wait_for_state(self, create_fleet_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.create_fleet` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param oci.jms.models.CreateFleetDetails create_fleet_details: (required)
            Details for the new Fleet.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.create_fleet`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.create_fleet(create_fleet_details, **operation_kwargs)
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

    def delete_crypto_analysis_result_and_wait_for_state(self, fleet_id, crypto_analysis_result_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.delete_crypto_analysis_result` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param str crypto_analysis_result_id: (required)
            The OCID of the analysis result.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.delete_crypto_analysis_result`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_crypto_analysis_result(fleet_id, crypto_analysis_result_id, **operation_kwargs)
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

    def delete_fleet_and_wait_for_state(self, fleet_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.delete_fleet` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.delete_fleet`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_fleet(fleet_id, **operation_kwargs)
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

    def delete_java_migration_analysis_result_and_wait_for_state(self, fleet_id, java_migration_analysis_result_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.delete_java_migration_analysis_result` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param str java_migration_analysis_result_id: (required)
            The OCID of the analysis result.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.delete_java_migration_analysis_result`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_java_migration_analysis_result(fleet_id, java_migration_analysis_result_id, **operation_kwargs)
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

    def delete_performance_tuning_analysis_result_and_wait_for_state(self, fleet_id, performance_tuning_analysis_result_id, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.delete_performance_tuning_analysis_result` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param str performance_tuning_analysis_result_id: (required)
            The OCID of the performance tuning analysis result.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.delete_performance_tuning_analysis_result`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = None
        try:
            operation_result = self.client.delete_performance_tuning_analysis_result(fleet_id, performance_tuning_analysis_result_id, **operation_kwargs)
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

    def remove_fleet_installation_sites_and_wait_for_state(self, fleet_id, remove_fleet_installation_sites_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.remove_fleet_installation_sites` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.RemoveFleetInstallationSitesDetails remove_fleet_installation_sites_details: (required)
            List of installation sites to be deleted.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.remove_fleet_installation_sites`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.remove_fleet_installation_sites(fleet_id, remove_fleet_installation_sites_details, **operation_kwargs)
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

    def request_crypto_analyses_and_wait_for_state(self, fleet_id, request_crypto_analyses_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.request_crypto_analyses` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.RequestCryptoAnalysesDetails request_crypto_analyses_details: (required)
            Detail information to start Crypto Analyses

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.request_crypto_analyses`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.request_crypto_analyses(fleet_id, request_crypto_analyses_details, **operation_kwargs)
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

    def request_java_migration_analyses_and_wait_for_state(self, fleet_id, request_java_migration_analyses_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.request_java_migration_analyses` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.RequestJavaMigrationAnalysesDetails request_java_migration_analyses_details: (required)
            Detail information that starts the Java migration analysis

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.request_java_migration_analyses`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.request_java_migration_analyses(fleet_id, request_java_migration_analyses_details, **operation_kwargs)
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

    def request_jfr_recordings_and_wait_for_state(self, fleet_id, request_jfr_recordings_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.request_jfr_recordings` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.RequestJfrRecordingsDetails request_jfr_recordings_details: (required)
            Detail information to start JFR recordings.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.request_jfr_recordings`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.request_jfr_recordings(fleet_id, request_jfr_recordings_details, **operation_kwargs)
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

    def request_performance_tuning_analyses_and_wait_for_state(self, fleet_id, request_performance_tuning_analyses_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.request_performance_tuning_analyses` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.RequestPerformanceTuningAnalysesDetails request_performance_tuning_analyses_details: (required)
            Detail information to start Performance Tuning Analyses

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.request_performance_tuning_analyses`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.request_performance_tuning_analyses(fleet_id, request_performance_tuning_analyses_details, **operation_kwargs)
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

    def scan_java_server_usage_and_wait_for_state(self, fleet_id, scan_java_server_usage_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.scan_java_server_usage` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.ScanJavaServerUsageDetails scan_java_server_usage_details: (required)
            List of managed instances to be scanned.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.scan_java_server_usage`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.scan_java_server_usage(fleet_id, scan_java_server_usage_details, **operation_kwargs)
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

    def scan_library_usage_and_wait_for_state(self, fleet_id, scan_library_usage_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.scan_library_usage` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.ScanLibraryUsageDetails scan_library_usage_details: (required)
            List of managed instances to be scanned.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.scan_library_usage`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.scan_library_usage(fleet_id, scan_library_usage_details, **operation_kwargs)
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

    def update_fleet_and_wait_for_state(self, fleet_id, update_fleet_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.update_fleet` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.UpdateFleetDetails update_fleet_details: (required)
            The new details for the Fleet.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.update_fleet`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_fleet(fleet_id, update_fleet_details, **operation_kwargs)
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

    def update_fleet_agent_configuration_and_wait_for_state(self, fleet_id, update_fleet_agent_configuration_details, wait_for_states=[], operation_kwargs={}, waiter_kwargs={}):
        """
        Calls :py:func:`~oci.jms.JavaManagementServiceClient.update_fleet_agent_configuration` and waits for the :py:class:`~oci.jms.models.WorkRequest`
        to enter the given state(s).

        :param str fleet_id: (required)
            The `OCID`__ of the Fleet.

            __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm

        :param oci.jms.models.UpdateFleetAgentConfigurationDetails update_fleet_agent_configuration_details: (required)
            The new details for the Fleet Agent Configuration.

        :param list[str] wait_for_states:
            An array of states to wait on. These should be valid values for :py:attr:`~oci.jms.models.WorkRequest.status`

        :param dict operation_kwargs:
            A dictionary of keyword arguments to pass to :py:func:`~oci.jms.JavaManagementServiceClient.update_fleet_agent_configuration`

        :param dict waiter_kwargs:
            A dictionary of keyword arguments to pass to the :py:func:`oci.wait_until` function. For example, you could pass ``max_interval_seconds`` or ``max_interval_seconds``
            as dictionary keys to modify how long the waiter function will wait between retries and the maximum amount of time it will wait
        """
        operation_result = self.client.update_fleet_agent_configuration(fleet_id, update_fleet_agent_configuration_details, **operation_kwargs)
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
