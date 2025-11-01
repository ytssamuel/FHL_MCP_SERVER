"""驗證 reading_passage 重構效果"""

from src.fhl_bible_mcp.prompts.reading.reading_passage_new import ReadingPassagePrompt

def main():
    prompt = ReadingPassagePrompt()
    result = prompt.render()
    length = len(result)
    target = 700
    
    print("=" * 70)
    print("reading_passage 重構驗證")
    print("=" * 70)
    print(f"渲染長度: {length} 字")
    print(f"目標標準: {target} 字")
    if length <= target:
        print(f"超出比例: {((length - target) / target * 100):.1f}% (低於標準)")
        print(f"達標狀態: ✅ PASS")
    else:
        print(f"超出比例: +{((length - target) / target * 100):.1f}%")
        print(f"達標狀態: ❌ FAIL")
    print("=" * 70)
    print("\n渲染結果:")
    print("-" * 70)
    print(result)
    print("-" * 70)

if __name__ == "__main__":
    main()
