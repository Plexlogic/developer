# Helper script to generate custom admonition stylesheets
# You can of course use SCSS just like mkdocs-material as well :)
# https://github.com/squidfunk/mkdocs-material/blob/master/src/assets/stylesheets/main/extensions/markdown/_admonition.scss

colors = [
    {
        'primary_color': 'var(--plexus-brand-400)',
        'secondary_color': 'var(--plexus-brand-900)',
        'types': ['note', 'abstract', 'summary', 'tldr', 'info', 'todo']
    },
    {
        'primary_color': 'var(--plexus-brand-200)',
        'secondary_color': 'var(--plexus-brand-800)',
        'types': ['tip', 'hint', 'important', 'question', 'help', 'faq', 'example']
    },
    {
        'primary_color': 'var(--plexus-positive-400)',
        'secondary_color': 'var(--plexus-positive-900)',
        'types': ['success', 'check', 'done']
    },
    {
        'primary_color': 'var(--plexus-caution-400)',
        'secondary_color': 'var(--plexus-caution-900)',
        'types': ['warning', 'caution', 'attention']
    },
    {
        'primary_color': 'var(--plexus-urgent-400)',
        'secondary_color': 'var(--plexus-urgent-900)',
        'types': ['failure', 'fail', 'missing', 'danger', 'error', 'bug']
    },
    {
        'primary_color': 'var(--plexus-neutral-500)',
        'secondary_color': 'var(--plexus-neutral-900)',
        'types': ['quote', 'cite']
    }
]

css = f'''/*
Generated by scripts/admonition.py
Please edit that script to generate this, instead of editing this directly :)
*/

/* Default */
.md-typeset .admonition,
.md-typeset details {{
    border-color: var(--plexus-brand-400);
}}
.md-typeset .admonition-title,
.md-typeset summary {{
    background-color: var(--plexus-brand-900);
    border-color: var(--plexus-brand-400);
}}
.md-typeset .admonition-title::before,
.md-typeset summary::before {{
    background-color: var(--plexus-brand-400);
}}'''

for color in colors:
    primary_color, secondary_color, types = color['primary_color'], color['secondary_color'], color['types']
    for type in types:
        css += f'''

/* Type: {type} */
.md-typeset .admonition.{type},
.md-typeset details.{type} {{
    border-color: {primary_color};
}}
.md-typeset .{type} > .admonition-title,
.md-typeset .{type} > summary {{
    background-color: {secondary_color};
    border-color: {primary_color};
}}
.md-typeset .{type} > .admonition-title::before,
.md-typeset .{type} > summary::before {{
    background-color: {primary_color};
}}'''

print(css)