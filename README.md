# Sentiment Analysis and Readability Calculation

## Overview
This project provides a Python script for sentiment analysis and readability calculation of text data. It includes functionality to scrape web pages, preprocess text, analyze sentiment, calculate readability metrics, and store the results in an Excel file.

## File Structure
- `final_script.py`: Contains the main script for sentiment analysis and readability calculation.
- `StopWords/`: Folder containing text files with stopwords.
    - `positive-words.txt`: List of positive words.
    - `negative-words.txt`: List of negative words.
- `Input.xlsx`: Input file containing URLs for web scraping.
- `all_file/`: Folder to store text files and scraped web pages.
- `Output_Data.xlsx`: Output file containing analysis results.

## Execution Instructions
1. Download the project files from [Google Drive](https://drive.google.com/drive/folders/1Axir6qf7G-GTEMjmqreXj8yjcvAqHYJU?usp=sharing).
2. Ensure all dependencies are installed.
3. Place input data (text files or URLs) in the appropriate folder.
4. Run the `final_script.py` script to perform sentiment analysis and calculate readability metrics.
> 👉 run cammand:
```
python final_script.py
```
5. Review the output file (`Output_Data.xlsx`) for analysis results.

## Dependencies
- Python 3.x
- NLTK (Natural Language Toolkit)
- pandas
- BeautifulSoup (for web scraping)

## Approach
The script utilizes NLTK for text processing, including tokenization and stopwords removal.
Sentiment analysis is performed using lists of positive and negative words.
Readability metrics are calculated based on the number of sentences, words, and syllables in the text.

## Additional Notes
- Ensure Python 3.x and pip are installed on your system.
- NLTK resources need to be downloaded before running the script (`nltk.download('punkt')`, `nltk.download('cmudict')`).
