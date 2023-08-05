# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class KubernetesVersionsFilters(object):
    """
    The range of kubernetes versions an addon can be configured.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new KubernetesVersionsFilters object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param minimal_version:
            The value to assign to the minimal_version property of this KubernetesVersionsFilters.
        :type minimal_version: str

        :param maximum_version:
            The value to assign to the maximum_version property of this KubernetesVersionsFilters.
        :type maximum_version: str

        :param exact_kubernetes_versions:
            The value to assign to the exact_kubernetes_versions property of this KubernetesVersionsFilters.
        :type exact_kubernetes_versions: list[str]

        """
        self.swagger_types = {
            'minimal_version': 'str',
            'maximum_version': 'str',
            'exact_kubernetes_versions': 'list[str]'
        }

        self.attribute_map = {
            'minimal_version': 'minimalVersion',
            'maximum_version': 'maximumVersion',
            'exact_kubernetes_versions': 'exactKubernetesVersions'
        }

        self._minimal_version = None
        self._maximum_version = None
        self._exact_kubernetes_versions = None

    @property
    def minimal_version(self):
        """
        Gets the minimal_version of this KubernetesVersionsFilters.
        The earliest kubernetes version.


        :return: The minimal_version of this KubernetesVersionsFilters.
        :rtype: str
        """
        return self._minimal_version

    @minimal_version.setter
    def minimal_version(self, minimal_version):
        """
        Sets the minimal_version of this KubernetesVersionsFilters.
        The earliest kubernetes version.


        :param minimal_version: The minimal_version of this KubernetesVersionsFilters.
        :type: str
        """
        self._minimal_version = minimal_version

    @property
    def maximum_version(self):
        """
        Gets the maximum_version of this KubernetesVersionsFilters.
        The latest kubernetes version.


        :return: The maximum_version of this KubernetesVersionsFilters.
        :rtype: str
        """
        return self._maximum_version

    @maximum_version.setter
    def maximum_version(self, maximum_version):
        """
        Sets the maximum_version of this KubernetesVersionsFilters.
        The latest kubernetes version.


        :param maximum_version: The maximum_version of this KubernetesVersionsFilters.
        :type: str
        """
        self._maximum_version = maximum_version

    @property
    def exact_kubernetes_versions(self):
        """
        Gets the exact_kubernetes_versions of this KubernetesVersionsFilters.
        The exact version of kubernetes that are compatible.


        :return: The exact_kubernetes_versions of this KubernetesVersionsFilters.
        :rtype: list[str]
        """
        return self._exact_kubernetes_versions

    @exact_kubernetes_versions.setter
    def exact_kubernetes_versions(self, exact_kubernetes_versions):
        """
        Sets the exact_kubernetes_versions of this KubernetesVersionsFilters.
        The exact version of kubernetes that are compatible.


        :param exact_kubernetes_versions: The exact_kubernetes_versions of this KubernetesVersionsFilters.
        :type: list[str]
        """
        self._exact_kubernetes_versions = exact_kubernetes_versions

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
