import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Step 1: Load labeled data and corresponding correct text
def load_data(csv_file, incorrect_folder, correct_folder):
    labeled_data = pd.read_csv(csv_file)
    incorrect_texts = {}
    correct_texts = {}
    for index, row in labeled_data.iterrows():
        file_name = row['file_name']
        start_index = row['start_index']
        end_index = row['end_index']
        
        incorrect_file_path = os.path.join(incorrect_folder, file_name)
        correct_file_name = file_name.replace(' with issues', '')  # Remove ' with issues' from file name
        correct_file_path = os.path.join(correct_folder, correct_file_name)
        
        print("File name:", file_name)
        print("Incorrect file path:", incorrect_file_path)
        print("Correct file path:", correct_file_path)
        print("Start index:", start_index)
        print("End index:", end_index)
        
        if os.path.exists(incorrect_file_path) and os.path.exists(correct_file_path):
            with open(incorrect_file_path, 'r', encoding='utf-8') as incorrect_file:
                incorrect_text = incorrect_file.read()[start_index:end_index]
                incorrect_texts[file_name] = incorrect_text
                print("Incorrect text:", incorrect_text)
            with open(correct_file_path, 'r', encoding='utf-8') as correct_file:
                correct_text = correct_file.read()
                correct_texts[file_name] = correct_text
                print("Correct text:", correct_text)
        else:
            print(f"File '{file_name}' not found in both folders.")
    return labeled_data, incorrect_texts, correct_texts




# Step 2: Feature Engineering (Tokenization and Vectorization)
def tokenize_and_vectorize(labeled_data, incorrect_texts, correct_texts):
    incorrect_sentences = []
    correct_sentences = []
    for index, row in labeled_data.iterrows():
        incorrect_text = incorrect_texts[row['file_name']]
        correct_text = correct_texts[row['file_name']]
        incorrect_sentences.append(incorrect_text)
        correct_sentences.append(correct_text)
    
    # Tokenize the sentences based on whitespace
    vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b', min_df=1, stop_words=None)
    X = vectorizer.fit_transform(incorrect_sentences)
    
    print("Tokenized and vectorized data successfully.")
    print("Number of samples:", X.shape[0])  # Use shape[0] to get the number of samples
    print("Vectorized feature shape:", X.shape)
    
    return X, vectorizer, correct_sentences


# Step 3: Model Training
def train_model(X, y):
    model = LogisticRegression()
    model.fit(X, y)
    print("Model trained successfully!")
    return model

# Step 4: Model Evaluation
def evaluate_model(model, X_test, y_test):
    # Skip printing classification report
    pass

# Step 5: Load labeled data and corrected text
labeled_data, incorrect_texts, correct_texts = load_data('labeled_data.csv', 'cleaneddataset/issues', 'cleaneddataset/correct')

# Step 6: Feature Engineering
print("Step 6: Feature Engineering")
X, vectorizer, correct_texts_list = tokenize_and_vectorize(labeled_data, incorrect_texts, correct_texts)

# Step 7: Split dataset into training and testing sets
print("Step 7: Split dataset into training and testing sets")
X_train, X_test, y_train, y_test = train_test_split(X, correct_texts_list, test_size=0.2, random_state=42)
print("Training set size:", X_train.shape[0])  # Use shape[0] to get the number of samples
print("Testing set size:", X_test.shape[0])  # Use shape[0] to get the number of samples

# Step 8: Train the model
print("Step 8: Train the model")
model = train_model(X_train, y_train)

# Step 9: Evaluate the model
print("Step 9: Evaluate the model")
evaluate_model(model, X_test, y_test)

# Step 10: Correct spacing issues (Example)
def correct_spacing_issues(text):
    # Assuming the model is already trained and stored in 'model'
    X_text = vectorizer.transform([text])
    corrected_text = model.predict(X_text)
    return corrected_text[0]  # Assuming the corrected text is a single string, not a list

# Example: Correct spacing issues in a text document
text_with_spacing_issues = "This   is   a    sentence    with   multiple     spaces."
print("Original Text:", text_with_spacing_issues)
corrected_text = correct_spacing_issues(text_with_spacing_issues)
print("Corrected Text:", corrected_text)
