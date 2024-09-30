import pdfplumber
import os
import json

def chunk_text(text, chunk_size=1000):
    """Splits text into paragraphs and then groups into chunks of specified size."""
    paragraphs = [para.strip() for para in text.split('\n') if para.strip()]  # Remove empty lines
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += " " + paragraph
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
    
    # Append the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def extract_text_with_metadata(pdf_path, chunk_size=1000):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                chunks = chunk_text(text, chunk_size)
                for chunk in chunks:
                    data.append({
                        'page_number': page_num + 1,
                        'text': chunk
                    })
    return data

def save_to_json(data, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)


pdf_directory = os.path.expanduser('FILE PATH HERE')
output_directory = os.path.expanduser('.')

extracted_data = extract_text_with_metadata(pdf_directory)

json_file_path = os.path.join(output_directory, 'chunks.json')
save_to_json(extracted_data, json_file_path)
