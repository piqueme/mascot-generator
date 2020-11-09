import os
import random
import sys
import sqlite3
import json
import xml.etree.ElementTree as ET
import requests
import re
import syllables
from wordfreq import word_frequency
from wn import WordNet

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
NUMERIC_PATTERN = re.compile('[0-9]+')

'''
    noun: birds | veggies | fruits
'''
def generate(
    noun='veggies',
    adjective_frequency_percentile_range=[0.4, 0.8],
    noun_frequency_percentile_range=[0, 1],
    max_adjective_syllable_count=3,
    max_noun_syllable_count=3,
    max_total_syllable_count=4):

    connection = sqlite3.connect('mascotgen.db')
    with connection:
        cursor = connection.cursor()
        cursor.execute('''
            WITH adjective_pct AS (
                SELECT
                    *,
                    PERCENT_RANK() OVER(
                        ORDER BY probability
                    ) percentile
                FROM adjectives
                WHERE syllables <= ?
            )
            SELECT *
            FROM adjective_pct
            WHERE percentile >= ?
            AND percentile <= ?
            ''',
            (
                max_adjective_syllable_count,
                adjective_frequency_percentile_range[0],
                adjective_frequency_percentile_range[1]
            )
        )
        adjectives = cursor.fetchall()
        cursor.execute('''
            WITH nouns_pct AS (
                SELECT
                    *,
                    PERCENT_RANK() OVER(
                        ORDER BY probability
                    ) percentile
                FROM %s
                WHERE syllables <= ?
            )
            SELECT *
            FROM nouns_pct
            WHERE percentile >= ?
            AND percentile <= ?
            ''' % (noun,),
            (
                max_noun_syllable_count,
                noun_frequency_percentile_range[0],
                noun_frequency_percentile_range[1]
            )
        )
        nouns = cursor.fetchall()
        random_adjective = adjectives[random.randrange(0, len(adjectives))]
        random_noun = nouns[random.randrange(0, len(nouns))]
        return random_adjective[0] + ' ' + random_noun[0]

def collect_adjectives_list():
    wordnet = WordNet()
    adjective_synsets = wordnet.all_synsets(pos='s')
    adjectives_set = set()
    for synset in adjective_synsets:
        adjectives_set.update(synset.lemma_names())
    adjectives_list = list(adjectives_set)
    adjectives_list = [w for w in adjectives_list if NUMERIC_PATTERN.match(w) is None]
    return adjectives_list

def collect_birds_list():
    BIRDS_LIST_URL = 'http://www.worldbirdnames.org/master_ioc-names_xml.xml'
    birds_list_response = requests.get(BIRDS_LIST_URL)
    birds_list_xml = birds_list_response.text
    root = ET.fromstring(birds_list_xml)
    species_nodes = root.findall('.//species/english_name')
    species = [spec.text.lower() for spec in species_nodes]
    return species

def collect_veggie_list():
    names = [
        "Amaranth Leaves",
        "Arrowroots",
        "Artichokes",
        "Arugulas",
        "Asparaguses",
        "Bamboo Shoots",
        "Green Beans",
        "Beets",
        "Endives",
        "Bitter Melons",
        "Broadbeans",
        "Broccolis",
        "Broccoli Rabes",
        "Brussel Sprouts",
        "Green Cabbages",
        "Red Cabbages",
        "Carrots",
        "Cassavas",
        "Cauliflowers",
        "Celeries",
        "Chayotes",
        "Chicories",
        "Collards",
        "Corns",
        "Crooknecks",
        "Cucumbers",
        "Daikons",
        "Dandelion Greens",
        "Edamames",
        "Eggplants",
        "Fennels",
        "Fiddleheads",
        "Gingers",
        "Horseradishes",
        "Jicamas",
        "Kales",
        "Kohlrabis",
        "Leeks",
        "Lettuces",
        "Mushrooms",
        "Mustard Greens",
        "Okras",
        "Red Onions",
        "Yellow Onions",
        "Parsnips",
        "Peas",
        "Green Peppers",
        "Red Peppers",
        "Red Potatoes",
        "White Potatoes",
        "Gold Potatoes",
        "Pumpkins",
        "Radicchios",
        "Radishes",
        "Rutabagas",
        "Shallots",
        "Snow Peas",
        "Sorrels",
        "Squashes",
        "Spinaches",
        "Sweet Potatoes",
        "Swiss Chards",
        "Tomatillos",
        "Tomatoes",
        "Turnips",
        "Watercresses",
        "Zucchinis"
    ]
    return [name.lower() for name in names]

def collect_fruits_list():
    names = [
        "Apples",
        "Apricots",
        "Cucumbers",
        "Pears",
        "Avocados",
        "Bananas",
        "Cherries",
        "Crowberries",
        "Currents",
        "Blackberries",
        "Oranges",
        "Blueberries",
        "Boysenberries",
        "Breadfruits",
        "Figs",
        "Melons",
        "Cantaloupes",
        "Gooseberries",
        "Plums",
        "Carissas",
        "Grapes",
        "Cherimoyas",
        "Chokecherries",
        "Clementines",
        "Coconuts",
        "Grapes",
        "Dates",
        "Durians",
        "Elderberries",
        "Feijoas",
        "Kiwifruits",
        "Grapefruits",
        "Guavas",
        "Huckleberries",
        "Jackfruits",
        "Jambolans",
        "Jujubes",
        "Limes",
        "Kiwanos",
        "Kumquats",
        "Lemons",
        "Loganberries",
        "Longans",
        "Loquats",
        "Lychees",
        "Sapotes",
        "Mangos",
        "Mangosteens",
        "Papayas",
        "Medlars",
        "Mulberries",
        "Nectarines",
        "Passion Fruits",
        "Peaches",
        "Persimmons",
        "Pineapples",
        "Plantains",
        "Pomegrantes",
        "Pummelos",
        "Quinces",
        "Raisins",
        "Raspberries",
        "Salmonberries",
        "Sapodillas",
        "Sapotes",
        "Soursops",
        "Strawberries",
        "Coconuts",
        "Watermelons",
        "Blueberries"
    ]
    return [name.lower() for name in names]

def get_short_name(name):
    return name.split()[-1]

def get_frequencies(word_list):
    return [word_frequency(word, 'en') for word in word_list]

def get_probabilities(word_list):
    frequencies = get_frequencies(word_list)
    total_frequency = sum(frequencies)
    probabilities = [frequency / total_frequency for frequency in frequencies]
    return probabilities

def create_adjective_data_rows(adjectives_list):
    frequencies = get_frequencies(adjectives_list)
    probabilities = get_probabilities(adjectives_list)
    syllable_counts = [syllables.estimate(adjective) for adjective in
            adjectives_list]
    return zip(adjectives_list, frequencies, probabilities, syllable_counts)

def create_bird_data_rows(birds_list):
    short_names = [get_short_name(bird) for bird in birds_list]
    frequencies = get_frequencies(birds_list)
    probabilities = get_probabilities(birds_list)
    syllable_counts = [syllables.estimate(bird) for bird in birds_list]
    return zip(short_names, frequencies, probabilities, syllable_counts)

def create_veggie_data_rows(veggie_list):
    short_names = [get_short_name(veggie) for veggie in veggie_list]
    frequencies = get_frequencies(veggie_list)
    probabilities = get_probabilities(veggie_list)
    syllable_counts = [syllables.estimate(veggie) for veggie in veggie_list]
    return zip(short_names, frequencies, probabilities, syllable_counts)

def create_fruit_data_rows(fruit_list):
    short_names = [get_short_name(fruit) for fruit in fruit_list]
    frequencies = get_frequencies(fruit_list)
    probabilities = get_probabilities(fruit_list)
    syllable_counts = [syllables.estimate(fruit) for fruit in fruit_list]
    return zip(short_names, frequencies, probabilities, syllable_counts)

def collect_all_data(db_name="mascotgen.db"):
    adjectives = collect_adjectives_list()
    birds = collect_birds_list()
    veggies = collect_veggie_list()
    fruits = collect_fruits_list()

    connection = sqlite3.connect(db_name)
    with connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE adjectives
            (name text, frequency real, probability real, syllables integer)
            ''')
        cursor.execute('''
            CREATE TABLE birds
            (name text, frequency real, probability real, syllables integer)
            ''')
        cursor.execute('''
            CREATE TABLE veggies
            (name text, frequency real, probability real, syllables integer)
            ''')
        cursor.execute('''
            CREATE TABLE fruits
            (name text, frequency real, probability real, syllables integer)
            ''')

        adjective_data_rows = create_adjective_data_rows(adjectives)
        bird_data_rows = create_bird_data_rows(birds)
        veggie_data_rows = create_veggie_data_rows(veggies)
        fruit_data_rows = create_fruit_data_rows(fruits)

        cursor.executemany('INSERT INTO adjectives VALUES (?, ?, ?, ?)', adjective_data_rows)
        cursor.executemany('INSERT INTO birds VALUES (?, ?, ?, ?)', bird_data_rows)
        cursor.executemany('INSERT INTO veggies VALUES (?, ?, ?, ?)', veggie_data_rows)
        cursor.executemany('INSERT INTO fruits VALUES (?, ?, ?, ?)', fruit_data_rows)

'''
DATA COLLECTION
[Adjectives] WordNet -> Adjectives -> Frequencies -> Percentiles -> Syllables
[Birds] URL -> Birds (map Shorten) -> Frequencies -> Percentiles -> Syllables
[Vegetables] Manual -> Vegetables (map Shorten) -> Frequencies -> Percentiles
'''

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

PARAMETERS
adjective_frequency_percentile_range
noun_frequency_percentile_range
max_adjective_syllable_count
max_noun_syllable_count
max_total_syllable_count

TABLE
word | type | frequency | syllables | isComposite
'''
