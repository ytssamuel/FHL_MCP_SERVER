"""
FHL Bible MCP Server - Prompt Base Classes

提供 Prompt 的基礎類別和共用功能
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class PromptTemplate:
    """Prompt 範本基類"""
    name: str
    description: str
    arguments: List[Dict[str, Any]]
    
    def render(self, **kwargs) -> str:
        """
        渲染 prompt 模板
        
        Args:
            **kwargs: 模板參數
            
        Returns:
            渲染後的 prompt 字符串
        """
        raise NotImplementedError("Subclasses must implement render method")
    
    def validate_arguments(self, **kwargs) -> bool:
        """
        驗證參數是否符合要求
        
        Args:
            **kwargs: 要驗證的參數
            
        Returns:
            True if valid, False otherwise
        """
        for arg in self.arguments:
            arg_name = arg["name"]
            is_required = arg.get("required", False)
            
            if is_required and arg_name not in kwargs:
                raise ValueError(f"Missing required argument: {arg_name}")
        
        return True
    
    def get_argument_info(self) -> List[Dict[str, Any]]:
        """
        獲取參數資訊
        
        Returns:
            參數列表
        """
        return self.arguments
