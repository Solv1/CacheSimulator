# 16 bit/2 byte word size 
#4096-byte cache




import argparse
import numpy as np

argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", help="name of cache data file you are passing in.")


def emptyCache(cache):
    cache = cache.clear()
    blankcache = np.uint16(0)

    for i in range(0,2047):
        cache.append(blankcache)

def directMapping(data, cache):

    numReads = 0
    numWrites = 0
    numCacheMiss = 0
    numCacheHits = 0

    for inst in data:

        rw = inst[1]
        addr = hex(inst[2])
        oldVal = hex(inst[3])
        newVal = hex(inst[4])

        if addr < 0xB000 or addr > 0xFF80:
            continue
        if rw == 'r':
            if cache[addr% 2047] != oldVal:
                numCacheMiss += 1
                numReads += 1
            else:
                numCacheHits += 1
                numReads += 1

        elif rw == 'w':
            cache[addr % 2047] = newVal
            numWrites += 1

        else:
            raise Exception  


def main():
    args = argparse.parse_args()
    filename = args.file

    #TODO: Handle File Input Parsing 

    cache = []

    emptyCache(cache)






