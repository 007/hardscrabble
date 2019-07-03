import gzip
import sys
from math import floor, sqrt

import numpy as np
import numexpr as ne

LONGEST_WORD = 8
LETTER_COUNT = 26

# do this the stupid way for now
def check_prime(x):
  for d in range(2, int(floor(sqrt(x))) + 1):
    if x % d == 0:
        return False
  return True

# get a set of primes for an alphabet
def get_letter_primes(alphabet_size=LETTER_COUNT):
    primes = []

    candidate = 3
    primes.append(2)
    prime_count = 1
    while prime_count < alphabet_size:
      if check_prime(candidate):
        prime_count += 1
        primes.append(candidate)
      candidate += 2
    return primes

# load a dictionary from file, filtering by word length
def load_dict(filename='test.txt.gz', max_len=LONGEST_WORD):
    dictionary = []
    with gzip.open(filename, 'rt') as fh:
        for line in fh:
            word = line.rstrip('\n').lower()
            if len(word) <= max_len and len(word) > 2:
                dictionary.append(word)
    return dictionary

# calcuate letter frequencies for all characters of all lines
def calculate_frequencies(d):
    freqs = {}
    for line in d:
        for letter in line:
            try:
                freqs[letter] += 1
            except KeyError:
                freqs[letter] = 1
    return freqs

# map a list of primes to a letter dictionary sorted by frequency
def freq_to_map(freq, primes):
    outmap = {}
    for f, p in zip(sorted(freq, key=freq.get, reverse=True), primes):
        outmap[f] = p
    return outmap

# map a word to a composite value letter-by-letter
def word_to_composite(letter_map, word):
    total = 1
    for l in word:
        total *= letter_map[l]
    return total

# map a dictionary to a list of values letter-by-letter
def dict_to_composite(letter_map, dictionary):
    mapped_words = []
    for word in dictionary:
        total = word_to_composite(letter_map, word)
        mapped_words.append((word, total))
    return mapped_words

def score_words(words, letter_mapping, candidates):
    # force candidates to be a list instead of str
    # list(list) and list(str) return the same result!
    candidates = list(candidates)
    # map it to a composite
    word = word_to_composite(letter_mapping, candidates)
    matches = ne.evaluate('word % words')

    # now that we've done the math, find where our words are evenly divisible
    end_words = np.nonzero(matches == 0)

    return end_words[0]


if __name__ == "__main__":
    primes = get_letter_primes()
    max_prime = primes[-1]

    max_check = max_prime ** LONGEST_WORD
    bits = max_check.bit_length()
    dictionary = load_dict()

    freq = calculate_frequencies(dictionary)
    prime_mapping = freq_to_map(freq, primes)

    all_words = dict_to_composite(prime_mapping, dictionary)

    # get highest-value word and its associated value
    (max_word,  max_value) = sorted(all_words, key=lambda t: t[1], reverse=True)[0]
    bits = max_value.bit_length()
    print("Hardest word is {} with score of {} and {} bits".format(max_word, max_value, bits))

    all_scores = np.array([ v[1] for v in all_words ])

    if len(sys.argv) > 1:
        word = sys.argv[1]
        matches = score_words(all_scores, prime_mapping, word)
        for e in matches:
            print(all_words[e][0])
    else:
        match_count = 0
        for w in dictionary:
            matches = score_words(all_scores, prime_mapping, w)
            match_count += len(matches)
        print("Found {} matches".format(match_count))
