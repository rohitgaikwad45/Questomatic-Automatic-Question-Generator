# question_generation_english.py
 
import re
import random

def generate_questions_english(text, num_questions):
    questions = []
    sections = re.split(r'\n[A-Z][a-zA-Z\s]+\n', text)
    for section in sections:
        section_title = ''
        if not section.strip():
            continue
        title_match = re.match(r'\n([A-Z][a-zA-Z\s]+)\n', section)
        if title_match:
            section_title = title_match.group(1)
        key_points = re.findall(r'\n(\w+(?:\s+\w+)*):\s*([^:]+)', section)
        for point in key_points:
            question_templates = [
                f"What is {point[0]}  {section_title.lower()}?",
                f"Explain the application of {point[0]}.",
                f"What does the term {point[0]} refer to?",
                f"What are the key points related to {point[0]}?",
                f"What are the advantages of {point[0]}?",
                f"What are the disadvantages of {point[0]}?",
                f"Discuss examples of {point[0]}.",
                f"Explain in detail the significance of {point[0]}.",
                f"Define {point[0]}.",
                f"Explain {point[0]} in the context {section_title.lower()}.",
                f"How does {point[0]} relate to {section_title.lower()}?",
                f"Discuss {point[0]} as mentioned in the {section_title.lower()} .",
                f"Provide an example of {point[0]} {section_title.lower()} .",
                f"Explain {point[0]} in detail with examples.",
                f"Write a short note on {point[0]}.",
                f"Explain {point[0]} in simple terms.",
                f"Explain {point[0]} in simple terms with examples.",
                f"Explain in brief {point[0]}.",
                f"What are the significance of {point[0]}?",
            ]
            
            random.shuffle(question_templates)
            
            selected_question_templates = question_templates[:2]
            
            questions.extend(selected_question_templates)
    
    return questions[:num_questions]