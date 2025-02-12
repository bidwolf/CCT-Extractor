"""
Configuration settings for the OpenAI API.
"""

from typing import TypedDict
from openai.types.beta.assistant_response_format_option_param import (
    AssistantResponseFormatOptionParam,
)
from openai.types.beta.assistant_tool_param import AssistantToolParam


class Config(TypedDict):
    """
    Configuration settings for the OpenAI API.
    """

    api_key: str
    assistant_id: str
    assistant_description: str
    assistant_model: str
    assistant_instructions: str
    cct_directory: str
    response_format: AssistantResponseFormatOptionParam | None
    tools: list[AssistantToolParam] | None
    # tool_resources: dict
    # tool_resources: dict[str, dict[str, list[str]]]
