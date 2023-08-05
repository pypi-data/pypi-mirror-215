# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectDominantLanguageResult(object):
    """
    Result of language detect call.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new DetectDominantLanguageResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param languages:
            The value to assign to the languages property of this DetectDominantLanguageResult.
        :type languages: list[oci.ai_language.models.DetectedLanguage]

        """
        self.swagger_types = {
            'languages': 'list[DetectedLanguage]'
        }

        self.attribute_map = {
            'languages': 'languages'
        }

        self._languages = None

    @property
    def languages(self):
        """
        **[Required]** Gets the languages of this DetectDominantLanguageResult.
        List of detected languages with results sorted in descending order of the scores. Most likely language is on top.


        :return: The languages of this DetectDominantLanguageResult.
        :rtype: list[oci.ai_language.models.DetectedLanguage]
        """
        return self._languages

    @languages.setter
    def languages(self, languages):
        """
        Sets the languages of this DetectDominantLanguageResult.
        List of detected languages with results sorted in descending order of the scores. Most likely language is on top.


        :param languages: The languages of this DetectDominantLanguageResult.
        :type: list[oci.ai_language.models.DetectedLanguage]
        """
        self._languages = languages

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
