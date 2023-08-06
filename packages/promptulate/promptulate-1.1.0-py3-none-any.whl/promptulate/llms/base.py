# Copyright (c) 2023 Zeeland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright Owner: Zeeland
# GitHub Link: https://github.com/Undertone0809/
# Project Link: https://github.com/Undertone0809/promptulate
# Contact Email: zeeland@foxmail.com

from typing import Any
from pydantic import BaseModel, Extra
from abc import ABC, abstractmethod
from promptulate.schema import AssistantMessage
from promptulate.schema import LLMPrompt


class BaseLLM(BaseModel, ABC):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @abstractmethod
    def generate_prompt(self, prompts: LLMPrompt) -> AssistantMessage:
        """llm generate prompt"""

    @abstractmethod
    def _parse_prompt(self, prompts: LLMPrompt) -> Any:
        """parse prompt"""

    @abstractmethod
    def __call__(self, prompt, *args, **kwargs):
        """input string prompt return answer"""
