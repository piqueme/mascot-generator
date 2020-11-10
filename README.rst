************************
Simple Mascot Generator
************************

#########
Overview
#########

This is a dead simple **mascot generator**.
It creates mascots by randomly combining adjectives and nouns.
Some options are provided for guiding the generation:

1. Limit the number of syllables in adjectives, nouns, or total
2. Pick from different types of mascots: birds, fruits, veggies...
3. Control the "rarety" of adjectives and nouns

#############
Install
#############
For the time being, we're not distributing over PyPI and instead opting for installation through
Github and the developer's environment::

    git clone https://www.github.com/piqueme/mascot-generator
    cd mascot-generator
    pip install
    python mascot_generator/cli.py collect

For safety, you may want to install into a `virtual Python environment
<https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments>`.

The last line will create the SQLite DB that the generator command uses to create example mascots
quickly.

#############
Usage
#############
It's a command line tool!::

    cd mascot-generator
    python mascot_generator/cli.py gen birds

This will generate a single bird mascot.
There are a number of command line flags::

    cd mascot-generator
    python mascot_generator/cli.py gen veggies -n 2 -A 0.1 0.2 -c 3

This will generate 3 veggie mascots with at most 2 syllables in the noun part, and only using
the veggies that are between the 10th and 20th percentiles for popularity (pretty rare veggies!).

You can see a full list of command line options::

    python mascot_generator/cli.py --help

#############
How it works
#############
1. Collects adjectives from *WordNet*
2. Collects birds from a live government-maintained bird list over the net
3. Fruits and vegetables are hardcoded lists
4. Word probabilities are determined using a community 1-gram distribution
5. Syllable counts are provided using a simple algorithm looking at vowel-consonant shifts
6. Words are mapped to filter data (probabilities, syllables) and stored in SQLite
