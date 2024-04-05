import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file while preserving spacing and alignment.
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            for obj in page.extract_text().split('\n'):
                text += obj + '\n'
    return text

def process_pdf_folder(input_folder, output_folder):
    """
    Process all PDF files in the input folder, convert them to text format,
    and save the extracted text data to the output folder.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process each PDF file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".txt")

            # Extract text from PDF while preserving spacing and alignment
            text = extract_text_from_pdf(pdf_path)

            # Save the extracted text data to a text file
            with open(output_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)

            print(f"Processed: {pdf_path} -> {output_path}")

# Input and output folder paths
input_folder = "rawdataset"
output_folder = "cleaneddataset"

# Process PDF folder
process_pdf_folder(input_folder, output_folder)
