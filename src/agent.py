import json
from typing import Dict, Any
from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

from src.model import AIMessageModel


class ScanSheetAgent:
    def __init__(self, api_key: str, model: str):

        self.api_key = api_key
        self.model = model
        self.client = ChatOpenAI(model=self.model, api_key=self.api_key)

    def _validate_model_response(self, model_response: AIMessage):
        """Validate the model response."""
        try:
            return AIMessageModel.model_validate(model_response.content)
        except:
            raise

    @staticmethod
    def _invoke_model(chain: LLMChain, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the model with the given chain and inputs.

        Args:
            chain (LLMChain): The chain to run
            inputs (Dict[str, Any]): Input parameters for the chain

        Returns:
            Dict[str, Any]: Model response
        """
        return chain.invoke(inputs)

    def _build_chain(self, prompt: ChatPromptTemplate):
        return prompt | self.client | self._validate_model_response

    def run(self, prompt: ChatPromptTemplate, inputs: Dict[str, Any]) -> str:
        """Run the agent with the given prompt and inputs.

        Args:
            prompt (ChatPromptTemplate): The prompt to use
            inputs (Dict[str, Any]): Input parameters for the chain

        Returns:
            AIMessageModel: Model response
        """
        chain = self._build_chain(prompt)
        model_response = self._invoke_model(chain, inputs)
        return json.dumps(model_response)
