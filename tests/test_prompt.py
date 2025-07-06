import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from src.prompt import PromptBuilder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage


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
    def test_create_prompt_with_system_and_human(self, mock_read_template):
        """Test creating a prompt with system and human templates."""
        # Setup
        mock_read_template.side_effect = ["System content", "Human content {variable}"]
        variables = {"variable": "test_value"}

        # Call the method
        result = self.prompt_builder.create_prompt(
            system_template="system.txt",
            human_template="human.txt",
            variables=variables
        )

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        mock_read_template.assert_any_call("system.txt")
        mock_read_template.assert_any_call("human.txt")

        self.assertEqual(len(result.messages), 2)

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_with_system_only(self, mock_read_template):
        """Test creating a prompt with only system template."""
        # Setup
        mock_read_template.return_value = "System content"

        # Call the method
        result = self.prompt_builder.create_prompt(system_template="system.txt")

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        mock_read_template.assert_called_once_with("system.txt")
        self.assertEqual(len(result.messages), 1)

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_with_human_only(self, mock_read_template):
        """Test creating a prompt with only human template."""
        # Setup
        mock_read_template.return_value = "Human content {variable}"
        variables = {"variable": "test_value"}

        # Call the method
        result = self.prompt_builder.create_prompt(
            human_template="human.txt",
            variables=variables
        )

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        mock_read_template.assert_called_once_with("human.txt")
        self.assertEqual(len(result.messages), 1)

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_with_image_url(self, mock_read_template):
        """Test creating a prompt with an image URL."""
        # Setup
        mock_read_template.side_effect = ["System content", "Human content"]
        variables = {"image_url": "base64_encoded_image_data"}

        # Call the method
        result = self.prompt_builder.create_prompt(
            system_template="system.txt",
            human_template="human.txt",
            variables=variables
        )

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        # With image_url, we should have 3 messages (system, human template, and image)
        self.assertEqual(len(result.messages), 3)

    @patch.object(PromptBuilder, "_read_template")
    def test_create_prompt_with_empty_templates(self, mock_read_template):
        """Test creating a prompt with empty templates."""
        # Setup
        mock_read_template.return_value = ""

        # Call the method
        result = self.prompt_builder.create_prompt(
            system_template="empty.txt",
            human_template="empty.txt"
        )

        # Assertions
        self.assertIsInstance(result, ChatPromptTemplate)
        # Empty templates should not create messages
        self.assertEqual(len(result.messages), 0)


if __name__ == "__main__":
    unittest.main()
