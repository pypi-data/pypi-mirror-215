# **KEYWORD AND SYNONYM EXTRACTION PACKAGE**
 The "synonym_custom" package is a versatile tool designed to extract keywords from a given sentence and generate synonyms for those keywords. It combines various modules and libraries to provide multiple approaches for keyword extraction and synonym generation. The package includes the following functionalities:

1. Dictionary-based synonym generation: Utilizes web scraping techniques to extract synonyms from online thesaurus websites.

2. Spacy-based synonym generation: Relies on the Spacy library and its WordNet annotator to generate synonyms using a lexical database.

3. OpenAI-based synonym generation: Leverages OpenAI's language model to generate synonyms by providing a prompt and extracting choices from the model's response.

4. OpenAI-based keyword extraction: Uses OpenAI's language model to extract keywords from a given text by specifying a prompt and processing the model's response.

5. Spacy-based keyword extraction: Implements keyword extraction using Spacy's natural language processing capabilities. It identifies relevant keywords based on part-of-speech (POS) tagging and filters out stopwords and punctuation.

6. NLTK-based keyword extraction: Utilizes the NLTK library for keyword extraction. It applies tokenization, POS tagging, and filtering techniques to identify meaningful keywords.

7. Transformer-based keyword extraction: Employs transformer models for keyphrase extraction. It uses a pre-trained model and tokenizer to identify and format keyphrases from the input text.

# **Installation and Prerequisites for the "synonym_custom" package:**
- To install the "synonym_custom" package and use its functionalities, you need to follow these steps:
- Prerequisites:

- Python: Ensure that Python is installed on your system. The package is compatible with Python 3.8 or higher.
- Pip: Check if you have pip installed, which is the package installer for Python. Pip comes bundled with Python - versions 3.4 and above, so it should already be available.

## Installation:

- Open a command prompt or terminal.
- Run the following command to install the package from the Python Package Index (PyPI): 
```pip install synonym_custom```
- Wait for the installation to complete. The required dependencies will be automatically installed

## Prerequisites:

API Keys: Depending on the functionalities you want to use, you may need to obtain API keys or set up accounts with specific services. The package requires the following API keys:
OpenAI API Key: To use the OpenAI-based synonym generation and keyword extraction functionalities, you need to have an OpenAI API key. If you don't have one, you can sign up for an account and obtain the API key from the [OpenAI](https://openai.com/) website. 
Optional: Some functionalities, such as dictionary-based synonym generation, do not require API keys.

## Usage:

Once you have installed the package and obtained the necessary API keys, you can import it in your Python script or interactive session:

```from synonym_custom.synonym_custom import Synonym_Generator```

1. Using openai to extract keywords : 

```syn_gen = Synonym_Generator(os.getenv('OPENAI_API_KEY'))```

```extracted_keywords = syn_gen.extract_keywords_openai(text)```

2. Using nltk to extract keywords: 

```syn_gen = Synonym_Generator()```

```extracted_keywords = syn_gen.extract_keywords_nltk(text)```

3. Using transformers to extract keywords: 

```syn_gen = Synonym_Generator()```

```extracted_keywords = syn_gen.extract_keywords_trans(text)```

4. Using spacy to extract keywords: 

```syn_gen = Synonym_Generator()```

```extracted_keywords = syn_gen.extract_keywords_spacy(text)```

5. Using dictionary to generate synonyms: 

```synonym_list = syn_gen.dictionary_syn(keyword)```

6. Using openai to generate synonyms: 

```synonym_list = syn_gen.openai_api(keyword)```

7. Using spacy to generate synonyms: 

```synonym_list = syn_gen.spacy_syn(keyword)```
 
By following these steps and providing the necessary API keys, you will be able to install and utilize the "synonym_custom" package to extract keywords from sentences and generate synonyms using multiple modules and libraries.

## Example:

text = "Machine learning is a subfield of artificial intelligence (AI) that focuses on developing algorithms and models that enable computers to learn and make predictions or decisions without being explicitly programmed. It involves the study of statistical and computational models and algorithms that allow machines to learn from and analyze data, recognize patterns, and make data-driven predictions or decisions."

```python
from synonym_custom.synonym_custom import Synonym_Generator

syn_gen = Synonym_Generator(os.getenv('OPENAI_API_KEY'))  ##when using openai_api
syn_gen = Synonym_Generator()
extracted_keywords = syn_gen.extract_keywords_spacy(text) #using sapcy to generate keywords
print("Extracted Keywords:", extracted_keywords)
synonyms_dict = {}
for keyword in extracted_keywords:

    synonym_list = syn_gen.dictionary_syn(keyword) #using dictionary to generate synonyms
    synonyms_dict[keyword] = synonym_list

print("Synonyms of extracted keywords:")
for keyword, synonyms in synonyms_dict.items():
    print(f"{keyword}: {synonyms}")
```





