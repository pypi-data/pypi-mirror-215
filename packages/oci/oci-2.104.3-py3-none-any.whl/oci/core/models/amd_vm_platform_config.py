# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from .platform_config import PlatformConfig
from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class AmdVmPlatformConfig(PlatformConfig):
    """
    The platform configuration of a virtual machine instance that uses the AMD platform.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new AmdVmPlatformConfig object with values from keyword arguments. The default value of the :py:attr:`~oci.core.models.AmdVmPlatformConfig.type` attribute
        of this class is ``AMD_VM`` and it should not be changed.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param type:
            The value to assign to the type property of this AmdVmPlatformConfig.
            Allowed values for this property are: "AMD_MILAN_BM", "AMD_MILAN_BM_GPU", "AMD_ROME_BM", "AMD_ROME_BM_GPU", "INTEL_ICELAKE_BM", "INTEL_SKYLAKE_BM", "AMD_VM", "INTEL_VM"
        :type type: str

        :param is_secure_boot_enabled:
            The value to assign to the is_secure_boot_enabled property of this AmdVmPlatformConfig.
        :type is_secure_boot_enabled: bool

        :param is_trusted_platform_module_enabled:
            The value to assign to the is_trusted_platform_module_enabled property of this AmdVmPlatformConfig.
        :type is_trusted_platform_module_enabled: bool

        :param is_measured_boot_enabled:
            The value to assign to the is_measured_boot_enabled property of this AmdVmPlatformConfig.
        :type is_measured_boot_enabled: bool

        :param is_memory_encryption_enabled:
            The value to assign to the is_memory_encryption_enabled property of this AmdVmPlatformConfig.
        :type is_memory_encryption_enabled: bool

        """
        self.swagger_types = {
            'type': 'str',
            'is_secure_boot_enabled': 'bool',
            'is_trusted_platform_module_enabled': 'bool',
            'is_measured_boot_enabled': 'bool',
            'is_memory_encryption_enabled': 'bool'
        }

        self.attribute_map = {
            'type': 'type',
            'is_secure_boot_enabled': 'isSecureBootEnabled',
            'is_trusted_platform_module_enabled': 'isTrustedPlatformModuleEnabled',
            'is_measured_boot_enabled': 'isMeasuredBootEnabled',
            'is_memory_encryption_enabled': 'isMemoryEncryptionEnabled'
        }

        self._type = None
        self._is_secure_boot_enabled = None
        self._is_trusted_platform_module_enabled = None
        self._is_measured_boot_enabled = None
        self._is_memory_encryption_enabled = None
        self._type = 'AMD_VM'

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
