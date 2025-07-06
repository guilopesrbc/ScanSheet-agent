import unittest
from unittest.mock import MagicMock, patch
import json
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

from src.agent import ScanSheetAgent
from src.model import AIMessageModel


class TestScanSheetAgent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key"
        self.model = "test_model"
        self.agent = ScanSheetAgent(api_key=self.api_key, model=self.model)

    def test_init(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.api_key, self.api_key)
        self.assertEqual(self.agent.model, self.model)
        self.assertIsNotNone(self.agent.client)

    @patch('src.agent.AIMessageModel.model_validate')
    def test_validate_model_response_success(self, mock_model_validate):
        """Test successful validation of model response."""
        # Create a mock AIMessage with valid JSON content
        valid_json = {
            "title": "Test Title",
            "content": {"field1": "value1", "field2": "value2"}
        }
        mock_response = AIMessage(content=json.dumps(valid_json))
        
        # Setup the mock to return a model instance
        mock_model = MagicMock()
        mock_model.model_dump_json.return_value = json.dumps(valid_json)
        mock_model_validate.return_value = mock_model
        
        # Call the method
        result = self.agent._validate_model_response(mock_response)
        
        # Assertions
        mock_model_validate.assert_called_once_with(valid_json)
        self.assertEqual(result, json.dumps(valid_json))

    @patch('src.agent.AIMessageModel.model_validate')
    def test_validate_model_response_invalid_json(self, mock_model_validate):
        """Test validation with invalid JSON."""
        # Create a mock AIMessage with invalid JSON content
        mock_response = AIMessage(content="not a json")
        
        # Call the method and expect an exception
        with self.assertRaises(Exception):
            self.agent._validate_model_response(mock_response)

    @patch('src.agent.AIMessageModel.model_validate')
    def test_validate_model_response_validation_error(self, mock_model_validate):
        """Test validation with JSON that doesn't match the model."""
        # Create a mock AIMessage with JSON that doesn't match the model
        invalid_model_json = {"not_title": "value", "not_content": {}}
        mock_response = AIMessage(content=json.dumps(invalid_model_json))
        
        # Setup the mock to raise an exception
        mock_model_validate.side_effect = ValueError("Validation error")
        
        # Call the method and expect an exception
        with self.assertRaises(ValueError):
            self.agent._validate_model_response(mock_response)

    def test_invoke_model(self):
        """Test invoking the model."""
        # Create mock chain and inputs
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "mock_response"
        inputs = {"key": "value"}
        
        # Call the method
        result = self.agent._invoke_model(mock_chain, inputs)
        
        # Assertions
        mock_chain.invoke.assert_called_once_with(inputs)
        self.assertEqual(result, "mock_response")

    @patch('src.agent.ScanSheetAgent._validate_model_response')
    def test_build_chain(self, mock_validate):
        """Test building a chain."""
        # Setup
        mock_prompt = MagicMock(spec=ChatPromptTemplate)
        mock_validate.return_value = "validated_response"
        
        # Call the method
        chain = self.agent._build_chain(mock_prompt)
        
        # We can't easily test the chain itself, but we can ensure it was created
        self.assertIsNotNone(chain)

    @patch('src.agent.ScanSheetAgent._build_chain')
    @patch('src.agent.ScanSheetAgent._invoke_model')
    def test_run(self, mock_invoke, mock_build_chain):
        """Test running the agent."""
        # Setup
        mock_prompt = MagicMock(spec=ChatPromptTemplate)
        mock_chain = MagicMock()
        mock_build_chain.return_value = mock_chain
        mock_invoke.return_value = "model_response"
        inputs = {"key": "value"}
        
        # Call the method
        result = self.agent.run(mock_prompt, inputs)
        
        # Assertions
        mock_build_chain.assert_called_once_with(mock_prompt)
        mock_invoke.assert_called_once_with(mock_chain, inputs)
        self.assertEqual(result, "model_response")

    @patch('src.agent.ScanSheetAgent._build_chain')
    @patch('src.agent.ScanSheetAgent._invoke_model')
    def test_run_with_error(self, mock_invoke, mock_build_chain):
        """Test running the agent with an error."""
        # Setup
        mock_prompt = MagicMock(spec=ChatPromptTemplate)
        mock_chain = MagicMock()
        mock_build_chain.return_value = mock_chain
        mock_invoke.side_effect = Exception("Test error")
        inputs = {"key": "value"}
        
        # Call the method and expect an exception
        with self.assertRaises(Exception):
            self.agent.run(mock_prompt, inputs)
        
        # Assertions
        mock_build_chain.assert_called_once_with(mock_prompt)
        mock_invoke.assert_called_once_with(mock_chain, inputs)


if __name__ == "__main__":
    unittest.main()