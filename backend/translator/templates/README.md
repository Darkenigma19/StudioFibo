# Jinja2 Templates for JSON Generation

This directory contains Jinja2 templates for generating FIBO JSON from structured data.

## Usage

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('product_template.json.j2')

output = template.render(
    description="Coffee grinder product shot",
    focal_length=50,
    seed=42
)
```

## Available Templates

- `product_template.json.j2` - E-commerce product photography
- `portrait_template.json.j2` - Portrait/headshot rendering
- `environment_template.json.j2` - Interior/exterior scenes

## Future Enhancement

Templates can be expanded to support:

- Brand-specific presets
- Industry templates (fashion, food, automotive)
- Custom lighting rigs
- Multi-shot compositions
