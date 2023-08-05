# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import absolute_import

from .application_collection import ApplicationCollection
from .application_summary import ApplicationSummary
from .bulk_replace_service_catalog_associations_details import BulkReplaceServiceCatalogAssociationsDetails
from .change_private_application_compartment_details import ChangePrivateApplicationCompartmentDetails
from .change_service_catalog_compartment_details import ChangeServiceCatalogCompartmentDetails
from .create_private_application_details import CreatePrivateApplicationDetails
from .create_private_application_package import CreatePrivateApplicationPackage
from .create_private_application_stack_package import CreatePrivateApplicationStackPackage
from .create_service_catalog_association_details import CreateServiceCatalogAssociationDetails
from .create_service_catalog_details import CreateServiceCatalogDetails
from .error_entity import ErrorEntity
from .private_application import PrivateApplication
from .private_application_collection import PrivateApplicationCollection
from .private_application_package import PrivateApplicationPackage
from .private_application_package_collection import PrivateApplicationPackageCollection
from .private_application_package_summary import PrivateApplicationPackageSummary
from .private_application_stack_package import PrivateApplicationStackPackage
from .private_application_summary import PrivateApplicationSummary
from .publisher_summary import PublisherSummary
from .service_catalog import ServiceCatalog
from .service_catalog_association import ServiceCatalogAssociation
from .service_catalog_association_collection import ServiceCatalogAssociationCollection
from .service_catalog_association_summary import ServiceCatalogAssociationSummary
from .service_catalog_collection import ServiceCatalogCollection
from .service_catalog_summary import ServiceCatalogSummary
from .update_private_application_details import UpdatePrivateApplicationDetails
from .update_service_catalog_details import UpdateServiceCatalogDetails
from .upload_data import UploadData
from .work_request import WorkRequest
from .work_request_error import WorkRequestError
from .work_request_error_collection import WorkRequestErrorCollection
from .work_request_log_entry import WorkRequestLogEntry
from .work_request_log_entry_collection import WorkRequestLogEntryCollection
from .work_request_resource import WorkRequestResource
from .work_request_summary import WorkRequestSummary
from .work_request_summary_collection import WorkRequestSummaryCollection

# Maps type names to classes for service_catalog services.
service_catalog_type_mapping = {
    "ApplicationCollection": ApplicationCollection,
    "ApplicationSummary": ApplicationSummary,
    "BulkReplaceServiceCatalogAssociationsDetails": BulkReplaceServiceCatalogAssociationsDetails,
    "ChangePrivateApplicationCompartmentDetails": ChangePrivateApplicationCompartmentDetails,
    "ChangeServiceCatalogCompartmentDetails": ChangeServiceCatalogCompartmentDetails,
    "CreatePrivateApplicationDetails": CreatePrivateApplicationDetails,
    "CreatePrivateApplicationPackage": CreatePrivateApplicationPackage,
    "CreatePrivateApplicationStackPackage": CreatePrivateApplicationStackPackage,
    "CreateServiceCatalogAssociationDetails": CreateServiceCatalogAssociationDetails,
    "CreateServiceCatalogDetails": CreateServiceCatalogDetails,
    "ErrorEntity": ErrorEntity,
    "PrivateApplication": PrivateApplication,
    "PrivateApplicationCollection": PrivateApplicationCollection,
    "PrivateApplicationPackage": PrivateApplicationPackage,
    "PrivateApplicationPackageCollection": PrivateApplicationPackageCollection,
    "PrivateApplicationPackageSummary": PrivateApplicationPackageSummary,
    "PrivateApplicationStackPackage": PrivateApplicationStackPackage,
    "PrivateApplicationSummary": PrivateApplicationSummary,
    "PublisherSummary": PublisherSummary,
    "ServiceCatalog": ServiceCatalog,
    "ServiceCatalogAssociation": ServiceCatalogAssociation,
    "ServiceCatalogAssociationCollection": ServiceCatalogAssociationCollection,
    "ServiceCatalogAssociationSummary": ServiceCatalogAssociationSummary,
    "ServiceCatalogCollection": ServiceCatalogCollection,
    "ServiceCatalogSummary": ServiceCatalogSummary,
    "UpdatePrivateApplicationDetails": UpdatePrivateApplicationDetails,
    "UpdateServiceCatalogDetails": UpdateServiceCatalogDetails,
    "UploadData": UploadData,
    "WorkRequest": WorkRequest,
    "WorkRequestError": WorkRequestError,
    "WorkRequestErrorCollection": WorkRequestErrorCollection,
    "WorkRequestLogEntry": WorkRequestLogEntry,
    "WorkRequestLogEntryCollection": WorkRequestLogEntryCollection,
    "WorkRequestResource": WorkRequestResource,
    "WorkRequestSummary": WorkRequestSummary,
    "WorkRequestSummaryCollection": WorkRequestSummaryCollection
}
