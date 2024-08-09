import stanza
import random

# Download the Marathi language model 
stanza.download('mr')
nlp = stanza.Pipeline('mr')

#  rule-based stemmer
def marathi_stemmer(word):
    suffixes = ['ांना', 'ांना', 'तील', 'तील', 'ने', 'तील', 'ही', 'चा', 'ची', 'चे', 'ला', 'मध्ये', 'त', 'वर', 'ने', 'साठी', 'तरी', 'ते', 'तो', 'ती', 'ले']
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    return word

# Extract keywords
def extract_keywords(doc):
    keywords = []
    for sentence in doc.sentences:
        for word in sentence.words:
            if word.deprel in {'nsubj', 'obj', 'iobj'} and word.upos in {'NOUN', 'PROPN'}:
                stemmed_word = marathi_stemmer(word.text)
                keywords.append(stemmed_word)
    # Remove duplicates
    keywords = list(dict.fromkeys(keywords))
    return keywords


def generate_questions_marathi(text, num_questions):
    doc = nlp(text)
    questions = []
    sentence_templates = [
        "__________ हे स्पष्ट करा.",
        "__________ महत्त्व स्पष्ट करा.",
        "__________ बद्दल थोडक्यात सांगा.",
        "__________ बद्दल काय म्हणता येईल?",
        "__________ फायदे काय आहेत?",
        "__________ तोटे काय आहेत?",
        "__________ उपयोग काय आहेत?",
        "__________ याची उदाहरणे द्या.",
        "__________ चा अर्थ काय आहे?",
        "__________ हा शब्द काय सूचित करतो?",
        "__________ अधिकतम लाभ काय आहे?",
        "__________ दुष्परिणाम काय आहेत?",
        "__________ उदाहरण चर्चा करा.",
        "__________ महत्त्व विस्तारात समजणे.",
        "__________ अर्थ काय आहे?",
        "__________ एक उदाहरण प्रदान करा.",
        "__________ बरोबर उदाहरण सहित विस्तारात समजणे.",
        "__________ विशेष टिप्पणी करा.",
        "__________ एक सोप्पी शब्दांत समजवा.",
        "__________ उदाहरण सहित सोप्प्या शब्दांत समजवा.",
        "__________ संक्षिप्तपणे समजवा."
    ]

    # Extract keywords using dependency parsing
    keywords = extract_keywords(doc)

    # Generate questions using the extracted keywords
    for keyword in keywords:
        for template in sentence_templates:
            questions.append(template.replace('__________', keyword))

    random.shuffle(questions)
    return questions[:num_questions]


# import stanza
# import pandas as pd
# from transformers import pipeline
# import random
# import logging

# # Initialize Stanza NLP pipeline for Marathi
# stanza.download('mr')
# nlp = stanza.Pipeline('mr')

# # Load the pre-trained question generation model
# def load_pretrained_model():
#     model_name = "valhalla/t5-small-qg-hl"  # Using a pre-trained question generation model
#     try:
#         question_generator = pipeline("text2text-generation", model=model_name, tokenizer=model_name, framework="pt")
#         return question_generator
#     except Exception as e:
#         logging.error(f"Error loading the pre-trained model: {e}")
#         return None

# # Extract key phrases using Stanza and generate questions using the pre-trained model
# def generate_questions_marathi(text, num_questions):
#     # Initialize the pre-trained model
#     question_generator = load_pretrained_model()
#     if question_generator is None:
#         return ["Error loading the pre-trained model"]

#     # Process the input text with Stanza
#     doc = nlp(text)

#     # Extract key phrases (we use simple noun extraction for this example)
#     key_phrases = []
#     for sentence in doc.sentences:
#         for word in sentence.words:
#             if word.upos in ["NOUN", "PROPN"]:  # Consider nouns and proper nouns as key phrases
#                 key_phrases.append(word.text)

#     # Generate questions based on key phrases
#     questions = []
#     for phrase in key_phrases:
#         input_text = f"generate question: {phrase}"
#         generated = question_generator(input_text)
#         for question in generated:
#             questions.append(question['generated_text'])

#     # Shuffle and return the specified number of questions
#     random.shuffle(questions)
#     return questions[:num_questions]


# import stanza
# import random

# stanza.download('mr')
# nlp = stanza.Pipeline('mr')

# def generate_questions_marathi(text, num_questions):
#     doc = nlp(text)
#     questions = []
#     sentence_templates = [
#         "__________ हे स्पष्ट करा.",
#         "__________ महत्त्व स्पष्ट करा.",
#         "__________ बद्दल थोडक्यात सांगा.",
#         "__________ बद्दल काय म्हणता येईल?",
#         "__________ फायदे काय आहेत?",
#         "__________ तोटे काय आहेत?",
#         "__________ उपयोग काय आहेत?",
#         "__________ याची उदाहरणे द्या.",
#         "__________ चा अर्थ काय आहे ?",
#         "__________ हा शब्द काय सूचित करतो?",
#         "__________ अधिकतम लाभ काय आहे?",
#         "__________ दुष्परिणाम काय आहेत?",
#         "__________ उदाहरण चर्चा करा .",
#         "__________ महत्त्व विस्तारात समजणे.",
#         "__________ अर्थ काय आहे?",
#         "__________ एक उदाहरण प्रदान करा.",
#         "__________ बरोबर उदाहरण सहित विस्तारात समजणे.",
#         "__________ विशेष टिप्पणी करा.",
#         "__________ एक सोप्पी शब्दांत समजवा.",
#         "__________ उदाहरण सहित सोप्प्या शब्दांत समजवा.",
#         "__________ संक्षिप्तपणे समजवा."
#     ]

#     for sentence in doc.sentences:
#         sentence_text = ' '.join([word.text for word in sentence.words])
#         for template in sentence_templates:
#             questions.append(template.replace('__________', sentence_text))

#     random.shuffle(questions)
#     return questions[:num_questions]





# import stanza
# import random

# # Download the Marathi language model for Stanza
# stanza.download('mr')
# nlp = stanza.Pipeline('mr')

# def generate_questions_marathi(text, num_questions):
#     doc = nlp(text)
#     questions = []
#     sentence_templates = [
#         "__________ हे स्पष्ट करा.",
#         "__________ महत्त्व स्पष्ट करा.",
#         "__________ बद्दल थोडक्यात सांगा.",
#         "__________ बद्दल काय म्हणता येईल?",
#         "__________ फायदे काय आहेत?",
#         "__________ तोटे काय आहेत?",
#         "__________ उपयोग काय आहेत?",
#         "__________ याची उदाहरणे द्या.",
#         "__________ चा अर्थ काय आहे?",
#         "__________ हा शब्द काय सूचित करतो?",
#         "__________ अधिकतम लाभ काय आहे?",
#         "__________ दुष्परिणाम काय आहेत?",
#         "__________ उदाहरण चर्चा करा.",
#         "__________ महत्त्व विस्तारात समजवा.",
#         "__________ अर्थ काय आहे?",
#         "__________ एक उदाहरण प्रदान करा.",
#         "__________ बरोबर उदाहरण सहित विस्तारात समजवा.",
#         "__________ विशेष टिप्पणी करा.",
#         "__________ उदाहरण सहित सोप्प्या शब्दांत समजवा.",
#         "__________ संक्षिप्तपणे समजवा."
#     ]

#     # Extract keywords using Named Entity Recognition (NER)
#     keywords = []
#     for sentence in doc.sentences:
#         for entity in sentence.ents:
#             keywords.append(entity.text)

#     # If no keywords are found, use nouns as keywords
#     if not keywords:
#         for sentence in doc.sentences:
#             for word in sentence.words:
#                 if word.upos == 'NOUN':
#                     keywords.append(word.text)

#     # Generate questions using the extracted keywords
#     for keyword in keywords:
#         for template in sentence_templates:
#             questions.append(template.replace('__________', keyword))

#     random.shuffle(questions)
#     return questions[:num_questions]

