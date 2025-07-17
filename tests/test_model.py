import unittest
import json
from pydantic import ValidationError

from scansheet_agent import AIMessageModel
from scansheet_agent.schemas import DocumentTypeEnum


class TestAIMessageModel(unittest.TestCase):
    def test_valid_model(self):
        """Test creating a valid AIMessageModel."""
        # Create a valid model
        data = {
            "title": "outros",
            "content": {"field1": "value1", "field2": "value2"}
        }

        # Create the model
        model = AIMessageModel.model_validate(data)

        # Assertions
        self.assertEqual(model.title, DocumentTypeEnum.OUTROS)
        self.assertEqual(model.content, {"field1": "value1", "field2": "value2"})

    def test_missing_title(self):
        """Test creating a model with missing title."""
        # Create data with missing title
        data = {
            "content": {"field1": "value1", "field2": "value2"}
        }

        # Attempt to create the model and expect an exception
        with self.assertRaises(ValidationError):
            AIMessageModel.model_validate(data)

    def test_missing_content(self):
        """Test creating a model with missing content."""
        # Create data with missing content
        data = {
            "title": DocumentTypeEnum.OUTROS
        }

        # Attempt to create the model and expect an exception
        with self.assertRaises(ValidationError):
            AIMessageModel.model_validate(data)

    def test_invalid_title_type(self):
        """Test creating a model with invalid title type."""
        # Create data with invalid title type
        data = {
            "title": 123,  # Should be a string
            "content": {"field1": "value1", "field2": "value2"}
        }

        # Attempt to create the model and expect an exception
        with self.assertRaises(ValidationError):
            AIMessageModel.model_validate(data)

    def test_invalid_content_type(self):
        """Test creating a model with invalid content type."""
        # Create data with invalid content type
        data = {
            "title": DocumentTypeEnum.OUTROS,
            "content": "not a dict"  # Should be a dict
        }

        # Attempt to create the model and expect an exception
        with self.assertRaises(ValidationError):
            AIMessageModel.model_validate(data)

    def test_model_dump_json(self):
        """Test serializing the model to JSON."""
        # Create a valid model
        data = {
            "title": DocumentTypeEnum.OUTROS,
            "content": {"field1": "value1", "field2": "value2"}
        }
        model = AIMessageModel.model_validate(data)

        # Serialize to JSON
        json_str = model.model_dump_json()

        # Parse the JSON string back to a dict
        parsed_data = json.loads(json_str)

        # Assertions
        self.assertEqual(parsed_data["title"], "outros")  # Enum serializes to its value
        self.assertEqual(parsed_data["content"], {"field1": "value1", "field2": "value2"})

    def test_complex_content(self):
        """Test creating a model with complex content."""
        # Create data with complex content
        data = {
            "title": DocumentTypeEnum.OUTROS,
            "content": {
                "field1": "value1",
                "nested": {
                    "subfield1": "subvalue1",
                    "subfield2": 123
                },
                "array": [1, 2, 3],
                "boolean": True,
                "null": None
            }
        }

        # Create the model
        model = AIMessageModel.model_validate(data)

        # Assertions
        self.assertEqual(model.title, DocumentTypeEnum.OUTROS)
        self.assertEqual(model.content["field1"], "value1")
        self.assertEqual(model.content["nested"]["subfield1"], "subvalue1")
        self.assertEqual(model.content["nested"]["subfield2"], 123)
        self.assertEqual(model.content["array"], [1, 2, 3])
        self.assertTrue(model.content["boolean"])
        self.assertIsNone(model.content["null"])


if __name__ == "__main__":
    unittest.main()
