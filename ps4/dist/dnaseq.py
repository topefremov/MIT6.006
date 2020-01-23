#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.t = {}
        for pair in pairs:
            self.put(pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        try:
            val = self.t[k]
            val.append(v)
        except KeyError:
            self.t[k] = [v]
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        try:
            return self.t[k]
        except KeyError:
            return []
            

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    
    try:
        subseq = ''
        while len(subseq) < k:
            subseq += seq.next()
        
        rh = RollingHash(subseq)
        pos = 0
        while True:
            yield (rh.current_hash(), (pos, subseq))
            c = seq.next()
            rh.slide(subseq[0], c)
            subseq = subseq[1:] + c
            pos += 1
    except StopIteration:
        return
    
    

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    cur = m
    for seqhash in subsequenceHashes(seq, k):
        if cur == m:
            cur = 1
            yield seqhash
        else:
            cur += 1    

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    seqdict = Multidict(intervalSubsequenceHashes(a, k, m))
    for bhash, (bpos, bseq) in subsequenceHashes(b, k):
        for apos, aseq in seqdict.get(bhash):
            if (aseq == bseq):
                yield (apos, bpos)
            else:
                continue
        
    

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
