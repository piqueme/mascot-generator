import sys
import xml.etree.ElementTree as ET
import requests

VEGETABLES = [
        'Amaranth Leaves',
        'Arrowroots',
        'Artichokes',
        'Arugulas',
        'Asparaguses',
        'Bamboo Shoots',
        'Green Beans',
        'Beets',
        'Endives',
        'Bitter Melons',
        'Broadbeans',
        'Broccolis',
        'Broccoli Rabes',
        'Brussel Sprouts',
        'Green Cabbages',
        'Red Cabbages',
        'Carrots',
        'Cassavas',
        'Cauliflowers',
        'Celeries',
        'Chayotes',
        'Chicories',
        'Collards',
        'Corns',
        'Crooknecks',
        'Cucumbers',
        'Daikons',
        'Dandelion Greens',
        'Edamames',
        'Eggplants',
        'Fennels',
        'Fiddleheads',
        'Gingers',
        'Horseradishes',
        'Jicamas',
        'Kales',
        'Kohlrabis',
        'Leeks',
        'Lettuces',
        'Mushrooms',
        'Mustard Greens',
        'Okras',
        'Red Onions',
        'Yellow Onions',
        'Parsnips',
        'Peas',
        'Green Peppers',
        'Red Peppers',
        'Red Potatoes',
        'White Potatoes',
        'Gold Potatoes',
        'Pumpkins',
        'Radicchios',
        'Radishes',
        'Rutabagas',
        'Shallots',
        'Snow Peas',
        'Sorrels',
        'Squashes',
        'Spinaches',
        'Sweet Potatoes',
        'Swiss Chards',
        'Tomatillos',
        'Tomatoes',
        'Turnips',
        'Watercresses',
        'Zucchinis'
    ]

FRUITS = [
        'Apples',
        'Apricots',
        'Cucumbers',
        'Pears',
        'Avocados',
        'Bananas',
        'Cherries',
        'Crowberries',
        'Currents',
        'Blackberries',
        'Oranges',
        'Blueberries',
        'Boysenberries',
        'Breadfruits',
        'Figs',
        'Melons',
        'Cantaloupes',
        'Gooseberries',
        'Plums',
        'Carissas',
        'Grapes',
        'Cherimoyas',
        'Chokecherries',
        'Clementines',
        'Coconuts',
        'Grapes',
        'Dates',
        'Durians',
        'Elderberries',
        'Feijoas',
        'Kiwifruits',
        'Grapefruits',
        'Guavas',
        'Huckleberries',
        'Jackfruits',
        'Jambolans',
        'Jujubes',
        'Limes',
        'Kiwanos',
        'Kumquats',
        'Lemons',
        'Loganberries',
        'Longans',
        'Loquats',
        'Lychees',
        'Sapotes',
        'Mangos',
        'Mangosteens',
        'Papayas',
        'Medlars',
        'Mulberries',
        'Nectarines',
        'Passion Fruits',
        'Peaches',
        'Persimmons',
        'Pineapples',
        'Plantains',
        'Pomegrantes',
        'Pummelos',
        'Quinces',
        'Raisins',
        'Raspberries',
        'Salmonberries',
        'Sapodillas',
        'Sapotes',
        'Soursops',
        'Strawberries',
        'Coconuts',
        'Watermelons',
        'Blueberries'
    ]

def fetch_birds_list():
    BIRDS_LIST_URL = 'http://www.worldbirdnames.org/master_ioc-names_xml.xml'
    birds_list_response = requests.get(BIRDS_LIST_URL)
    return birds_list_response.text

def parse_birds_list(birds_list_xml):
    root = ET.fromstring(birds_list_xml)
    species = root.findall('.//species/english_name')
    return [spec.text for spec in species]

def extract_bird_short_names(bird_species_list):
    short_names = [species_name.split()[-1] for species_name in bird_species_list]
    return sorted(set(short_names))

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


