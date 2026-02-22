import xml.etree.ElementTree as ET
import sys
import base64
import zlib
from urllib.parse import unquote

def decode_diagram_data(data):
    try:
        # Check if it's base64/compressed
        decoded = base64.b64decode(data)
        return zlib.decompress(decoded, -15).decode('utf-8')
    except Exception as e:
        # Maybe it's already XML or just plain text?
        return data

def parse_drawio(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    diagrams = []
    for diagram in root.findall('diagram'):
        name = diagram.get('name', 'Untitled')
        diag_id = diagram.get('id')
        
        # Check content
        if diagram.find('mxGraphModel') is not None:
            # Uncompressed
            mx_graph = diagram.find('mxGraphModel')
            root_cell = mx_graph.find('root')
        else:
            # Compressed
            text_data = diagram.text
            if text_data:
                xml_content = decode_diagram_data(text_data)
                # Parse the inner XML
                try:
                    inner_tree = ET.fromstring(unquote(xml_content))
                    root_cell = inner_tree.find('root')
                except Exception as e:
                    print(f"Error parsing inner XML for {name}: {e}")
                    continue
            else:
                continue

        # Extract text from cells
        texts = []
        if root_cell is not None:
            for cell in root_cell.findall('mxCell'):
                val = cell.get('value')
                if val:
                    # Clean up HTML if present
                    # accurate way is hard without bs4, but simple strip is ok
                    texts.append(val)
        
        diagrams.append({
            'name': name,
            'id': diag_id,
            'texts': texts
        })

    return diagrams

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_drawio.py <file>")
        sys.exit(1)
        
    results = parse_drawio(sys.argv[1])
    for d in results:
        print(f"## Diagram: {d['name']} (ID: {d['id']})")
        for t in d['texts']:
            print(f"- {t}")
        print("\n" + "="*40 + "\n")
