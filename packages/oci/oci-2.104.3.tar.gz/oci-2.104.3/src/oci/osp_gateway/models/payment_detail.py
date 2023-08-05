# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PaymentDetail(object):
    """
    Payment related details
    """

    #: A constant which can be used with the payment_method property of a PaymentDetail.
    #: This constant has a value of "CREDIT_CARD"
    PAYMENT_METHOD_CREDIT_CARD = "CREDIT_CARD"

    #: A constant which can be used with the payment_method property of a PaymentDetail.
    #: This constant has a value of "PAYPAL"
    PAYMENT_METHOD_PAYPAL = "PAYPAL"

    #: A constant which can be used with the payment_method property of a PaymentDetail.
    #: This constant has a value of "OTHER"
    PAYMENT_METHOD_OTHER = "OTHER"

    def __init__(self, **kwargs):
        """
        Initializes a new PaymentDetail object with values from keyword arguments. This class has the following subclasses and if you are using this class as input
        to a service operations then you should favor using a subclass over the base class:

        * :class:`~oci.osp_gateway.models.OtherPaymentDetail`
        * :class:`~oci.osp_gateway.models.PaypalPaymentDetail`
        * :class:`~oci.osp_gateway.models.CreditCardPaymentDetail`

        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param time_paid_on:
            The value to assign to the time_paid_on property of this PaymentDetail.
        :type time_paid_on: datetime

        :param paid_by:
            The value to assign to the paid_by property of this PaymentDetail.
        :type paid_by: str

        :param payment_method:
            The value to assign to the payment_method property of this PaymentDetail.
            Allowed values for this property are: "CREDIT_CARD", "PAYPAL", "OTHER", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type payment_method: str

        :param amount_paid:
            The value to assign to the amount_paid property of this PaymentDetail.
        :type amount_paid: float

        """
        self.swagger_types = {
            'time_paid_on': 'datetime',
            'paid_by': 'str',
            'payment_method': 'str',
            'amount_paid': 'float'
        }

        self.attribute_map = {
            'time_paid_on': 'timePaidOn',
            'paid_by': 'paidBy',
            'payment_method': 'paymentMethod',
            'amount_paid': 'amountPaid'
        }

        self._time_paid_on = None
        self._paid_by = None
        self._payment_method = None
        self._amount_paid = None

    @staticmethod
    def get_subtype(object_dictionary):
        """
        Given the hash representation of a subtype of this class,
        use the info in the hash to return the class of the subtype.
        """
        type = object_dictionary['paymentMethod']

        if type == 'OTHER':
            return 'OtherPaymentDetail'

        if type == 'PAYPAL':
            return 'PaypalPaymentDetail'

        if type == 'CREDIT_CARD':
            return 'CreditCardPaymentDetail'
        else:
            return 'PaymentDetail'

    @property
    def time_paid_on(self):
        """
        Gets the time_paid_on of this PaymentDetail.
        Paid the invoice on this day


        :return: The time_paid_on of this PaymentDetail.
        :rtype: datetime
        """
        return self._time_paid_on

    @time_paid_on.setter
    def time_paid_on(self, time_paid_on):
        """
        Sets the time_paid_on of this PaymentDetail.
        Paid the invoice on this day


        :param time_paid_on: The time_paid_on of this PaymentDetail.
        :type: datetime
        """
        self._time_paid_on = time_paid_on

    @property
    def paid_by(self):
        """
        Gets the paid_by of this PaymentDetail.
        example


        :return: The paid_by of this PaymentDetail.
        :rtype: str
        """
        return self._paid_by

    @paid_by.setter
    def paid_by(self, paid_by):
        """
        Sets the paid_by of this PaymentDetail.
        example


        :param paid_by: The paid_by of this PaymentDetail.
        :type: str
        """
        self._paid_by = paid_by

    @property
    def payment_method(self):
        """
        **[Required]** Gets the payment_method of this PaymentDetail.
        Payment method

        Allowed values for this property are: "CREDIT_CARD", "PAYPAL", "OTHER", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The payment_method of this PaymentDetail.
        :rtype: str
        """
        return self._payment_method

    @payment_method.setter
    def payment_method(self, payment_method):
        """
        Sets the payment_method of this PaymentDetail.
        Payment method


        :param payment_method: The payment_method of this PaymentDetail.
        :type: str
        """
        allowed_values = ["CREDIT_CARD", "PAYPAL", "OTHER"]
        if not value_allowed_none_or_none_sentinel(payment_method, allowed_values):
            payment_method = 'UNKNOWN_ENUM_VALUE'
        self._payment_method = payment_method

    @property
    def amount_paid(self):
        """
        Gets the amount_paid of this PaymentDetail.
        Amount that paid


        :return: The amount_paid of this PaymentDetail.
        :rtype: float
        """
        return self._amount_paid

    @amount_paid.setter
    def amount_paid(self, amount_paid):
        """
        Sets the amount_paid of this PaymentDetail.
        Amount that paid


        :param amount_paid: The amount_paid of this PaymentDetail.
        :type: float
        """
        self._amount_paid = amount_paid

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
