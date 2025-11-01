"""驗證 basic_tool_reference 重構效果"""

from src.fhl_bible_mcp.prompts.basic.basic_tool_reference import BasicToolReferencePrompt

def main():
    prompt = BasicToolReferencePrompt()
    result = prompt.render()
    length = len(result)
    target = 500
    
    print("=" * 70)
    print("basic_tool_reference 重構驗證")
    print("=" * 70)
    print(f"渲染長度: {length} 字")
    print(f"目標標準: {target} 字")
    print(f"超出比例: {((length - target) / target * 100):.1f}%")
    print(f"達標狀態: {'✅ PASS' if length <= target else '❌ FAIL'}")
    print("=" * 70)
    print("\n渲染結果:")
    print("-" * 70)
    print(result)
    print("-" * 70)

if __name__ == "__main__":
    main()
