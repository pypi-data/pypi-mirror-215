# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class DetectedLanguage(object):
    """
    The language detected in a document.
    """

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "ENG"
    LANGUAGE_CODE_ENG = "ENG"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "CES"
    LANGUAGE_CODE_CES = "CES"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "DAN"
    LANGUAGE_CODE_DAN = "DAN"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "NLD"
    LANGUAGE_CODE_NLD = "NLD"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "FIN"
    LANGUAGE_CODE_FIN = "FIN"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "FRA"
    LANGUAGE_CODE_FRA = "FRA"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "DEU"
    LANGUAGE_CODE_DEU = "DEU"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "ELL"
    LANGUAGE_CODE_ELL = "ELL"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "HUN"
    LANGUAGE_CODE_HUN = "HUN"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "ITA"
    LANGUAGE_CODE_ITA = "ITA"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "NOR"
    LANGUAGE_CODE_NOR = "NOR"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "POL"
    LANGUAGE_CODE_POL = "POL"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "POR"
    LANGUAGE_CODE_POR = "POR"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "RON"
    LANGUAGE_CODE_RON = "RON"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "RUS"
    LANGUAGE_CODE_RUS = "RUS"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "SLK"
    LANGUAGE_CODE_SLK = "SLK"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "SPA"
    LANGUAGE_CODE_SPA = "SPA"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "SWE"
    LANGUAGE_CODE_SWE = "SWE"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "TUR"
    LANGUAGE_CODE_TUR = "TUR"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "ARA"
    LANGUAGE_CODE_ARA = "ARA"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "CHI_SIM"
    LANGUAGE_CODE_CHI_SIM = "CHI_SIM"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "HIN"
    LANGUAGE_CODE_HIN = "HIN"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "JPN"
    LANGUAGE_CODE_JPN = "JPN"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "KOR"
    LANGUAGE_CODE_KOR = "KOR"

    #: A constant which can be used with the language_code property of a DetectedLanguage.
    #: This constant has a value of "OTHERS"
    LANGUAGE_CODE_OTHERS = "OTHERS"

    def __init__(self, **kwargs):
        """
        Initializes a new DetectedLanguage object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param language_code:
            The value to assign to the language_code property of this DetectedLanguage.
            Allowed values for this property are: "ENG", "CES", "DAN", "NLD", "FIN", "FRA", "DEU", "ELL", "HUN", "ITA", "NOR", "POL", "POR", "RON", "RUS", "SLK", "SPA", "SWE", "TUR", "ARA", "CHI_SIM", "HIN", "JPN", "KOR", "OTHERS", 'UNKNOWN_ENUM_VALUE'.
            Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.
        :type language_code: str

        :param confidence:
            The value to assign to the confidence property of this DetectedLanguage.
        :type confidence: float

        """
        self.swagger_types = {
            'language_code': 'str',
            'confidence': 'float'
        }

        self.attribute_map = {
            'language_code': 'languageCode',
            'confidence': 'confidence'
        }

        self._language_code = None
        self._confidence = None

    @property
    def language_code(self):
        """
        **[Required]** Gets the language_code of this DetectedLanguage.
        The language of the document, abbreviated according to ISO 639-2.

        Allowed values for this property are: "ENG", "CES", "DAN", "NLD", "FIN", "FRA", "DEU", "ELL", "HUN", "ITA", "NOR", "POL", "POR", "RON", "RUS", "SLK", "SPA", "SWE", "TUR", "ARA", "CHI_SIM", "HIN", "JPN", "KOR", "OTHERS", 'UNKNOWN_ENUM_VALUE'.
        Any unrecognized values returned by a service will be mapped to 'UNKNOWN_ENUM_VALUE'.


        :return: The language_code of this DetectedLanguage.
        :rtype: str
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code):
        """
        Sets the language_code of this DetectedLanguage.
        The language of the document, abbreviated according to ISO 639-2.


        :param language_code: The language_code of this DetectedLanguage.
        :type: str
        """
        allowed_values = ["ENG", "CES", "DAN", "NLD", "FIN", "FRA", "DEU", "ELL", "HUN", "ITA", "NOR", "POL", "POR", "RON", "RUS", "SLK", "SPA", "SWE", "TUR", "ARA", "CHI_SIM", "HIN", "JPN", "KOR", "OTHERS"]
        if not value_allowed_none_or_none_sentinel(language_code, allowed_values):
            language_code = 'UNKNOWN_ENUM_VALUE'
        self._language_code = language_code

    @property
    def confidence(self):
        """
        **[Required]** Gets the confidence of this DetectedLanguage.
        The confidence score between 0 and 1.


        :return: The confidence of this DetectedLanguage.
        :rtype: float
        """
        return self._confidence

    @confidence.setter
    def confidence(self, confidence):
        """
        Sets the confidence of this DetectedLanguage.
        The confidence score between 0 and 1.


        :param confidence: The confidence of this DetectedLanguage.
        :type: float
        """
        self._confidence = confidence

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
