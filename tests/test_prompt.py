import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from pydantic import ValidationError

from scansheet_agent import PromptBuilder
from langchain_core.prompts import ChatPromptTemplate


class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.prompt_builder = PromptBuilder(templates_dir="templates")

    def test_init(self):
        """Test PromptBuilder initialization."""
        self.assertEqual(self.prompt_builder.templates_dir, Path("templates"))

        # Test with custom templates directory
        custom_builder = PromptBuilder(templates_dir="custom_templates")
        self.assertEqual(custom_builder.templates_dir, Path("custom_templates"))

    @patch("builtins.open", new_callable=mock_open, read_data="Test template content")
    @patch("pathlib.Path.resolve")
    def test_read_template(self, mock_resolve, mock_file):
        """Test reading template from file."""
        # Setup
        mock_current_path = MagicMock()
        mock_resolve.return_value = mock_current_path
        mock_parent = MagicMock()
        mock_current_path.parent = mock_parent
        mock_templates_path = MagicMock()
        mock_parent.__truediv__.return_value = mock_templates_path
        mock_file_path = Path("mocked_path")
        mock_templates_path.__truediv__.return_value = mock_file_path

        # Call the method
        result = self.prompt_builder._read_template("test_template.txt")

        # Assertions
        mock_file.assert_called_once_with(mock_file_path, "r", encoding="utf-8")
        self.assertEqual(result, "Test template content")

    @patch("builtins.open", new_callable=mock_open, read_data="Test document instructions")
    @patch("pathlib.Path.resolve")
    def test_read_template_with_document_instructions(self, mock_resolve, mock_file):
        """Test reading document instructions template from file."""
        # Setup
        mock_current_path = MagicMock()
        mock_resolve.return_value = mock_current_path
        mock_parent = MagicMock()
        mock_current_path.parent = mock_parent
        mock_templates_path = MagicMock()
        mock_parent.__truediv__.return_value = mock_templates_path
        mock_doc_instructions_path = MagicMock()
        mock_templates_path.__truediv__.return_value = mock_doc_instructions_path
        mock_file_path = Path("mocked_path")
        mock_doc_instructions_path.__truediv__.return_value = mock_file_path

        # Call the method
        result = self.prompt_builder._read_template("outros.txt", get_document_instructions=True)

        # Assertions
        mock_file.assert_called_once_with(mock_file_path, "r", encoding="utf-8")
        self.assertEqual(result, "Test document instructions")

    @patch("builtins.open", new_callable=mock_open)
    @patch("pathlib.Path.resolve")
    def test_read_template_file_not_found(self, mock_resolve, mock_file):
        """Test reading template from non-existent file."""
        # Setup
        mock_current_path = MagicMock()
        mock_resolve.return_value = mock_current_path
        mock_parent = MagicMock()
        mock_current_path.parent = mock_parent
        mock_templates_path = MagicMock()
        mock_parent.__truediv__.return_value = mock_templates_path
        mock_file_path = Path("mocked_path")
        mock_templates_path.__truediv__.return_value = mock_file_path
        mock_file.side_effect = FileNotFoundError("File not found")

        # Call the method and expect an exception
        with self.assertRaises(FileNotFoundError):
            self.prompt_builder._read_template("non_existent.txt")

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_success(self, mock_read_template):
        """Test creating a prompt with valid inputs."""
        # Setup
        mock_read_template.side_effect = ["System content with {{document_instructions}}", "Document instructions"]
        variables = {
            "title": "outros",
            "image_base64": "base64_encoded_image_data"
        }

        # Call the method
        result = self.prompt_builder.create_prompt(
            system_template="system.txt",
            variables=variables
        )

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        mock_read_template.assert_any_call("system.txt")
        mock_read_template.assert_any_call("outros.txt", True)
        self.assertEqual(len(result.messages), 2)  # System message and Human message with image

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_missing_variables(self, mock_read_template):
        """Test creating a prompt with missing variables."""
        # Setup
        mock_read_template.return_value = "System content"

        # Call the method and expect an exception
        with self.assertRaises(ValueError):
            self.prompt_builder.create_prompt(system_template="system.txt")

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_invalid_title(self, mock_read_template):
        """Test creating a prompt with invalid title."""
        # Setup
        mock_read_template.return_value = "System content"
        variables = {
            "title": "invalid_title",
            "image_base64": "base64_encoded_image_data"
        }

        # Call the method and expect an exception
        with self.assertRaises(ValueError):
            self.prompt_builder.create_prompt(
                system_template="system.txt",
                variables=variables
            )

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_empty_image(self, mock_read_template):
        """Test creating a prompt with empty image_base64."""
        # Setup
        mock_read_template.side_effect = ["System content", "Document instructions"]
        variables = {
            "title": "outros",
            "image_base64": ""
        }

        # Call the method and expect an exception
        with self.assertRaises(ValueError):
            self.prompt_builder.create_prompt(
                system_template="system.txt",
                variables=variables
            )

    def test_create_prompt_invalid_system_template(self):
        """Test creating a prompt with empty system template."""
        # Setup
        variables = {
            "title": "outros",
            "image_base64": "base64_encoded_image_data"
        }

        # Call the method and expect an exception
        with self.assertRaises(FileNotFoundError):
            self.prompt_builder.create_prompt(
                system_template="empty.txt",
                variables=variables
            )


if __name__ == "__main__":
    unittest.main()
