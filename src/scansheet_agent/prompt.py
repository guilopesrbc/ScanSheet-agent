from pathlib import Path
from typing import Dict
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from scansheet_agent.schemas import DocumentTypeEnum


class PromptBuilder:
    def __init__(self, templates_dir: str = "templates"):
        """Initialize the prompt builder.

        Args:
            templates_dir (str): Directory containing template files
        """
        self.templates_dir = Path(templates_dir)

    def _read_template(self, file_name: str, get_document_instructions: bool = False) -> str:
        """Read template content from file.

        Args:
            file_name (str): Template file name

        Returns:
            str: Template content
        """
        current_path = Path(__file__).resolve().parent
        file_path = current_path / self.templates_dir / file_name
        
        if get_document_instructions:
            file_path = current_path / self.templates_dir / "document_instructions" / file_name
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {file_path}")

    def create_prompt(
        self,
        system_template: str = "SYSTEM.txt",
        variables: Dict[str, str] = None,
    ) -> ChatPromptTemplate:
        """Create a chat prompt from template files.

        Args:
            system_template (str): System template file name
            variables (Dict[str, Any]): Template variables, must include 'image_base64' and 'title'

        Returns:
            ChatPromptTemplate: Configured prompt template
        """
        messages = []
        system_content = self._read_template(system_template) if system_template else ""
        if system_content:
            if variables:
                try:
                    title = variables.get("title", "outros")
                    title_valid_values = [e.value for e in DocumentTypeEnum]
                    if title not in title_valid_values:
                        raise ValueError(
                            f"Invalid title: '{title}'. "
                            f"It must be a valid value from DocumentTypeEnum: "
                            f"{list(DocumentTypeEnum.__members__.values())}"
                        )

                    document_instructions = self._read_template(f"{title}.txt", True)
                    system_content = system_content.replace("{{document_instructions}}", document_instructions)

                    image_base64 = variables.get("image_base64")
                    if image_base64 == '':
                        raise ValueError("Image URL cannot be an empty string.")

                    human_content = [
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                except Exception as e:
                    raise Exception(f"Error processing variables: {e}")
            else:
                raise ValueError("Image URL is required in variables.")
            
            messages.append(SystemMessage(content=system_content))
            messages.append(HumanMessage(content=human_content))
            
        else:
            raise ValueError("System template is required.")

        return ChatPromptTemplate.from_messages(messages)