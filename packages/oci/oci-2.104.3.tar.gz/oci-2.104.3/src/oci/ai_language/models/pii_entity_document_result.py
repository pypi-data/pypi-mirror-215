# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.


from oci.util import formatted_flat_dict, NONE_SENTINEL, value_allowed_none_or_none_sentinel  # noqa: F401
from oci.decorators import init_model_state_from_kwargs


@init_model_state_from_kwargs
class PiiEntityDocumentResult(object):
    """
    The document response for batch detect personal identification.
    """

    def __init__(self, **kwargs):
        """
        Initializes a new PiiEntityDocumentResult object with values from keyword arguments.
        The following keyword arguments are supported (corresponding to the getters/setters of this class):

        :param key:
            The value to assign to the key property of this PiiEntityDocumentResult.
        :type key: str

        :param entities:
            The value to assign to the entities property of this PiiEntityDocumentResult.
        :type entities: list[oci.ai_language.models.PiiEntity]

        :param masked_text:
            The value to assign to the masked_text property of this PiiEntityDocumentResult.
        :type masked_text: str

        :param language_code:
            The value to assign to the language_code property of this PiiEntityDocumentResult.
        :type language_code: str

        """
        self.swagger_types = {
            'key': 'str',
            'entities': 'list[PiiEntity]',
            'masked_text': 'str',
            'language_code': 'str'
        }

        self.attribute_map = {
            'key': 'key',
            'entities': 'entities',
            'masked_text': 'maskedText',
            'language_code': 'languageCode'
        }

        self._key = None
        self._entities = None
        self._masked_text = None
        self._language_code = None

    @property
    def key(self):
        """
        **[Required]** Gets the key of this PiiEntityDocumentResult.
        Document unique identifier defined by the user.


        :return: The key of this PiiEntityDocumentResult.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        Sets the key of this PiiEntityDocumentResult.
        Document unique identifier defined by the user.


        :param key: The key of this PiiEntityDocumentResult.
        :type: str
        """
        self._key = key

    @property
    def entities(self):
        """
        **[Required]** Gets the entities of this PiiEntityDocumentResult.
        List of batch detect personal identification.


        :return: The entities of this PiiEntityDocumentResult.
        :rtype: list[oci.ai_language.models.PiiEntity]
        """
        return self._entities

    @entities.setter
    def entities(self, entities):
        """
        Sets the entities of this PiiEntityDocumentResult.
        List of batch detect personal identification.


        :param entities: The entities of this PiiEntityDocumentResult.
        :type: list[oci.ai_language.models.PiiEntity]
        """
        self._entities = entities

    @property
    def masked_text(self):
        """
        **[Required]** Gets the masked_text of this PiiEntityDocumentResult.
        Masked text per given mask mode.


        :return: The masked_text of this PiiEntityDocumentResult.
        :rtype: str
        """
        return self._masked_text

    @masked_text.setter
    def masked_text(self, masked_text):
        """
        Sets the masked_text of this PiiEntityDocumentResult.
        Masked text per given mask mode.


        :param masked_text: The masked_text of this PiiEntityDocumentResult.
        :type: str
        """
        self._masked_text = masked_text

    @property
    def language_code(self):
        """
        **[Required]** Gets the language_code of this PiiEntityDocumentResult.
        Language code supported
        Automatically detect language - auto
        Arabic - ar
        Brazilian Portuguese -  pt-BR
        Czech - cs
        Danish - da
        Dutch - nl
        English - en
        Finnish - fi
        French - fr
        Canadian French - fr-CA
        German - de
        Italian - it
        Japanese - ja
        Korean - ko
        Norwegian - no
        Polish - pl
        Romanian - ro
        Simplified Chinese - zh-CN
        Spanish - es
        Swedish - sv
        Traditional Chinese - zh-TW
        Turkish - tr
        Greek - el
        Hebrew - he


        :return: The language_code of this PiiEntityDocumentResult.
        :rtype: str
        """
        return self._language_code

    @language_code.setter
    def language_code(self, language_code):
        """
        Sets the language_code of this PiiEntityDocumentResult.
        Language code supported
        Automatically detect language - auto
        Arabic - ar
        Brazilian Portuguese -  pt-BR
        Czech - cs
        Danish - da
        Dutch - nl
        English - en
        Finnish - fi
        French - fr
        Canadian French - fr-CA
        German - de
        Italian - it
        Japanese - ja
        Korean - ko
        Norwegian - no
        Polish - pl
        Romanian - ro
        Simplified Chinese - zh-CN
        Spanish - es
        Swedish - sv
        Traditional Chinese - zh-TW
        Turkish - tr
        Greek - el
        Hebrew - he


        :param language_code: The language_code of this PiiEntityDocumentResult.
        :type: str
        """
        self._language_code = language_code

    def __repr__(self):
        return formatted_flat_dict(self)

    def __eq__(self, other):
        if other is None:
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other
