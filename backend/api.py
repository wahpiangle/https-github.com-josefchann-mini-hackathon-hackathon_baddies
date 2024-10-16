from fastapi import FastAPI
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import string
import spacy
from spellchecker import SpellChecker

# Load Spacy English model for named entity recognition (NER)
nlp = spacy.load('en_core_web_sm')
spell = SpellChecker()
spell.word_frequency.load_text_file("../words.txt")
spell.word_frequency.load_text_file("../tech_words_list.txt")

# Define the FastAPI app
app = FastAPI()

# Input model for the API
class TextsInput(BaseModel):
    texts: list[str]

def clean_word(word):
    # Retain apostrophes but remove other punctuation
    return word.strip(string.punctuation.replace("'", ""))

def check_spelling(text):
    # Use Spacy to identify named entities (proper nouns)
    doc = nlp(text)
    named_entities = {ent.text for ent in doc.ents if ent.label_ == "PERSON"}

    words = [clean_word(word) for word in text.split()]

    # Exclude and named entities from spell checking
    misspelled = spell.unknown(word for word in words if word not in named_entities)

    if not misspelled:
        return {"original_text": text, "error": False, "message": "No errors found.", "corrected_text": text}

    corrected_words = []
    for word in text.split():
        cleaned_word = clean_word(word)
        if cleaned_word in misspelled:
            correction = spell.correction(cleaned_word)
            # Replace the cleaned word with its corrected version
            corrected_words.append(word.replace(cleaned_word, correction))
        else:
            corrected_words.append(word)

    # Join the words back into a corrected sentence
    corrected_text = ' '.join(corrected_words)

    # Format the output for errors found
    return {
        "original_text": text,
        "error": True,
        "misspelled_words": list(misspelled),
        "corrected_text": corrected_text
    }

def check_multiple_texts_concurrently(texts):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(check_spelling, texts))
    return results

# Define the POST API route
@app.post("/check-spelling")
def check_spelling_endpoint(input_data: TextsInput):
    results = check_multiple_texts_concurrently(input_data.texts)
    return {"results": results}

