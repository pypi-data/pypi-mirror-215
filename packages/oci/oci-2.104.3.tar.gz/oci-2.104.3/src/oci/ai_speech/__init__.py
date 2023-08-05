# coding: utf-8
# Copyright (c) 2016, 2023, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.

from __future__ import absolute_import


from .ai_service_speech_client import AIServiceSpeechClient
from .ai_service_speech_client_composite_operations import AIServiceSpeechClientCompositeOperations
from . import models

__all__ = ["AIServiceSpeechClient", "AIServiceSpeechClientCompositeOperations", "models"]
