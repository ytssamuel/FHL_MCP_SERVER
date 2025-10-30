"""
快速修正工具：將 response.field 改為 response["field"]
"""

import re
import glob

def fix_file(filepath):
    """修正單一檔案"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 修正 response.xxx 為 response["xxx"]
    # 只修正在 response 後面的屬性存取
    patterns = [
        (r'response\.record_count', 'response["record_count"]'),
        (r'response\.record\b', 'response["record"]'),
        (r'response\.version\b', 'response["version"]'),
        (r'response\.v_name', 'response["v_name"]'),
        (r'response\.prev\b', 'response.get("prev")'),
        (r'response\.next\b', 'response.get("next")'),
        (r'response\.N\b', 'response["N"]'),
        (r'response\.name\b', 'response["name"]'),
        (r'response\.chinesef\b', 'response["chinesef"]'),
        (r'response\.engf\b', 'response["engf"]'),
        (r'response\.chap\b', 'response["chap"]'),
        (r'response\.mp3\b', 'response.get("mp3")'),
        (r'response\.ogg\b', 'response.get("ogg")'),
        (r'response\.pbid\b', 'response.get("pbid")'),
        (r'response\.pchinesef\b', 'response.get("pchinesef")'),
        (r'response\.pchap\b', 'response.get("pchap")'),
        (r'response\.nbid\b', 'response.get("nbid")'),
        (r'response\.nchinesef\b', 'response.get("nchinesef")'),
        (r'response\.nchap\b', 'response.get("nchap")'),
        # record 內的屬性
        (r'record\.id\b', 'record["id"]'),
        (r'record\.name\b', 'record["name"]'),
        (r'record\.book_name', 'record["book_name"]'),
        (r'record\.title\b', 'record.get("title", "")'),
        (r'record\.com_text', 'record.get("com_text", "")'),
        (r'record\.prev\b', 'record.get("prev")'),
        (r'record\.next\b', 'record.get("next")'),
        (r'record\.tag\b', 'record["tag"]'),
        (r'record\.chinesef\b', 'record["chinesef"]'),
        (r'record\.engs\b', 'record["engs"]'),
        (r'record\.bchap\b', 'record["bchap"]'),
        (r'record\.bsec\b', 'record["bsec"]'),
        (r'record\.echap\b', 'record["echap"]'),
        (r'record\.esec\b', 'record["esec"]'),
        (r'record\.book\b', 'record["book"]'),
        (r'record\.topic\b', 'record.get("topic", "")'),
        (r'record\.text\b', 'record.get("text", "")'),
        # version 內的屬性
        (r'record\.cname\b', 'record["cname"]'),
        (r'record\.proc\b', 'record["proc"]'),
        (r'record\.strong\b', 'record["strong"]'),
        (r'record\.ntonly\b', 'record["ntonly"]'),
        (r'record\.otonly\b', 'record["otonly"]'),
        (r'record\.candownload\b', 'record["candownload"]'),
        (r'record\.version\b', 'record.get("version", "")'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 修正: {filepath}")
        return True
    else:
        print(f"- 跳過: {filepath} (無需修正)")
        return False

def main():
    """修正所有工具檔案"""
    tools_files = glob.glob("src/fhl_bible_mcp/tools/*.py")
    
    fixed_count = 0
    for filepath in tools_files:
        if filepath.endswith("__init__.py"):
            continue
        if fix_file(filepath):
            fixed_count += 1
    
    print(f"\n完成！共修正 {fixed_count} 個檔案")

if __name__ == "__main__":
    main()
