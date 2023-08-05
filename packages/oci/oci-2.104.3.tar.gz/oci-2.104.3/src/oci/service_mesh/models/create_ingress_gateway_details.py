# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class CreateIngressGatewayDetails(object):
    """
    The information about a new IngressGateway.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new CreateIngressGatewayDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param name:
            The value to assign to the name property of this CreateIngressGatewayDetails.
        :type name: str

        :param description:
            The value to assign to the description property of this CreateIngressGatewayDetails.
        :type description: str

        :param mesh_id:
            The value to assign to the mesh_id property of this CreateIngressGatewayDetails.
        :type mesh_id: str

        :param hosts:
            The value to assign to the hosts property of this CreateIngressGatewayDetails.
        :type hosts: list[oci.service_mesh.models.IngressGatewayHost]

        :param access_logging:
            The value to assign to the access_logging property of this CreateIngressGatewayDetails.
        :type access_logging: oci.service_mesh.models.AccessLoggingConfiguration

        :param mtls:
            The value to assign to the mtls property of this CreateIngressGatewayDetails.
        :type mtls: oci.service_mesh.models.IngressGatewayMutualTransportLayerSecurityDetails

        :param compartment_id:
            The value to assign to the compartment_id property of this CreateIngressGatewayDetails.
        :type compartment_id: str

        :param freeform_tags:
            The value to assign to the freeform_tags property of this CreateIngressGatewayDetails.
        :type freeform_tags: dict(str, str)

        :param defined_tags:
            The value to assign to the defined_tags property of this CreateIngressGatewayDetails.
        :type defined_tags: dict(str, dict(str, object))

        """
        self.swagger_types = {
            'name': 'str',
            'description': 'str',
            'mesh_id': 'str',
            'hosts': 'list[IngressGatewayHost]',
            'access_logging': 'AccessLoggingConfiguration',
            'mtls': 'IngressGatewayMutualTransportLayerSecurityDetails',
            'compartment_id': 'str',
            'freeform_tags': 'dict(str, str)',
            'defined_tags': 'dict(str, dict(str, object))'
        }

        self.attribute_map = {
            'name': 'name',
            'description': 'description',
            'mesh_id': 'meshId',
            'hosts': 'hosts',
            'access_logging': 'accessLogging',
            'mtls': 'mtls',
            'compartment_id': 'compartmentId',
            'freeform_tags': 'freeformTags',
            'defined_tags': 'definedTags'
        }

        self._name = None
        self._description = None
        self._mesh_id = None
        self._hosts = None
        self._access_logging = None
        self._mtls = None
        self._compartment_id = None
        self._freeform_tags = None
        self._defined_tags = None

    @property
    def name(self):
        """
        **[Required]** Gets the name of this CreateIngressGatewayDetails.
        A user-friendly name. The name has to be unique within the same service mesh and cannot be changed after creation.
        Avoid entering confidential information.

        Example: `My unique resource name`


        :return: The name of this CreateIngressGatewayDetails.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CreateIngressGatewayDetails.
        A user-friendly name. The name has to be unique within the same service mesh and cannot be changed after creation.
        Avoid entering confidential information.

        Example: `My unique resource name`


        :param name: The name of this CreateIngressGatewayDetails.
        :type: str
        """
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this CreateIngressGatewayDetails.
        Description of the resource. It can be changed after creation.
        Avoid entering confidential information.

        Example: `This is my new resource`


        :return: The description of this CreateIngressGatewayDetails.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this CreateIngressGatewayDetails.
        Description of the resource. It can be changed after creation.
        Avoid entering confidential information.

        Example: `This is my new resource`


        :param description: The description of this CreateIngressGatewayDetails.
        :type: str
        """
        self._description = description

    @property
    def mesh_id(self):
        """
        **[Required]** Gets the mesh_id of this CreateIngressGatewayDetails.
        The OCID of the service mesh in which this ingress gateway is created.


        :return: The mesh_id of this CreateIngressGatewayDetails.
        :rtype: str
        """
        return self._mesh_id

    @mesh_id.setter
    def mesh_id(self, mesh_id):
        """
        Sets the mesh_id of this CreateIngressGatewayDetails.
        The OCID of the service mesh in which this ingress gateway is created.


        :param mesh_id: The mesh_id of this CreateIngressGatewayDetails.
        :type: str
        """
        self._mesh_id = mesh_id

    @property
    def hosts(self):
        """
        **[Required]** Gets the hosts of this CreateIngressGatewayDetails.
        An array of hostnames and their listener configuration that this gateway will bind to.


        :return: The hosts of this CreateIngressGatewayDetails.
        :rtype: list[oci.service_mesh.models.IngressGatewayHost]
        """
        return self._hosts

    @hosts.setter
    def hosts(self, hosts):
        """
        Sets the hosts of this CreateIngressGatewayDetails.
        An array of hostnames and their listener configuration that this gateway will bind to.


        :param hosts: The hosts of this CreateIngressGatewayDetails.
        :type: list[oci.service_mesh.models.IngressGatewayHost]
        """
        self._hosts = hosts

    @property
    def access_logging(self):
        """
        Gets the access_logging of this CreateIngressGatewayDetails.

        :return: The access_logging of this CreateIngressGatewayDetails.
        :rtype: oci.service_mesh.models.AccessLoggingConfiguration
        """
        return self._access_logging

    @access_logging.setter
    def access_logging(self, access_logging):
        """
        Sets the access_logging of this CreateIngressGatewayDetails.

        :param access_logging: The access_logging of this CreateIngressGatewayDetails.
        :type: oci.service_mesh.models.AccessLoggingConfiguration
        """
        self._access_logging = access_logging

    @property
    def mtls(self):
        """
        Gets the mtls of this CreateIngressGatewayDetails.

        :return: The mtls of this CreateIngressGatewayDetails.
        :rtype: oci.service_mesh.models.IngressGatewayMutualTransportLayerSecurityDetails
        """
        return self._mtls

    @mtls.setter
    def mtls(self, mtls):
        """
        Sets the mtls of this CreateIngressGatewayDetails.

        :param mtls: The mtls of this CreateIngressGatewayDetails.
        :type: oci.service_mesh.models.IngressGatewayMutualTransportLayerSecurityDetails
        """
        self._mtls = mtls

    @property
    def compartment_id(self):
        """
        **[Required]** Gets the compartment_id of this CreateIngressGatewayDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :return: The compartment_id of this CreateIngressGatewayDetails.
        :rtype: str
        """
        return self._compartment_id

    @compartment_id.setter
    def compartment_id(self, compartment_id):
        """
        Sets the compartment_id of this CreateIngressGatewayDetails.
        The `OCID`__ of the compartment.

        __ https://docs.cloud.oracle.com/Content/General/Concepts/identifiers.htm


        :param compartment_id: The compartment_id of this CreateIngressGatewayDetails.
        :type: str
        """
        self._compartment_id = compartment_id

    @property
    def freeform_tags(self):
        """
        Gets the freeform_tags of this CreateIngressGatewayDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :return: The freeform_tags of this CreateIngressGatewayDetails.
        :rtype: dict(str, str)
        """
        return self._freeform_tags

    @freeform_tags.setter
    def freeform_tags(self, freeform_tags):
        """
        Sets the freeform_tags of this CreateIngressGatewayDetails.
        Simple key-value pair that is applied without any predefined name, type or scope. Exists for cross-compatibility only.
        Example: `{\"bar-key\": \"value\"}`


        :param freeform_tags: The freeform_tags of this CreateIngressGatewayDetails.
        :type: dict(str, str)
        """
        self._freeform_tags = freeform_tags

    @property
    def defined_tags(self):
        """
        Gets the defined_tags of this CreateIngressGatewayDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :return: The defined_tags of this CreateIngressGatewayDetails.
        :rtype: dict(str, dict(str, object))
        """
        return self._defined_tags

    @defined_tags.setter
    def defined_tags(self, defined_tags):
        """
        Sets the defined_tags of this CreateIngressGatewayDetails.
        Defined tags for this resource. Each key is predefined and scoped to a namespace.
        Example: `{\"foo-namespace\": {\"bar-key\": \"value\"}}`


        :param defined_tags: The defined_tags of this CreateIngressGatewayDetails.
        :type: dict(str, dict(str, object))
        """
        self._defined_tags = defined_tags

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
