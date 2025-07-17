import json
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import SecretStr

from scansheet_agent.schemas import AIMessageModel

class ScanSheetAgent:
    def __init__(self, api_key: str, model: str):

        self.api_key = api_key
        self.model = model
        self.client = ChatOpenAI(model=self.model, api_key=SecretStr(self.api_key))

    def _validate_model_response(self, model_response: AIMessage):
        """Validate the model response."""
        try:
            return AIMessageModel.model_validate(json.loads(model_response.content)).model_dump_json()
        except:
            raise

    @staticmethod
    def _invoke_model(chain: RunnableSerializable, inputs=None) -> Dict[str, str]:
        """Invoke the model with the given chain and inputs.

        Args:
            chain (RunnableSerializable): The chain to run
            inputs (Dict[str, str]): Input parameters for the chain

        Returns:
            Dict[str, str]: Model response
        """
        if inputs is None:
            inputs = {}

        return chain.invoke(inputs)

    def _build_chain(self, prompt: ChatPromptTemplate):
        return prompt | self.client | self._validate_model_response

    def run(self, prompt: ChatPromptTemplate, inputs: Optional[Dict[str, str]] = None):
        """Run the agent with the given prompt and inputs.

        Args:
            prompt (ChatPromptTemplate): The prompt to use
            inputs (Optional[Dict[str, str]]): Input parameters for the chain

        Returns:
            AIMessageModel: Model response
        """
        chain = self._build_chain(prompt)
        model_response = self._invoke_model(chain, inputs)
        return model_response
