from math import floor, sqrt

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

def load_dict(filename='twl06.txt', max_len=100):
    dictionary = []
    with open(filename, 'r') as fh:
        for line in fh:
            word = line.rstrip('\n')
            if len(word) <= max_len:
                dictionary.append(word)
    return dictionary

def calculate_frequencies(d):
    freqs = {}
    for line in d:
        for letter in line:
            try:
                freqs[letter] += 1
            except KeyError:
                freqs[letter] = 1
    return freqs

# map a list of primes to a dictionary sorted by frequency
def freq_to_map(freq, primes):
    outmap = {}
    for f, p in zip(sorted(freq, key=freq.get, reverse=True), primes):
        outmap[f] = p
    return outmap

def dict_to_composite(symbol_map, dictionary):
    mapped_words = []
    for word in dictionary:
        total = 1
        for l in word:
            total *= symbol_map[l]
        mapped_words.append((word, total))
    return mapped_words

if __name__ == "__main__":

    primes = get_letter_primes()
    max_prime = primes[-1]

    max_check = max_prime ** LONGEST_WORD
    bits = max_check.bit_length()
    print ("highest of {} primes is {} and gives {} bits for max {}".format(len(primes), max_prime, bits, max_check))
    dictionary = load_dict('twl06.txt', LONGEST_WORD)
    print("one word is {}".format(dictionary[-1]))

    freq = calculate_frequencies(dictionary)
    prime_mapping = freq_to_map(freq, primes)
    print(prime_mapping)

    all_words = dict_to_composite(prime_mapping, dictionary)
    print(all_words[0])

    # get highest-value word and its associated value
    (max_word,  max_value) = sorted(all_words, key=lambda t: t[1], reverse=True)[0]
    bits = max_value.bit_length()
    print("Hardest word is {} with score of {} and {} bits".format(max_word, max_value, bits))
