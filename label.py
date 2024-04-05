import os
import csv

def label_spacing_errors(text):
    """
    Label spacing errors in the text data and return the labeled data.
    """
    labeled_text = []
    start_index = None
    for i, char in enumerate(text):
        if char == ' ':
            if start_index is None:
                start_index = i
        elif start_index is not None:
            end_index = i - 1
            if end_index > start_index:
                labeled_text.append({'start_index': start_index, 'end_index': end_index})
            start_index = None
    return labeled_text

def process_text_folder(input_folder, output_file):
    """
    Process all text files in the input folder, label spacing errors,
    and store the labeled data in a CSV file.
    """
    # Open the CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_name', 'start_index', 'end_index']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Process each text file in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                input_file = os.path.join(input_folder, filename)

                # Read the text content from the input file
                with open(input_file, "r", encoding="utf-8") as f:
                    text = f.read()

                # Label spacing errors
                spacing_errors = label_spacing_errors(text)

                # Write spacing error labels to the CSV file
                for error in spacing_errors:
                    writer.writerow({'file_name': filename, 'start_index': error['start_index'], 'end_index': error['end_index']})

                print(f"Labeled: {input_file}")

# Input and output folder paths
input_folder = "cleaneddataset/issues"
output_file = "labeled_data.csv"

# Process text folder and store labeled data in CSV file
process_text_folder(input_folder, output_file)
