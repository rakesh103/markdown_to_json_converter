import os
import json
import markdown

"""
    Convert a Markdown file to a structured JSON format.

    This function reads a Markdown file and converts its content into a JSON format.
    The structure of the JSON format includes sections, subsections, lists (bulleted and numbered), 
    and tables found within the Markdown file.

    Parameters:
    md_file (str): Path to the input Markdown file.
    json_file (str): Path to the output JSON file.
"""
def convert_md_to_json(md_file, json_file):
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to JSON format
    json_content = {
        'template': 'Example Markdown Template',
        'sections': []
    }

    lines = md_content.splitlines()
    current_section = None
    current_subsection = None
    current_list = None
    current_table = None

    for line in lines:
        line = line.strip()

        if line.startswith('## '):
            current_section = {
                'title': line[3:].strip(),
                'content': ''
            }
            json_content['sections'].append(current_section)
            current_subsection = None
            current_list = None
            current_table = None
        elif line.startswith('### '):
            current_subsection = {
                'title': line[4:].strip(),
                'content': ''
            }
            if current_section:
                current_section.setdefault('subsections', []).append(current_subsection)
            current_list = None
            current_table = None
        elif line.startswith('- '):
            if current_subsection:
                current_list = {
                    'type': 'bulleted',
                    'items': []
                }
                current_subsection.setdefault('lists', []).append(current_list)
            elif current_section:
                current_list = {
                    'type': 'bulleted',
                    'items': []
                }
                current_section.setdefault('lists', []).append(current_list)
        elif line.startswith('1. '):
            if current_subsection:
                current_list = {
                    'type': 'numbered',
                    'items': []
                }
                current_subsection.setdefault('lists', []).append(current_list)
            elif current_section:
                current_list = {
                    'type': 'numbered',
                    'items': []
                }
                current_section.setdefault('lists', []).append(current_list)
        elif line.startswith('|'):
            if line.startswith('| Column '):
                current_table = {
                    'columns': [col.strip() for col in line[1:-1].split('|') if col.strip()]
                }
                if current_subsection:
                    current_subsection.setdefault('table', []).append(current_table)
                elif current_section:
                    current_section.setdefault('table', []).append(current_table)
            elif current_table:
                cells = [cell.strip() for cell in line[1:-1].split('|') if cell.strip()]
                if len(cells) == len(current_table['columns']):
                    current_table.setdefault('rows', []).append(cells)

        # Collecting paragraph content under current section/subsection
        elif current_section:
            if current_subsection:
                current_subsection['content'] += line + '\n'
            else:
                current_section['content'] += line + '\n'

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_content, f, indent=4)


def main():
    templates_dir = '../templates'  # Use relative path

    output_dir = '../output'  # Use relative path

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(templates_dir):
        if filename.endswith('.md'):
            md_file = os.path.join(templates_dir, filename)
            json_file = os.path.join(output_dir, os.path.splitext(filename)[0] + '.json')
            convert_md_to_json(md_file, json_file)
            print(f'Converted {filename} to JSON.')


if __name__ == '__main__':
    main()
