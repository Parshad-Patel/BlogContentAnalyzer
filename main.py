import os
import string

import nltk
import pandas as pd

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('cmudict')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict


import requests

from bs4 import BeautifulSoup


# Function to load stopwords from a folder
def load_stopwords(stopwords_folder):
    stop_words = []
    if not os.path.exists(stopwords_folder):
        print("Error: Folder not found:", stopwords_folder)
        return stop_words

    for filename in os.listdir(stopwords_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(stopwords_folder, filename)
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    words = file.read().splitlines()
                    stop_words += words
            except Exception as e:
                print("Error reading file:", file_path)
                print(e)
    return stop_words


# Functions to calculate positive and negative scores
def Positive_Score(positive_words_file_path, final_words):
    p_words = []
    p_score = 0
    try:
        with open(positive_words_file_path, 'r', encoding='latin-1') as file:
            positive_words = file.read().splitlines()
            p_words += positive_words
    except Exception as e:
        print("Error reading file:", positive_words_file_path)
        print(e)
    for word in final_words:
        if word in p_words:
            p_score += 1
    return p_score


def Negative_Score(negative_words_file_path, final_words):
    n_words = []
    n_score = 0
    try:
        with open(negative_words_file_path, 'r', encoding='latin-1') as file:
            negative_words = file.read().splitlines()
            n_words += negative_words
    except Exception as e:
        print("Error reading file:", negative_words_file_path)
        print(e)
    for word in final_words:
        if word in n_words:
            n_score -= 1
    return n_score * -1


# Functions to calculate polarity and subjectivity scores
def Polarity_Score(p_score, n_score):
    polarity_Score = (p_score - n_score) / ((p_score + n_score) + 0.000001)
    return polarity_Score


def Subjectivity_Score(p_score, n_score, final_words):
    Total_Words_after_cleaning = len(final_words)
    subjectivity_Score = (p_score + n_score) / ((Total_Words_after_cleaning) + 0.000001)
    return subjectivity_Score


# Function to count complex words using CMU Pronouncing Dictionary
def count_complex_words(words):
    d = cmudict.dict()
    complex_count = 0
    for word in words:
        if word.lower() in d:
            syllables = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
            if max(syllables) > 2:
                complex_count += 1
    return complex_count


# Function to calculate readability metrics
def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    num_sentences = len(sentences)
    num_words = len(words)
    num_complex_words = count_complex_words(words)

    average_sentence_length = num_words / num_sentences
    percentage_complex_words = (num_complex_words / num_words) * 100

    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

    return average_sentence_length, percentage_complex_words, fog_index, num_complex_words


# Function to count syllables in a word
def Count_syllables(tokenized_words):
    vowels = "aeiouy"
    syllables = 0
    skip = False

    for i, letter in enumerate(tokenized_words):
        if skip:
            skip = False
            continue
        if letter in vowels and (i == len(tokenized_words) - 1 or tokenized_words[i + 1] not in vowels):
            syllables += 1
        elif letter in vowels and i == len(tokenized_words) - 2 and tokenized_words.endswith(("es", "ed")):
            syllables += 1
            skip = True

    return syllables


# Function to count personal pronouns in a text
def Count_personal_pronouns(tokenized_words):
    pronouns = ["I", "we", "my", "ours", "us"]
    count = 0
    for i in range(len(tokenized_words)):
        word = tokenized_words[i]
        if word in pronouns:
            if word == "us" and i > 0 and tokenized_words[i - 1].lower() not in ["the", "in"]:
                count += 1
            elif word != "us":
                count += 1
    return count


# Function to calculate average word length
def Average_word_length(tokenized_words):
    total_characters = 0
    total_words = len(tokenized_words)

    for word in tokenized_words:
        total_characters += len(word)

    if total_words > 0:
        average_length = total_characters / total_words
    else:
        average_length = 0

    return average_length


# Function to analyze a single file
def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    lower_case = text.lower()
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = cleaned_text.split()

    stopwords_folder = "StopWords"
    stop_words = load_stopwords(stopwords_folder)

    final_words = []
    for words in tokenized_words:
        if words not in stop_words:
            final_words.append(words)
    word_count = len(final_words)

    positive_words_file_path = "positive-words.txt"
    negative_words_file_path = "negative-words.txt"
    p_score = Positive_Score(positive_words_file_path, final_words)
    n_score = Negative_Score(negative_words_file_path, final_words)
    polarity_score = Polarity_Score(p_score, n_score)
    subjectivity_score = Subjectivity_Score(p_score, n_score, final_words)

    average_sentence_length, percentage_complex_words, fog_index, num_complex_words = calculate_readability(text)

    syllables = Count_syllables(tokenized_words)

    personal_pronouns_count = Count_personal_pronouns(tokenized_words)

    avg_word_length = Average_word_length(tokenized_words)

    return {
        "Positive_Score": p_score,
        "Negative_Score": n_score,
        "Polarity_Score": polarity_score,
        "Subjectivity_Score": subjectivity_score,
        "Average_Sentence_Length": average_sentence_length,
        "Percentage_Complex_Words": percentage_complex_words,
        "Fog_Index": fog_index,
        "Num_Complex_Words": num_complex_words,
        "Word_Count": word_count,
        "Syllables": syllables,
        "Personal_Pronouns_Count": personal_pronouns_count,
        "Average_Word_Length": avg_word_length
    }


# Function to analyze all files in a folder
def analyze_all_files(folder_path):
    analysis_results = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            url_id = os.path.splitext(filename)[0]
            analysis_results[url_id] = analyze_file(file_path)
    return analysis_results


# Function to save analysis results to an Excel file
def save_to_excel(analysis_results, output_file, url_id):
    df = pd.read_excel(output_file)
    index = df.index[df['URL_ID'] == url_id].tolist()[0]
    df.at[index, 'POSITIVE_SCORE'] = analysis_results['Positive_Score']
    df.at[index, 'NEGATIVE_SCORE'] = analysis_results['Negative_Score']
    df.at[index, 'POLARITY_SCORE'] = analysis_results['Polarity_Score']
    df.at[index, 'SUBJECTIVITY_SCORE'] = analysis_results['Subjectivity_Score']
    df.at[index, 'AVG_SENTENCE_LENGTH'] = analysis_results['Average_Sentence_Length']
    df.at[index, 'PERCENTAGE_OF_COMPLEX_WORDS'] = analysis_results['Percentage_Complex_Words']
    df.at[index, 'FOG_INDEX'] = analysis_results['Fog_Index']
    df.at[index, 'AVG_NUMBER_OF_WORDS_PER_SENTENCE'] = analysis_results['Average_Sentence_Length']
    df.at[index, 'COMPLEX_WORD_COUNT'] = analysis_results['Num_Complex_Words']
    df.at[index, 'WORD_COUNT'] = analysis_results['Word_Count']
    df.at[index, 'SYLLABLE_PER_WORD'] = analysis_results['Syllables']
    df.at[index, 'PERSONAL_PRONOUNS'] = analysis_results['Personal_Pronouns_Count']
    df.at[index, 'AVG_WORD_LENGTH'] = analysis_results['Average_Word_Length']
    df.to_excel(output_file, index=False)


# Main function to run the analysis
def analyze_all_files_main():
    folder_path = "all_file"
    analysis_results = analyze_all_files(folder_path)
    output_file = "Output_Data.xlsx"
    for url_id, result in analysis_results.items():
        save_to_excel(result, output_file, url_id)
    print("Analysis completed and saved to Excel file.")


# extract article text
def extract_article_text_main():
    excel_file_path = "Input.xlsx"  # Update with your file path
    df = pd.read_excel(excel_file_path)

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        url = row['URL']
        url_id = row['URL_ID']
        extract_article_text(url, url_id)
    

def extract_article_text(url, url_id):
    try:
        # get the html 
        content = requests.get(url)
        htmlcontent = content.text

        # parse the html 
        soup = BeautifulSoup(htmlcontent, 'html.parser')

        # get the title of the html page 
        title = soup.title.string

        # get the text of the html page
        article_text = ""
        paras = soup.find_all('div',class_='td-post-content tagdiv-type')
        for para in paras:
         for child in para.children:
                # Check if the child is a <pre> tag, and skip it
                if child.name == 'pre':
                    continue
                # Otherwise, append the text to article_text
                article_text += child.get_text()

        # Write the extracted title and text to a text file
        filename = f"all_file/{url_id}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Title: " + title + "\n")
            file.write(article_text)

        print(f"File '{filename}' saved successfully")
    except Exception as e:
        print(f"Error occurred while processing URL: {url}, Error: {e}")


if __name__ == "__main__":
    extract_article_text_main()
    analyze_all_files_main()