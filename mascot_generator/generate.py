import random
import sqlite3

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
        generated_mascot = None
        generate_trials = 0
        while generated_mascot is None and generate_trials < 20:
            random_adjective = adjectives[random.randrange(0, len(adjectives))]
            random_noun = nouns[random.randrange(0, len(nouns))]
            if random_adjective[3] + random_noun[3] <= max_total_syllable_count:
                generated_mascot = random_adjective[0] + ' ' + random_noun[0]
            generate_trials += 1
        return generated_mascot

