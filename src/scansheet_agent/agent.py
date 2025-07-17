import json
import logging
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import SecretStr

from scansheet_agent.schemas import AIMessageModel

# Configure logger
logger = logging.getLogger(__name__)

class ScanSheetAgent:
    def __init__(self, api_key: str, model: str):
        logger.info("Initializing ScanSheetAgent")

        self.api_key = api_key
        self.model = model
        self.client = ChatOpenAI(model=self.model, api_key=SecretStr(self.api_key))
        logger.info("ScanSheetAgent initialized successfully")

    @staticmethod
    def validate_model_response(model_response: AIMessage):
        """Validate the model response."""
        logger.debug("Validating model response")
        try:
            validated_response = AIMessageModel.model_validate(json.loads(model_response.content)).model_dump_json()
            logger.debug("Model response validated successfully")
            return validated_response
        except Exception as e:
            logger.error(f"Error validating model response: {str(e)}")
            raise

    @staticmethod
    def invoke_model(chain: RunnableSerializable, inputs=None) -> Dict[str, str]:
        """Invoke the model with the given chain and inputs.

        Args:
            chain (RunnableSerializable): The chain to run
            inputs (Dict[str, str]): Input parameters for the chain

        Returns:
            Dict[str, str]: Model response
        """
        logger.info("Invoking model")
        logger.debug(f"Input parameters: {inputs}")

        if inputs is None:
            inputs = {}
            logger.debug("No inputs provided, using empty dict")

        try:
            response = chain.invoke(inputs)
            logger.info("Model invocation successful")
            logger.debug("Received response from model")
            return response
        except Exception as e:
            logger.error(f"Error invoking model: {str(e)}")
            raise

    def build_chain(self, prompt: ChatPromptTemplate):
        logger.debug("Building processing chain")
        chain = prompt | self.client | self.validate_model_response
        logger.debug("Chain built successfully")
        return chain

    def run(self, prompt: ChatPromptTemplate, inputs: Optional[Dict[str, str]] = None):
        """Run the agent with the given prompt and inputs.

        Args:
            prompt (ChatPromptTemplate): The prompt to use
            inputs (Optional[Dict[str, str]]): Input parameters for the chain

        Returns:
            AIMessageModel: Model response
        """
        logger.info("Starting agent run")
        logger.debug(f"Using inputs: {inputs}")

        try:
            chain = self.build_chain(prompt)
            model_response = self.invoke_model(chain, inputs)
            logger.info("Agent run completed successfully")
            return model_response
        except Exception as e:
            logger.error(f"Error during agent run: {str(e)}")
            raise
