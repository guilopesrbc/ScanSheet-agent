# ScanSheet Agent Library 
This library provides a simple interface to interact with the ScanSheet Agent, allowing you to processing form images into formatted JSON with values and columns using OpenAI's models.

## Installation
To install the ScanSheet Agent Library, you need to install the library using pip:
```bash
pip install git+https://github.com/guilopesrbc/ScanSheet-agent.git@<version>
```

If you want to install it from the local source code, you can clone the repository and run the following command in the root directory of the project:
```bash
pip install .
```

If you want to install the development dependencies as well, use:
```bash
pip install .[dev]
```

## Usage

To use the ScanSheet Agent Library, you can import it in your Python script.
```python
from scansheet_agent.agent import ScanSheetAgent
```

### Configuration
#### ScanSheet Agent
After importing, you can create an instance of the `ScanSheetAgent` class and use it to create ScanSheet Agent.

You need to provide your API key and the model you want to use (e.g., "gpt-4").

It's important that the model you choose is compatible with Image inputs, such as "gpt-4".

Check the OpenAI documentation for more details on model capabilities:
https://platform.openai.com/docs/guides/images-vision?api-mode=responses

```python
agent = ScanSheetAgent(chat_gpt_model="your_chat_gpt_api_model", chat_gpt_api_key="your_chat_gpt_api_key", mistral_api_key="your_mistral_api_key")
``` 

#### Variables and Inputs
You must to provide the image and pdf as a bytestring in variables and a valid ```scansheet_agent.schemas.DocumentTypeEnum``` when creating prompt.
You can also provide additional inputs that will be used in the prompt, check project prompts to use availables input.
```python
variables = {
    "image_base64": "Your image as a base64 encoded string",
    "pdf_base64": "Your pdf as a base64 encoded string",
    "title": "Your document type title",
}

inputs = {
    'some_input': "Some input value",
}
```

#### Invoke the Agent
Finally, you can invoke the agent using the `run` method, passing in the prompt and any additional inputs.
```python
response = agent.run(variables=variables, inputs=inputs) 
# inputs is optional, you can pass it if you want to use additional inputs in the prompt
# check project prompts to use availables input.
```

## Tests

The ScanSheet Agent Library includes a comprehensive test suite to ensure its functionality. The tests are located in the `tests` directory.

### Running Tests

You can run all tests using the provided script:

```bash
python tests/run_tests.py
```

Or run individual test files:

```bash
python -m unittest tests/test_agent.py
python -m unittest tests/test_prompt.py
python -m unittest tests/test_model.py
```

### Test Coverage

The tests cover all major components of the library:
- ScanSheetAgent: Tests for initialization, model response validation, and execution
- PromptBuilder: Tests for template reading and prompt creation
- AIMessageModel: Tests for model validation and serialization

## Data Version Control (DVC)

This project uses DVC for managing large files and datasets. Follow these steps to set up and use DVC:

### Setup DVC

1. Initialize DVC in your local repository:
```bash
dvc init
```

2. Add the Google Drive remote storage:
```bash
dvc remote add --default myremote gdrive://FOLDER_ID
```

3. Configure the remote to acknowledge abuse warnings:
```bash
dvc remote modify myremote gdrive_acknowledge_abuse true
```

4. Configure your Google Drive credentials (you'll need to obtain your own credentials):
```bash
dvc remote modify myremote gdrive_client_id 'your-client-id'
dvc remote modify myremote gdrive_client_secret 'your-client-secret'
```

### Using DVC

1. Add files to DVC:
```bash
dvc add data/
```

2. Push files to the remote storage:
```bash
dvc push
```

3. Pull files from the remote storage:
```bash
dvc pull
```

For more information on using DVC, refer to the [official DVC documentation](https://dvc.org/doc).
