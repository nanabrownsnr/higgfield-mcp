"""Tool and UI integration tests."""

import pytest
from fastmcp.server import Server

from app.main import app
from app.tools.api_call import APICallInput
from app.tools.files import FILE_ROOT


@pytest.mark.asyncio
async def test_api_call_tool_has_ui_contract():
    """Verify API call tool has proper UI integration contract."""
    from app.tools.api_call import call_external

    # Check tool definition
    assert call_external.name == "call_external"
    assert "model" in call_external.app_config.get("visibility", [])
    assert "app" in call_external.app_config.get("visibility", [])

    # Check tool description
    assert "external API" in call_external.description.lower()

    # Check app_config includes ui_resource_uri
    assert "ui_resource_uri" in call_external.app_config


@pytest.mark.asyncio
async def test_files_tool_has_ui_contract():
    """Verify files tool has proper UI integration contract."""
    from app.tools.files import list_dir, get_file

    # Check list_dir tool
    assert list_dir.name == "list_dir"
    assert list_dir.app_config.get("ui_resource_uri") == "ui://file-browser"

    # Check get_file tool
    assert get_file.name == "get_file"
    assert get_file.app_config.get("ui_resource_uri") == "ui://file-viewer"


@pytest.mark.asyncio
async def test_files_tool_creates_directory():
    """Test that file directory is created if it doesn't exist."""
    # Create temporary owner directory
    test_dir = FILE_ROOT / "test-owner"
    test_dir.mkdir(exist_ok=True)

    try:
        # Should create directory if it doesn't exist
        result = await list_dir(path=".")
        assert "items" in result
        assert isinstance(result["items"], list)
    finally:
        # Clean up
        if test_dir.exists():
            test_dir.rmdir()


@pytest.mark.asyncio
async def test_files_tool_returns_errors_properly():
    """Test file tools return proper error responses."""
    # Test non-existent file
    result = await get_file(path="nonexistent.txt")
    assert result.get("error") == "not found"


@pytest.mark.asyncio
async def test_files_tool_binary_image():
    """Test binary image file handling."""
    # Create a test image
    test_file = FILE_ROOT / "test-owner" / "test.png"
    test_file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    try:
        result = await get_file(path="test.png")
        assert "contentType" in result
        assert result["contentType"] == "image.png"
        assert "content" in result
        assert isinstance(result["content"], str)
    finally:
        if test_file.exists():
            test_file.unlink()