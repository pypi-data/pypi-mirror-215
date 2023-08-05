# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DownloadOperationsInsightsWarehouseWalletDetails(object):
    """
    Download Wallet details.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DownloadOperationsInsightsWarehouseWalletDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param operations_insights_warehouse_wallet_password:
            The value to assign to the operations_insights_warehouse_wallet_password property of this DownloadOperationsInsightsWarehouseWalletDetails.
        :type operations_insights_warehouse_wallet_password: str

        """
        self.swagger_types = {
            'operations_insights_warehouse_wallet_password': 'str'
        }

        self.attribute_map = {
            'operations_insights_warehouse_wallet_password': 'operationsInsightsWarehouseWalletPassword'
        }

        self._operations_insights_warehouse_wallet_password = None

    @property
    def operations_insights_warehouse_wallet_password(self):
        """
        **[Required]** Gets the operations_insights_warehouse_wallet_password of this DownloadOperationsInsightsWarehouseWalletDetails.
        User provided ADW wallet password for the Operations Insights Warehouse.


        :return: The operations_insights_warehouse_wallet_password of this DownloadOperationsInsightsWarehouseWalletDetails.
        :rtype: str
        """
        return self._operations_insights_warehouse_wallet_password

    @operations_insights_warehouse_wallet_password.setter
    def operations_insights_warehouse_wallet_password(self, operations_insights_warehouse_wallet_password):
        """
        Sets the operations_insights_warehouse_wallet_password of this DownloadOperationsInsightsWarehouseWalletDetails.
        User provided ADW wallet password for the Operations Insights Warehouse.


        :param operations_insights_warehouse_wallet_password: The operations_insights_warehouse_wallet_password of this DownloadOperationsInsightsWarehouseWalletDetails.
        :type: str
        """
        self._operations_insights_warehouse_wallet_password = operations_insights_warehouse_wallet_password

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
