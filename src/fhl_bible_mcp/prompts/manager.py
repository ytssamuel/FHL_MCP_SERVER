"""
FHL Bible MCP Server - Prompt Manager

管理所有 Prompt 模板
"""

from typing import Dict, List, Any, Optional
from .base import PromptTemplate
from .basic import (
    HelpGuidePrompt,
    URIDemoPrompt,
    QuickLookupPrompt,
    ToolReferencePrompt
)
from .study import (
    StudyVersePrompt,
    SearchTopicPrompt,
    CompareTranslationsPrompt,
    WordStudyPrompt
)


class PromptManager:
    """Prompt 管理器"""
    
    def __init__(self):
        """初始化 Prompt 管理器，註冊所有 prompts"""
        self.prompts: Dict[str, PromptTemplate] = {}
        
        # 註冊基礎 prompts (Phase 1 完成)
        self._register_prompt(HelpGuidePrompt())
        self._register_prompt(URIDemoPrompt())
        self._register_prompt(QuickLookupPrompt())
        self._register_prompt(ToolReferencePrompt())
        
        # 註冊研經 prompts
        self._register_prompt(StudyVersePrompt())
        self._register_prompt(SearchTopicPrompt())
        self._register_prompt(CompareTranslationsPrompt())
        self._register_prompt(WordStudyPrompt())
    
    def _register_prompt(self, prompt: PromptTemplate) -> None:
        """
        註冊一個 prompt
        
        Args:
            prompt: PromptTemplate 實例
        """
        self.prompts[prompt.name] = prompt
    
    def get_prompt(self, name: str) -> Optional[PromptTemplate]:
        """
        根據名稱獲取 prompt 模板
        
        Args:
            name: Prompt 名稱
            
        Returns:
            PromptTemplate 對象，如果不存在則返回 None
        """
        return self.prompts.get(name)
    
    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        列出所有可用的 prompts
        
        Returns:
            Prompt 資訊列表
        """
        return [
            {
                "name": prompt.name,
                "description": prompt.description,
                "arguments": prompt.arguments
            }
            for prompt in self.prompts.values()
        ]
    
    def render_prompt(self, name: str, **kwargs) -> Optional[str]:
        """
        渲染指定的 prompt
        
        Args:
            name: Prompt 名稱
            **kwargs: Prompt 參數
            
        Returns:
            渲染後的 prompt 字符串，如果 prompt 不存在則返回 None
        """
        prompt = self.get_prompt(name)
        if prompt:
            # 驗證參數
            if not prompt.validate_arguments(**kwargs):
                return None
            return prompt.render(**kwargs)
        return None
    
    def get_prompt_names(self) -> List[str]:
        """
        獲取所有 prompt 名稱列表
        
        Returns:
            Prompt 名稱列表
        """
        return list(self.prompts.keys())
    
    def has_prompt(self, name: str) -> bool:
        """
        檢查是否存在指定名稱的 prompt
        
        Args:
            name: Prompt 名稱
            
        Returns:
            True 如果存在，否則 False
        """
        return name in self.prompts
