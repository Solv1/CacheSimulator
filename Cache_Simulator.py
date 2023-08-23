# 16 bit/2 byte word size 
#4096-byte cache



import random
from threading import Thread
import argparse


argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", help="name of cache data file you are passing in.")


class CacheThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
    def run(self):
        if self._target != None:
            self._return = self._target(*self._args, **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def directMapping():
    cache_lines = []
    cache_line = 0

    print("Clearing and Initiailzing Cache Lines...")

    for lines in range(0,32):
        cache_lines.append(cache_line)

    with open("crc_trace.txt", "r") as command:
        command.readline() #Gets rid of the first line 
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[2],16)
            addr = int(file_line[3],16)
 
            #index = (addr >> 5) & 0x1F
            index = addr % 32
            tag = (addr >> 10) & 0x1F

            if ((cache_lines[index] & 0x7FFF0000) == tag):
                #Cache Hit
                print("Cache Hit at Cycle Count: " + str(cycle_count) + " and Index: " + str(index))
            else:
                #Cache Miss
                print("Cache Miss at Cycle Count: ", cycle_count)
                cache_lines[index] = ((tag << 16) | data) | 0x80000000



def fullAssocative():
    cache_lines = []
    cache_line = 0
    hit = False

    print("Clearing and Initiailzing Cache Lines...")

    for lines in range(0,32):
        cache_lines.append(cache_line)

    with open("crc_trace.txt", "r") as command:
        command.readline()         
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[3], 16)
            addr = int(file_line[2], 16)
            
            tag = (addr >> 8)
            print("This is the addr " + str(addr))
            print("This is the tag " + str(tag))

            for lines in cache_lines:
                    
                if ((lines & 0xFFFF0000) >> 16) == tag:
                    print("This is the pulled tag from cache: " + str((lines & 0xFFFF0000) >> 16))
                    
                    print("Cache Hit at address: " +f"{addr:02x}"+ " Cycle: " + cycle_count)
                    hit = True
                    break

            if hit == True:
                hit = False
                continue
            for lines in cache_lines:
                if lines == 0:
                    lines = (tag << 16) | data
                    print("Cache Miss Data Stored in empty cache line offset")
                    hit = True
                    break
                if hit == True:
                    hit = False
                continue
            ranline = random.randint(0,31)
            print("Did not find a empty cache word...")
            print("Writting to line " + str(ranline) )
            cache_lines[ranline] = (tag << 16) | data
            hit = False

def setSearch(cache_sets, tag, index):
    if (cache_sets[index] >> 16) == tag:
        return True
    else:
        return False



def fourWayAssocaitve():
    cache_ways = []
    cache_sets = []
    hit = False

    print("Clearing and Initiailzing Cache Lines...")
    for lines in range(0,8):
        cache_sets.append(0)

    for lines in range(0,4):
        cache_ways.append(cache_sets)

    with open("crc_trace.txt", "r") as command:
        command.readline()         
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[3], 16)
            addr = int(file_line[2], 16)
            print("This is the address used: ", addr)
            
            tag = (addr >> 6) & 0x3FF
            index = (addr >> 2) & 0x7
            print("This is the tag used: ", tag)
            t0 = CacheThread(target=setSearch, args= (cache_ways[0],tag,index))
            t1 = CacheThread(target=setSearch, args=(cache_ways[1],tag,index))
            t2 = CacheThread(target=setSearch, args = (cache_ways[2],tag,index))
            t3 = CacheThread(target=setSearch , args = (cache_ways[3],tag,index))

            t0.start()
            t1.start()
            t2.start()
            t3.start()

            result0 = t0.join()
            print(result0)
            result1 = t1.join()
            print(result1)
            result2 = t2.join()
            print(result2)
            result3 = t3.join()
            print(result3)

            if result0:
                print("Cache Hit in Way 1")
            elif result1:
                print("Cache Hit in Way 2")
            elif result2:
                print("Cache Hit in Way 3")
            elif result3:
                print("Cache Hit in Way 4")
            else:
                print("Cache Miss")
                ranway = random.randint(0,3)
                cache_ways[ranway][index] = (tag << 16) | data                                

                    





def main():

    #print("Starting Direct Mapping now...")
    #directMapping()
    #print("Direct Mapping All Done")
    #print("Starting Fully Assocative....")
    #fullAssocative()
    #print("Fully Assocative all done")
    print("4-Part Set Assocative is next...")
    fourWayAssocaitve()
    print("All Done")
if __name__ == '__main__':
    main()








