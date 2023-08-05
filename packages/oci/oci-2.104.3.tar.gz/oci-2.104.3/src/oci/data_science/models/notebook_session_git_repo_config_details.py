# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class NotebookSessionGitRepoConfigDetails(object):
    """
    Git repository configurations.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new NotebookSessionGitRepoConfigDetails object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param url:
            The value to assign to the url property of this NotebookSessionGitRepoConfigDetails.
        :type url: str

        """
        self.swagger_types = {
            'url': 'str'
        }

        self.attribute_map = {
            'url': 'url'
        }

        self._url = None

    @property
    def url(self):
        """
        **[Required]** Gets the url of this NotebookSessionGitRepoConfigDetails.
        The repository URL


        :return: The url of this NotebookSessionGitRepoConfigDetails.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """
        Sets the url of this NotebookSessionGitRepoConfigDetails.
        The repository URL


        :param url: The url of this NotebookSessionGitRepoConfigDetails.
        :type: str
        """
        self._url = url

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
