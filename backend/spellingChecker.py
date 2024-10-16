import json
from spellchecker import SpellChecker
from concurrent.futures import ThreadPoolExecutor
import string
import spacy

# Load Spacy English model for named entity recognition (NER)
nlp = spacy.load('en_core_web_sm')
spell = SpellChecker()
spell.word_frequency.load_text_file("../words.txt")
spell.word_frequency.load_text_file("../tech_words_list.txt")

def clean_word(word):
    # Retain apostrophes but remove other punctuation
    return word.strip(string.punctuation.replace("'", ""))

def check_spelling(text):
    # Use Spacy to identify named entities (proper nouns)
    doc = nlp(text)
    named_entities = {ent.text for ent in doc.ents if ent.label_ == "PERSON"}

    words = [clean_word(word) for word in text.split()]

    # Exclude named entities from spell checking
    misspelled = spell.unknown(word for word in words if word not in named_entities)

    # Initialize result dictionary
    result = {
        "error_count": len(misspelled),
    }

    if not misspelled:
        return result  # No errors found, return result as is

    corrected_words = []
    for word in text.split():
        cleaned_word = clean_word(word)
        if cleaned_word in misspelled:
            correction = spell.correction(cleaned_word) or ""
            # Replace the cleaned word with its corrected version
            corrected_words.append(word.replace(cleaned_word, correction))
        else:
            corrected_words.append(word)

    return result

def check_multiple_texts_concurrently(texts):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_spelling, texts))
    return results

input_texts = [
    "This are an exmple sentence with erors. I love machine learning.",
    "Alice and Bobby are working on an example.",
    "Neural networks and quantum computing are the future of N.",
    "The word compiler and encryption are technical terms.",
    "I love using php"
]

# Check spelling for multiple texts
results = check_multiple_texts_concurrently(input_texts)

# Convert results to JSON format and print
json_results = json.dumps(results, indent=4)