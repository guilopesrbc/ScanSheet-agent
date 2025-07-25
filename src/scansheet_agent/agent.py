import json
import logging
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from mistralai import Mistral, OCRResponse
from pydantic import SecretStr

from scansheet_agent import PromptBuilder
from scansheet_agent.schemas import AIMessageModel

# Configure logger
logger = logging.getLogger(__name__)

class ScanSheetAgent:
    def __init__(self, chat_gpt_api_key: str, chat_gpt_model: str, mistral_api_key: str):
        logger.info("Initializing ScanSheetAgent")

        self.chat_gpt_api_key = chat_gpt_api_key
        self.chat_gpt_model = chat_gpt_model

        self.chatgpt = ChatOpenAI(model=self.chat_gpt_model, api_key=SecretStr(self.chat_gpt_api_key))
        self.mistral_ai = Mistral(api_key=mistral_api_key)

        logger.info("ScanSheetAgent initialized successfully")

    @staticmethod
    def validate_model_response(model_response: AIMessage):
        """Validate the model response.

        Args:
            model_response (AIMessage): The response from the model to be validated
        """
        logger.debug("Validating model response")
        try:
            response_json = json.loads(model_response.content)
            validated_response = AIMessageModel.model_validate(response_json).model_dump_json()
            logger.debug("Model response validated successfully")
            return validated_response
        except Exception as e:
            logger.error(f"Error validating model response: {str(e)}")
            raise e

    def _extract_ocr(self, pdf_base64: str) -> OCRResponse:
        """
        Extract the OCR (Optical Character Recognition) data from a base64-encoded PDF document.

        Args:
            pdf_base64 (str): The base64-encoded content of the PDF document to be processed.

        Returns:
            OCRResponse: An object containing the extracted OCR data, potentially including images 
            and text content obtained from the PDF document.

        Raises:
            Exception: If an error occurs during the OCR extraction process.
        """

        try:
            ocr_response = self.mistral_ai.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{pdf_base64}"
                },
                include_image_base64=True
            )
            return ocr_response
        except Exception as e:
            logger.error("Error extracting OCR")
            raise e

    @staticmethod
    def _get_ocr_markdown(ocr_response: OCRResponse) -> str:
        """
        Extract markdown content from OCRResponse for all pages.

        Args:
            ocr_response (OCRResponse): The OCR response from Mistral AI

        Returns:
            str: Combined markdown content from all pages
        """
        markdown_content = []

        # Iterate through all pages in the response
        for page in ocr_response.pages:
            # Get markdown content for the current page
            if page.markdown:
                markdown_content.append(page.markdown)

        # Join all markdown content with double newlines between pages
        return "\n\n".join(markdown_content)

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
            raise e

    def build_chain(self, prompt: ChatPromptTemplate):
        """Build a processing chain with the given prompt.

        Args:
            prompt (ChatPromptTemplate): The prompt template to use in the chain

        Returns:
            RunnableSerializable: The constructed processing chain
        """
        logger.debug("Building processing chain")
        chain = prompt | self.chatgpt | self.validate_model_response
        logger.debug("Chain built successfully")
        return chain

    def run(self, variables: Dict[str,str], inputs: Optional[Dict[str, str]] = None):
        """Run the agent with the given variables and inputs.

        Args:
            variables (Dict[str, str]): Variables used to create the prompt, must include 'pdf_base64'
            inputs (Optional[Dict[str, str]]): Input parameters for the chain

        Returns:
            AIMessageModel: Model response
        """
        logger.info("Starting agent run")
        logger.debug(f"Using inputs: {inputs}")

        try:
            ocr_response = self._extract_ocr(variables.get("pdf_base64"))
            markdown_content = self._get_ocr_markdown(ocr_response)
            variables['markdown_content'] = markdown_content
            prompt = PromptBuilder().create_prompt(variables=variables)
            chain = self.build_chain(prompt)
            model_response = self.invoke_model(chain, inputs)
            logger.info("Agent run completed successfully")
            return model_response
        except Exception as e:
            logger.error(f"Error during agent run: {str(e)}")
            raise
