"""
Basic prompts module - 基礎入門 Prompts
"""

from .help_guide import HelpGuidePrompt
from .uri_demo import URIDemoPrompt
from .quick_lookup import QuickLookupPrompt
from .tool_reference import ToolReferencePrompt

__all__ = [
    'HelpGuidePrompt',
    'URIDemoPrompt',
    'QuickLookupPrompt',
    'ToolReferencePrompt',
]
