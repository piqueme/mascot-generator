import os
import sys
import json
import xml.etree.ElementTree as ET
import requests
from wordfreq import word_frequency
from wn import WordNet

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')

def get_list_file(list_name):
    return os.path.join(DATA_DIR, list_name + '.json')

def dump_to_file(word_list, list_name):
    output_file_name = get_list_file(list_name)
    with open(output_file_name, 'w') as output_file:
        json.dump(word_list, output_file, indent=2)

def get_adjectives_list():
    wordnet = WordNet()
    adjective_synsets = wordnet.all_synsets(pos='s')
    adjectives_set = set()
    for synset in adjective_synsets:
        adjectives_set.update(synset.lemma_names())
    dump_to_file(list(adjectives_set), 'adjectives')

def fetch_birds_list():
    BIRDS_LIST_URL = 'http://www.worldbirdnames.org/master_ioc-names_xml.xml'
    birds_list_response = requests.get(BIRDS_LIST_URL)
    return birds_list_response.text

def parse_birds_list(birds_list_xml):
    root = ET.fromstring(birds_list_xml)
    species = root.findall('.//species/english_name')
    return [spec.text for spec in species]

def get_birds_list():
    birds_list_xml = fetch_birds_list()
    birds_list = parse_birds_list(birds_list_xml)
    dump_to_file(birds_list, 'birds')

def extract_short_names(object_name_list):
    short_names = [object_name.split()[-1] for object_name in object_name_list]
    return sorted(set(short_names))

def load_word_list(list_name):
    list_filename = get_list_file(list_name)
    with open(list_filename, 'r') as list_file:
        return json.load(list_file)

def get_frequencies(word_list):
    word_frequencies = { w: word_frequency(w, 'en') for w in word_list }
    frequency_total = sum([
        word_freq[1] for word_freq in word_frequencies.items()
    ])
    word_frequencies = { w: f / frequency_total for w, f in word_frequencies }
    return word_frequencies

'''
Data
1. Full names (birds, fruits, vegetables)
2. Nouns / Proper Nouns
3. Adjectives
4. Frequency (percentiles)

Sources
1. Dictionary (POS-tagged)
2. 1-grams with frequencies

Algorithm
1. Select adjective in percentile range
2. Select noun in percentile range
3. Filter adjectives / nouns with more than X syllables
4. Select uniformly at random from nouns, adjectives
5. Filter joined (adjective + noun)
'''

if __name__ == '__main__':
    birds_list_xml = fetch_birds_list()
    birds_list = parse_birds_list(birds_list_xml)
    birds_shortname_list = extract_bird_short_names(birds_list)
    print(birds_list[0:10])
    print(birds_shortname_list[0:10])

    # xml_file = sys.argv[1]
    # page_start, page_end = int(sys.argv[2]), int(sys.argv[3])
    # with open(xml_file) as f:
    #     birds_list_contents = f.read()
    #     birds_list = parse_birds_list(birds_list_contents)
    #     shortname_birds_list = extract_bird_short_names(birds_list)
    #     print("***** SPECIES *****")
    #     print("\n".join(birds_list[page_start:page_end]))
    #     print("")
    #     print("***** SHORT NAMES *****")
    #     print("\n".join(shortname_birds_list[page_start:page_end]))


