from pathlib import Path
import logging
from typing import Dict
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from scansheet_agent.schemas import DocumentTypeEnum

# Configure logger
logger = logging.getLogger(__name__)


class PromptBuilder:
    def __init__(self, templates_dir: str = "templates"):
        """Initialize the prompt builder.

        Args:
            templates_dir (str): Directory containing template files
        """
        logger.info("Initializing PromptBuilder")
        logger.debug(f"Using templates directory: {templates_dir}")
        self.templates_dir = Path(templates_dir)

    def _read_template(self, file_name: str, get_document_instructions: bool = False) -> str:
        """Read template content from file.

        Args:
            file_name (str): Template file name

        Returns:
            str: Template content
        """
        logger.debug(f"Reading template: {file_name}")
        logger.debug(f"Get document instructions: {get_document_instructions}")

        current_path = Path(__file__).resolve().parent
        file_path = current_path / self.templates_dir / file_name

        if get_document_instructions:
            file_path = current_path / self.templates_dir / "document_instructions" / file_name
            logger.debug(f"Using document instructions path: {file_path}")
        else:
            logger.debug(f"Using template path: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                logger.debug(f"Template '{file_name}' read successfully")
                return content
        except FileNotFoundError:
            error_msg = f"Template file not found: {file_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

    def create_prompt(
        self,
        system_template: str = "SYSTEM.txt",
        variables: Dict[str, str] = None,
    ) -> ChatPromptTemplate:
        """Create a chat prompt from template files.

        Args:
            system_template (str): System template file name
            variables (Dict[str, Any]): Template variables, must include 'markdown_content' and 'title'

        Returns:
            ChatPromptTemplate: Configured prompt template
        """
        logger.info("Creating prompt")
        logger.debug(f"Using system template: {system_template}")
        logger.debug(f"Variables provided: {True if variables else False}")

        messages = []
        try:
            system_content = self._read_template(system_template) if system_template else ""
            if system_content:
                if variables:
                    title = variables.get("title", "outros")
                    logger.debug(f"Document type: {title}")

                    title_valid_values = [e.value for e in DocumentTypeEnum]
                    if title not in title_valid_values:
                        error_msg = (
                            f"Invalid title: '{title}'. "
                            f"It must be a valid value from DocumentTypeEnum: "
                            f"{list(DocumentTypeEnum.__members__.values())}"
                        )
                        logger.error(error_msg)
                        raise ValueError(error_msg)

                    logger.debug(f"Reading document instructions for: {title}")
                    document_instructions = self._read_template(f"{title}.txt", True)

                    system_content = system_content.replace("{{title_instructions}}", title)
                    system_content = system_content.replace("{{document_instructions}}", document_instructions)

                    logger.debug("Document instructions added to system content")

                    image_base64 = variables.get("image_base64")
                    if not image_base64 or image_base64 == '':
                        error_msg = "image_base64 not exists or is an empty string."
                        raise ValueError(error_msg)

                    logger.debug("Image base64 validated")
                    image_content = [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]

                    markdown_content = variables.get("markdown_content", None)
                    if not markdown_content or markdown_content == '':
                        error_msg = "markdown_content not exists or is an empty string."
                        logger.error(error_msg)
                        raise ValueError(error_msg)


                    logger.debug("Human content with image created")
                else:
                    error_msg = "Variables is empty."
                    logger.error(error_msg)
                    raise ValueError(error_msg)

                messages.append(SystemMessage(content=system_content))
                messages.append(HumanMessage(content=markdown_content))
                messages.append(HumanMessage(content=image_content))
                logger.debug("Messages created successfully")

            else:
                error_msg = "System template is required."
                logger.error(error_msg)
                raise ValueError(error_msg)

            prompt = ChatPromptTemplate.from_messages(messages)
            logger.info("Prompt created successfully")
            return prompt

        except Exception as e:
            logger.error(f"Error creating prompt: {str(e)}")
            raise
