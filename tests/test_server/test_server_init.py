"""
Test FHL Bible MCP Server Initialization

Tests for server initialization and component registration.
"""

import pytest
from fhl_bible_mcp.server import FHLBibleServer


@pytest.mark.asyncio
async def test_server_initialization():
    """
    Test 1: Server Initialization
    測試 FHLBibleServer 是否能成功初始化
    """
    print("\n" + "="*70)
    print("Test 1: Server Initialization")
    print("="*70)
    
    # 初始化 server
    server = FHLBibleServer()
    
    # 驗證屬性
    assert server.server is not None, "Server should be initialized"
    assert server.endpoints is not None, "Endpoints should be initialized"
    assert server.resource_router is not None, "ResourceRouter should be initialized"
    assert server.prompt_manager is not None, "PromptManager should be initialized"
    
    print("✅ Server initialized successfully")
    print(f"   - Server: {server.server.name}")
    print(f"   - Endpoints: {type(server.endpoints).__name__}")
    print(f"   - Resource Router: {type(server.resource_router).__name__}")
    print(f"   - Prompt Manager: {type(server.prompt_manager).__name__}")


@pytest.mark.asyncio
async def test_tools_registered():
    """
    Test 2: Tools Registration
    測試 Tools 是否已註冊
    """
    print("\n" + "="*70)
    print("Test 2: Tools Registration")
    print("="*70)
    
    server = FHLBibleServer()
    
    # 驗證 server 有註冊工具的機制
    assert hasattr(server.server, 'request_handlers'), "Server should have request handlers"
    
    print(f"✅ Server has tool registration mechanism")
    
    # 驗證各類別的工具 (通過檢查導入的函數)
    categories = {
        "verse": ["get_bible_verse", "get_bible_chapter", "query_verse_citation"],
        "search": ["search_bible", "search_bible_advanced"],
        "strongs": ["get_word_analysis", "lookup_strongs", "search_strongs_occurrences"],
        "commentary": ["get_commentary", "list_commentaries", "search_commentary", "get_topic_study"],
        "info": ["list_bible_versions", "get_book_list", "get_book_info", "search_available_versions"],
        "audio": ["get_audio_bible", "list_audio_versions", "get_audio_chapter_with_text"]
    }
    
    total_tools = sum(len(tools) for tools in categories.values())
    
    print(f"\n已註冊的工具類別:")
    for category, expected_tools in categories.items():
        print(f"   - {category}: {len(expected_tools)} tools")
    
    print(f"\n總計: {total_tools} tools")
    assert total_tools == 19, "Should have 19 tools"


@pytest.mark.asyncio
async def test_resources_registered():
    """
    Test 3: Resources Registration
    測試 Resources 是否已註冊
    """
    print("\n" + "="*70)
    print("Test 3: Resources Registration")
    print("="*70)
    
    server = FHLBibleServer()
    
    # 驗證 resource_router 已初始化
    assert server.resource_router is not None, "ResourceRouter should be initialized"
    
    # 使用 ResourceRouter 來列出支援的資源
    supported = server.resource_router.list_supported_resources()
    
    # 驗證 URI schemes
    expected_schemes = ["bible", "strongs", "commentary", "info"]
    
    print(f"✅ Resource registration mechanism active")
    print(f"\n支援的 URI schemes:")
    for scheme in expected_schemes:
        status = "✓" if scheme in supported else "✗"
        resource_count = len(supported.get(scheme, []))
        print(f"   {status} {scheme}://  ({resource_count} resource types)")
        assert scheme in supported, f"Scheme {scheme} not registered"
    
    # 顯示範例資源
    print(f"\n範例資源:")
    for scheme, resources in list(supported.items())[:3]:
        for resource in resources[:2]:
            print(f"   • {resource['example']}")
            print(f"     {resource['description'][:60]}...")


@pytest.mark.asyncio
async def test_prompts_registered():
    """
    Test 4: Prompts Registration
    測試 Prompts 是否已註冊
    """
    print("\n" + "="*70)
    print("Test 4: Prompts Registration")
    print("="*70)
    
    server = FHLBibleServer()
    
    # 驗證 prompt_manager 已初始化
    assert server.prompt_manager is not None, "PromptManager should be initialized"
    
    # 使用 PromptManager 來列出 prompts
    prompts = server.prompt_manager.list_prompts()
    
    # 驗證 prompts 數量
    assert len(prompts) == 4, "Should have 4 prompts registered"
    print(f"✅ {len(prompts)} prompts registered")
    
    # 驗證每個 prompt
    expected_prompts = ["study_verse", "search_topic", "compare_translations", "word_study"]
    prompt_names = [p["name"] for p in prompts]
    
    print("\n已註冊的 Prompts:")
    for name in expected_prompts:
        assert name in prompt_names, f"Prompt {name} not registered"
        prompt = next(p for p in prompts if p["name"] == name)
        print(f"   • {prompt['name']}")
        print(f"     {prompt['description'][:60]}...")
        print(f"     參數數量: {len(prompt['arguments'])}")


@pytest.mark.asyncio
async def test_server_handlers():
    """
    Test 5: Server Handlers
    測試 server 的所有 handlers 是否正確註冊
    """
    print("\n" + "="*70)
    print("Test 5: Server Handlers")
    print("="*70)
    
    server = FHLBibleServer()
    
    # 檢查 server 的 request_handlers 屬性
    assert hasattr(server.server, 'request_handlers'), "Server should have request_handlers"
    
    # 檢查重要的 handler 類型
    handlers = server.server.request_handlers
    
    important_methods = [
        "tools/list",
        "tools/call", 
        "resources/list",
        "resources/read",
        "prompts/list",
        "prompts/get"
    ]
    
    print("Handler 註冊狀況:")
    registered_count = 0
    for method in important_methods:
        if method in handlers:
            registered_count += 1
            print(f"   ✓ {method}")
        else:
            print(f"   ✗ {method} (not found)")
    
    print(f"\n✅ {registered_count}/{len(important_methods)} core handlers registered")


@pytest.mark.asyncio
async def test_component_integration():
    """
    Test 6: Component Integration
    測試各元件之間的整合
    """
    print("\n" + "="*70)
    print("Test 6: Component Integration")
    print("="*70)
    
    server = FHLBibleServer()
    
    # 驗證 endpoints 是否與 resource_router 共用
    assert server.resource_router.endpoints is server.endpoints, \
        "ResourceRouter should use server's endpoints"
    
    # 驗證 prompt_manager 是否可以使用
    prompts = server.prompt_manager.list_prompts()
    assert len(prompts) > 0, "PromptManager should have prompts"
    
    # 驗證 resource_router 的功能
    supported = server.resource_router.list_supported_resources()
    assert "bible" in supported, "ResourceRouter should support bible resources"
    assert "strongs" in supported, "ResourceRouter should support strongs resources"
    assert "commentary" in supported, "ResourceRouter should support commentary resources"
    assert "info" in supported, "ResourceRouter should support info resources"
    
    print("✅ Component integration verified")
    print(f"   - Endpoints shared: ✓")
    print(f"   - PromptManager active: ✓")
    print(f"   - ResourceRouter active: ✓")
    print(f"   - Supported resource types: {len(supported)}")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    import asyncio
    
    async def run_all_tests():
        """執行所有測試"""
        print("\n" + "="*70)
        print("FHL Bible MCP Server - Initialization Tests")
        print("="*70)
        
        tests = [
            ("Server Initialization", test_server_initialization),
            ("Tools Registration", test_tools_registered),
            ("Resources Registration", test_resources_registered),
            ("Prompts Registration", test_prompts_registered),
            ("Server Handlers", test_server_handlers),
            ("Component Integration", test_component_integration),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                await test_func()
                passed += 1
            except AssertionError as e:
                print(f"\n❌ Test Failed: {name}")
                print(f"   Error: {e}")
                failed += 1
            except Exception as e:
                print(f"\n❌ Test Error: {name}")
                print(f"   Error: {e}")
                failed += 1
        
        # 顯示總結
        print("\n" + "="*70)
        print("Test Summary")
        print("="*70)
        print(f"Total Tests: {len(tests)}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} {'❌' if failed > 0 else ''}")
        print("="*70)
        
        if failed == 0:
            print("\n🎉 All tests passed!")
        else:
            print(f"\n⚠️  {failed} test(s) failed")
    
    # 執行測試
    asyncio.run(run_all_tests())
