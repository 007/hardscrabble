# Hardscrabble

Scrabble / Wordscape / anagram solver based on prime factorization

## Wat?

`hardscrabble` (`/ˈhɑɹdˌskɹæbəl/`) - Involving hard work and struggle

## No, really, WTF?

This is an anagram solver based on prime factorization. Instead of trying to match words letter-by-letter, we can assign unique primes to each letter in our alphabet and find anagrams by doing division.

## How does that work?

I'll use `ABRACADABRA` as an example.  First we count letter frequency:

```
5 As
2 Bs
2 Rs
1 C
1 D
```

So we have a total of 5 letters in our alphabet. We assign primes to each letter, with the smallest primes going to the most frequent letters:

```
A = 2
B = 3
R = 5
C = 7
D = 11
```

_Note: You need to use the same set of primes for every word, so usually you want to do a frequency count for the entire dictionary and assign smallest prime to largest frequency across the board._

Next we do the math: for each letter in a word, multiply out its prime:

```
A   B   R   A   C   A   D    A   B   R   A
2   3   5   2   7   2   11   2   3   5   2

2 * 3 * 5 * 2 * 7 * 2 * 11 * 2 * 3 * 5 * 2 = 554,400
```

So we create a mapping where `554400` represents `ABRACADABRA`. Lather, rinse and repeat for all of our words to build a dictionary.

Now we want to find out if we can make `RADAR` from the letters in `ABRACADABRA`. Instead of sorting or scanning through all of the letters, we just do the same mapping for our candidate:

```
R   A   D    A   R
5   2   11   2   5

5 * 2 * 11 * 2 * 5 = 1,100
```
So we know that `RADAR` is `1100`. For every word in our dictionary, we divide the word value by `1100` and see if there's any remainder. If there isn't (if it divides evenly) then we know we have all of our letters in that word.

In our case, we try `554400 / 1100` and we get `504` and no remainder, so `RADAR` is an anagram of `ABRACADABRA`. The extra `504` is the set of remaining letters multiplied together.


## Is it good?

I haven't written the "simple" version to bench against it, but it's pretty fast.

Testing all words of 8 or fewer letters in SOWPODS takes under a minute on a 2017 MBP:

```
Hardest word is bumfluff with score of 21936944647909 and 45 bits
Found 10625955 matches

real	0m49.745s
user	2m43.153s
sys	0m11.863s
```

Even running non-parallel (factoring out `ne.evaluate`) is under 3 minutes:

```
$ time python ./prime-solver.py
Hardest word is bumfluff with score of 21936944647909 and 45 bits
Found 10625955 matches

real	2m23.500s
user	2m23.001s
sys	0m0.462s
```

