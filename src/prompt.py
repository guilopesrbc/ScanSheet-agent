from pathlib import Path
from typing import Dict, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import HumanMessagePromptTemplate

from src.utils import encode_image


class PromptBuilder:
    def __init__(self, templates_dir: str = "templates"):
        """Initialize the prompt builder.

        Args:
            templates_dir (str): Directory containing template files
        """
        self.templates_dir = Path(templates_dir)

    def _read_template(self, file_name: str) -> str:
        """Read template content from file.

        Args:
            file_name (str): Template file name

        Returns:
            str: Template content
        """
        current_path = Path(__file__).resolve().parent
        file_path = current_path / self.templates_dir / file_name
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {file_path}")

    def create_prompt(
        self,
        system_template: str = None,
        human_template: str = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> ChatPromptTemplate:
        """Create a chat prompt from template files.

        Args:
            system_template (str): System template file name
            human_template (str): Human template file name
            variables (Dict[str, Any], optional): Template variables

        Returns:
            ChatPromptTemplate: Configured prompt template
        """
        messages = []
        system_content = self._read_template(system_template) if system_template else ""
        human_content = self._read_template(human_template) if human_template else ""

        if system_content:
            messages.append(SystemMessage(content=system_content))
        if human_content:
            messages.append(HumanMessagePromptTemplate.from_template(human_content))

        if variables and "image_url" in variables:
            messages.append(HumanMessage(content=[
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(variables["image_url"])}"}}
            ]))

        return ChatPromptTemplate.from_messages(messages)