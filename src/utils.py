import os
from src.config import TEMPLATES_DIR

def load_template(filename: str) -> str:
    path = os.path.join(TEMPLATES_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def render_template(template_name, **context):
    template = load_template(template_name)
    for key, value in context.items():
        placeholder = "{{ " + key + " }}"
        template = template.replace(placeholder, str(value))
    return template
