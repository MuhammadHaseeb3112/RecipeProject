# RecipeApp/templatetags/recipe_tags.py
import re
from django import template

register = template.Library()

@register.filter
def split_ingredients(value):
    """
    Splits a comma or newline-separated ingredients string into a list.
    """
    if not value:
        return []
    # Split by comma or newline, strip spaces
    items = [item.strip() for item in value.replace('\r', '').split('\n')]
    result = []
    for line in items:
        result.extend([i.strip() for i in line.split(',') if i.strip()])
    return result


@register.filter
def split_steps(value):
    """
    Splits instructions text into steps.
    - If "Step X" exists, split by that.
    - Else, split by paragraphs (newlines).
    Returns a list of steps.
    """
    if not value:
        return []

    # Check if "Step X" exists anywhere
    if re.search(r'Step\s*\d+', value, re.IGNORECASE):
        # Split by "Step X"
        pattern = re.compile(r'(Step\s*\d+[:.]?)', re.IGNORECASE)
        parts = pattern.split(value)
        
        steps = []
        current_step = ""
        for part in parts:
            if pattern.match(part):
                if current_step:
                    steps.append(current_step.strip())
                current_step = part
            else:
                current_step += part
        if current_step:
            steps.append(current_step.strip())
        return steps
    else:
        # No "Step X", split by newline paragraphs
        paragraphs = [p.strip() for p in value.replace('\r','').split('\n') if p.strip()]
        return paragraphs


@register.filter
def to(value, arg):
    """Usage: {% for i in 1|to:5 %} -> loops 1,2,3,4,5"""
    return range(value, int(arg)+1)
