import requests
import random
import string
import re

easy = ['apple', 'happy', 'friend', 'blue', 'cat', 'sun', 'dog', 'bird', 'fish', 'ship', 'moon', 'door', 'park', 'song', 'pen', 'hat', 'cake', 'hill', 'rain', 'corn', 'smile', 'road', 'bike', 'bell', 'duck', 'sand', 'hill', 'town', 'frog', 'soap', 'farm', 'shoe', 'juice', 'chair', 'shirt', 'tiger', 'phone', 'plant', 'sleep', 'happy', 'friend', 'blue', 'cat', 'sun', 'dog', 'bird', 'fish', 'ship', 'moon', 'door', 'park', 'song', 'pen', 'hat', 'cake']


medium =  ['ambivalence', 'serendipity', 'ephemeral', 'quintessential', 'benevolent', 'meticulous', 'resilient', 'surreptitious', 'integrity', 'vulnerable', 'capricious', 'defenestration', 'enervate', 'gregarious', 'hedonist', 'insidious', 'labyrinthine', 'mellifluous', 'nefarious', 'obsequious', 'parsimonious', 'quixotic', 'recalcitrant', 'salubrious', 'taciturn', 'ubiquitous', 'welter', 'xenophobic', 'yearn', 'zealous', 'alacrity', 'belligerent', 'cathartic', 'deleterious', 'effervescent', 'facetious', 'gregarious', 'histrionic', 'impetuous', 'jejune', 'kaleidoscope', 'labyrinth', 'misanthrope', 'nebulous', 'opulent', 'panacea', 'quandary', 'recondite', 'serendipity', 'tantamount', 'ubiquitous', 'verisimilitude', 'wanton', 'xenophobia', 'zenith', 'altruistic', 'benevolent', 'cogent', 'didactic', 'efficacious', 'gregarious', 'hallowed', 'iconoclast', 'juxtapose', 'kowtow', 'laconic', 'magnanimous', 'nadir', 'obfuscate', 'pedantic', 'quintessential', 'reverent', 'sycophant', 'trepidation', 'ubiquitous', 'verbose', 'winsome', 'xenophobe', 'yearn', 'zenith', 'agnostic', 'bucolic', 'catalyst', 'dichotomy', 'frugal', 'garrulous']


hard = ['paradox', 'equanimity', 'ubiquitous', 'cacophony', 'ebullient', 'idiosyncrasy', 'quixotic', 'deleterious', 'antediluvian', 'perspicacious', 'anachronistic', 'bombastic', 'cynosure', 'diaphanous', 'ebullient', 'fugacious', 'garrulous', 'histrionic', 'iconoclast', 'jejune', 'kaleidoscope', 'labyrinthine', 'mellifluous', 'nefarious', 'obsequious', 'peregrinate', 'quiescent', 'recalcitrant', 'salubrious', 'tantamount', 'ululate', 'vexatious', 'winsome', 'xenophobia', 'yonder', 'zephyr', 'aberration', 'beleaguer', 'cavalcade', 'desultory', 'effulgent', 'facetious', 'genuflect', 'hagiography', 'inculcate', 'juxtapose', 'kowtow', 'lambent', 'maelstrom', 'nadir', 'obfuscate', 'pastiche', 'quandary', 'ratiocinate', 'sangfroid', 'terpsichorean', 'ubiquitous', 'vacillate', 'welter', 'xenophobe', 'yearn', 'zenith', 'abstemious', 'bucolic', 'cogent', 'deleterious', 'effervescent', 'gregarious', 'hallowed', 'iconoclast', 'juxtapose', 'kowtow', 'laconic', 'magnanimous', 'nadir', 'obfuscate', 'pedantic', 'quintessential', 'reverent', 'sycophant', 'trepidation', 'ubiquitous', 'verbose', 'winsome', 'xenophobe', 'yearn', 'zenith', 'agnostic', 'bucolic']



DIC_KEY = 'f41c1a5b-1a8c-481b-9175-6ba7d619643c'
DIC_URL = 'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={api_key}'

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
            definitions = word_details.get('shortdef', [0])
            
            # Remove punctuation from definitions
            clean_definitions = []
            for definition in definitions:
                first_the_index = definition.find('the')
                if first_the_index != -1:
                    clean_definition = definition[:first_the_index]
                else:
                    clean_definition = definition
                    
                clean_definition = clean_definition.translate(str.maketrans('', '', string.punctuation))
                clean_definitions.append(clean_definition.strip())
    
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
    
            #(details)
            return details
            
    
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

def clean_list(original_list, words_to_remove):
    cleaned_list = [word for word in original_list if word not in words_to_remove]
    print(cleaned_list)
    return cleaned_list






