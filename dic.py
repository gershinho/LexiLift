import requests
import random
import string
import re


easy = ['happy', 'friend', 'blue', 'cat', 'sun', 'dog', 'fish', 'ship', 'moon', 'door', 'park', 'song', 'pen', 'hat', 'cake', 'rain', 'smile', 'road', 'bell', 'duck', 'town', 'frog', 'farm', 'shoe', 'juice', 'chair', 'shirt', 'tiger', 'phone', 'plant', 'sleep', 'happy', 'friend', 'blue', 'cat', 'sun', 'dog', 'fish', 'ship', 'moon', 'door', 'park', 'song', 'pen', 'hat', 'cake', 'light', 'box', 'wind', 'bread', 'wall', 'cup', 'note', 'map', 'glue', 'queen', 'robot', 'spoon', 'train', 'whale', 'bat', 'cake', 'cat', 'dog', 'ear', 'fan', 'hat', 'ink', 'rat', 'sun', 'web']

medium = ['ambivalence', 'ephemeral', 'quintessential', 'benevolent', 'meticulous', 'surreptitious', 'vulnerable', 'defenestration', 'gregarious', 'hedonist', 'insidious', 'labyrinthine', 'mellifluous', 'recalcitrant', 'salubrious', 'ubiquitous', 'yearn', 'zealous', 'alacrity', 'cathartic', 'deleterious', 'effervescent', 'facetious', 'gregarious', 'histrionic', 'impetuous', 'jejune', 'kaleidoscope', 'labyrinth', 'nebulous', 'opulent', 'panacea', 'recondite', 'tantamount', 'ubiquitous', 'wanton', 'zenith', 'altruistic', 'benevolent', 'cogent', 'didactic', 'efficacious', 'gregarious', 'juxtapose', 'kowtow', 'magnanimous', 'obfuscate']

hard = ['equanimity', 'ubiquitous', 'cacophony', 'ebullient', 'deleterious', 'antediluvian', 'cynosure', 'diaphanous', 'ebullient', 'garrulous', 'histrionic', 'jejune', 'kaleidoscope', 'labyrinthine', 'mellifluous', 'quiescent', 'recalcitrant', 'salubrious', 'tantamount', 'ululate', 'vexatious', 'winsome', 'aberration', 'cavalcade', 'desultory', 'facetious', 'genuflect', 'hagiography', 'juxtapose', 'kowtow', 'maelstrom', 'obfuscate', 'pastiche', 'ubiquitous', 'yearn', 'zenith', 'abstemious', 'cogent', 'deleterious', 'effervescent', 'gregarious']
# Usage of merriam webster API
DIC_KEY = 'f41c1a5b-1a8c-481b-9175-6ba7d619643c'
DIC_URL = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

#Aid of Open AI to filter through data of API 
def fetch_word_details(word):
    url = DIC_URL.format(word=word, api_key=DIC_KEY)
    try:
        response = requests.get(url)
        json_data = response.json()
        
        if json_data and isinstance(json_data, list) and 'shortdef' in json_data[0]:
            word_details = json_data[0]
            
            # Extracting necessary details
            word_id = word_details.get('meta', {}).get('id', '')
            word_id = word_id.split(':')[0]
            part_of_speech = word_details.get('fl', '')
            definitions = word_details.get('shortdef', [])
            
            # Remove punctuation from definitions and filter out short ones
            clean_definitions = []
            for definition in definitions:
                definition = definition.translate(str.maketrans('', '', string.punctuation))
                if len(definition.split()) >= 5:
                    clean_definitions.append(definition.strip())
    
            # Extracting example sentences
            examples = []
            if 'def' in word_details:
                for d in word_details['def']:
                    for sseq in d['sseq']:
                        for sense in sseq:
                            if isinstance(sense, list):  # Check if sense is a list
                                for dt in sense[1].get('dt', []):
                                    if dt[0] == 'vis':
                                        for vis in dt[1]:
                                            example_text = vis.get('t', '').strip()
                                            if example_text:  # Ensure example is not empty
                                                examples.append(example_text)
                            elif isinstance(sense, dict):  # Check if sense is a dictionary
                                for dt in sense.get('dt', []):
                                    if dt[0] == 'vis':
                                        example_text = dt[1].get('t', '').strip()
                                        if example_text:  # Ensure example is not empty
                                            examples.append(example_text)
    
            example = ""
            if examples:
                example = random.choice(examples)
                processed_example_parts = []
                for part in re.split(r'[_]+', example):
                    cleaned_part = re.sub(r'{.*?}', '', part)
                    processed_example_parts.append(cleaned_part)
                example_processed = ' '.join(processed_example_parts)
                new_example = re.sub(r"_{2,}", "", example_processed)
                example = new_example.replace(word, '____')
    
            details = {
                'word_id': word_id,
                'part_of_speech': part_of_speech,
                'definitions': clean_definitions,
                'example': example,
            }
    
            if clean_definitions:  # Ensure there are valid definitions
                return details
            else:
                print(f"No valid definitions for '{word}'")
    
        else:
            print("shortdef not found in the response for word:", word)
    
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for '{word}': {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON for '{word}': {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for '{word}': {e}")
        return None

def check_for_errors(words):
    words_with_issues = []
    for word in words:
        details = fetch_word_details(word)
        if details is None:
            words_with_issues.append(word)
        elif not details.get('example') or details['example'].strip() == '':
            words_with_issues.append(word)
    
    return words_with_issues


#Aid of Open AI for cleaning and filtering lists

def clean_list(original_list, words_to_remove):
    cleaned_list = [word for word in original_list if word not in words_to_remove]
    print(cleaned_list)
    return cleaned_list

def filter_words_with_long_examples(word_list):
    filtered_words = []
    for word in word_list:
        details = fetch_word_details(word)
        if details and 'example' in details and len(details['example'].split()) > 3:
            filtered_words.append(word)
    return filtered_words

# Example usage
# filtered_easy_words = filter_words_with_long_examples(easy)
# filtered_medium_words = filter_words_with_long_examples(medium)
# filtered_hard_words = filter_words_with_long_examples(hard)

# print("Filtered Easy Words:", filtered_easy_words)
# print("Filtered Medium Words:", filtered_medium_words)
# print("Filtered Hard Words:", filtered_hard_words)

 # Example usage
 # words_with_issues = check_for_errors(easy)
 # cleaned_easy_words = clean_list(easy, words_with_issues)
 # print(cleaned_easy_words)
