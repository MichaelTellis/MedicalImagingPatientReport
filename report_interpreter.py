from openai import OpenAI
import sys
import os
from pdf2image import convert_from_path
import pytesseract


# --- Convert Text file to strinvg---
def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        with open(filename, "r", encoding="latin1") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Could not find '{filename}'. Please check the file location.")
        return ""



# --- Convert PDF to string using OCR only ---
def pdf_to_text_with_ocr(pdf_path):
    try:
        pages = convert_from_path(pdf_path, dpi=300)
        text = ""
        for i, page in enumerate(pages):
            print(f"🔍 OCR on page {i+1} of {len(pages)}...")
            page_text = pytesseract.image_to_string(page)
            text += page_text + "\n"
        print(type(text))
        return text
    except Exception as e:
        print(f"❌ OCR failed: {e}")
        return ""

#Calls OpenAI API with prompt and report, returns output text
def interpret_report(report_text, prompt_text,filename):
    prompt = f"""{prompt_text} {report_text}
"""

    response = client.responses.create(
        model="gpt-4o",
        input = [{"role": "user", "content": prompt}],
        temperature = 0.2
    )
    output_tokens[filename] = response.usage.output_tokens

    return response.output_text

#Script Start --------------------------------------------------------------------

report_folder = sys.argv[1]
prompt_path = sys.argv[2]
output_folder = sys.argv[3]
api_key = None
if len(sys.argv)> 4:
    api_txt = sys.argv[4]
    api_key = load_file(api_txt)

else:
    api_key = os.getenv("OPENAI_API_KEY")
    

client = OpenAI(api_key = api_key)
#output_path = "/Users/michaeltellis/OpenaiOutput"

output_tokens = {}
print(report_folder)

if __name__ == "__main__":
    
    prompt_text = load_file(prompt_path)
    if not prompt_text.strip():
        print("Prompt is empty or could not be loaded.")
        sys.exit(1)
    for filename in os.listdir(report_folder):
        report_path = os.path.join(report_folder, filename)
        if filename.endswith(".txt"):
            report_text = load_file(report_path)
            print(report_text)
        elif filename.endswith(".pdf"):
            report_text = pdf_to_text_with_ocr(report_path)
            print(report_text)
        else:
            continue  # skip unknown file types
        
        print(f"\n=== Processing: {filename} ===")
        
        if report_text.strip():
            result = interpret_report(report_text,prompt_text,filename)
            print("\n===== AI-Generated Explanation =====\n")
            print(result)
            #save output to file
            output_path = os.path.join(output_folder, f"{filename}_interpreted.txt")
            print("Saving to output Path: " + output_path)

            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(result)
        else:
            print("No report text found. Please check your file.")

print(output_tokens)