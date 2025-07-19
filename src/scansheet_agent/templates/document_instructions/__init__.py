import os

# Get the directory of this file
_current_dir = os.path.dirname(os.path.abspath(__file__))

# Dictionary to store template names and their file paths
document_templates = {}

# Add each template file to the dictionary
for filename in os.listdir(_current_dir):
    if filename.endswith('.txt'):
        template_name = os.path.splitext(filename)[0]
        document_templates[template_name] = os.path.join(_current_dir, filename)

# Export the dictionary
__all__ = ['document_templates']
