import fitz

def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype='pdf') as doc :
        for page in doc :
            text += page.get_text()
        return text.strip()
    
    #upgrade cuz string concatenation inside loops is slow
    # pages_text = []
    # for page in doc:
        #pages_texxt.append(page.get_text())
    #return "\n".join(pages_text).strip()