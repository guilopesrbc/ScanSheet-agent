import os
from .document_instructions import *

# Get the directory of this file
_current_dir = os.path.dirname(os.path.abspath(__file__))

# Path to SYSTEM.txt
SYSTEM_TEMPLATE_PATH = os.path.join(_current_dir, 'SYSTEM.txt')

# Export the path
__all__ = ['document_templates', 'SYSTEM_TEMPLATE_PATH']
