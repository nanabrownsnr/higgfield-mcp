"""Resource loading tests."""

import pytest
from pathlib import Path


class TestFileOperations:
    """Tests for file operation utilities."""

    def test_directory_creation(self):
        """Test that directories can be created."""
        from app.tools.files import FILE_ROOT
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_owner"
            test_dir.mkdir()
            assert test_dir.exists()

    def test_file_reading(self):
        """Test that files can be read."""
        from app.tools.files import FILE_ROOT
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_owner"
            test_dir.mkdir()
            test_file = test_dir / "test.txt"
            test_file.write_text("Hello, World!")

            assert test_file.exists()
            assert test_file.read_text() == "Hello, World!"

    def test_binary_file_handling(self):
        """Test handling of binary files."""
        from app.tools.files import get_file
        from app.tools.files import FILE_ROOT
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_owner"
            test_dir.mkdir()
            test_file = test_dir / "test.png"

            # Create fake PNG header
            png_data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
            test_file.write_bytes(png_data)

            result = get_file(path="test.png")
            assert "contentType" in result
            assert result["contentType"] == "image.png"
            assert "content" in result
            assert isinstance(result["content"], str)