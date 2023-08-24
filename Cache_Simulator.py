# 16 bit/2 byte word size 
#4096-byte cache



import random
import copy
from threading import Thread
import argparse


argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", help="name of cache data file you are passing in.")

filename = "crc_trace.txt"


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

    cache_hit = 0
    cache_miss = 0

    print("Clearing and Initiailzing Cache Lines...")

    for lines in range(0,32):
        cache_lines.append(0)

    with open(filename, "r") as command:
        command.readline() #Gets rid of the first line 
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[3],16)
            addr = int(file_line[2],16)
 
            index = (addr >> 5) & 0x1F
            #index = addr % 32
            tag = (addr >> 10) & 0x1F

            if (((cache_lines[index] & 0x7FFF0000) >> 16) == tag):
                #Cache Hit
                #print("Cache Hit at Cycle Count: " + str(cycle_count) + " and Index: " + str(index))
                if addr <= 65408 and addr >= 45056:
                    cache_hit += 1
            else:
                #Cache Miss
                #print("Cache Miss at Cycle Count: ", cycle_count)
                if addr <= 65408 and addr >= 45056:
                    cache_miss += 1
                cache_lines[index] = ((tag << 16) | data) | 0x80000000

    print("Number of Cache Hits for Direct Mapping: ", cache_hit)
    print("Number of Cache Misses for Direct Mapping: ", cache_miss)
    print("-------------------------------------------------------------")




def fullAssocative():
    cache_lines = []
    hit = False

    cache_hit = 0
    cache_miss = 0

    print("Clearing and Initiailzing Cache Lines...")

    for lines in range(0,32):
        cache_lines.append(0)

    with open(filename, "r") as command:
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
            #print("This is the addr " + str(addr))
            #print("This is the tag " + str(tag))

            for lines in cache_lines:
                    
                if ((lines & 0xFFFF0000) >> 16) == tag:
                    #print("This is the pulled tag from cache: " + str((lines & 0xFFFF0000) >> 16))
                    if addr <= 65408 and addr >= 45056:
                        cache_hit += 1
                    #print("Cache Hit at address: " +f"{addr:02x}"+ " Cycle: " + cycle_count)
                    hit = True
                    break

            if hit == True:
                hit = False
                continue
            if addr <= 65408 and addr >= 45056:
                cache_miss += 1
            for lines in cache_lines:
                if lines == 0:
                    lines = (tag << 16) | data
                    #print("Cache Miss Data Stored in empty cache line offset")
                    hit = True
                    break
                if hit == True:
                    hit = False
                continue
            ranline = random.randint(0,31)
            #print("Did not find a empty cache word...")
            #print("Writting to line " + str(ranline) )
            cache_lines[ranline] = (tag << 16) | data
            hit = False

    print("Number of Cache Hits for Fully Assocaitive: ", cache_hit)
    print("Number of Cache Misses for Fully Assocative: ", cache_miss)
    print("-------------------------------------------------------------")


def setSearch(cache_sets, tag, index):
    if (cache_sets[index] >> 16) == tag:
        return True
    else:
        return False



def fourWayAssocaitve():
    cache_ways = []
    cache_sets = []
    hit = False
    cache_hit = 0
    cache_miss = 0

    print("Clearing and Initiailzing Cache Lines...")
    for lines in range(0,8):
        cache_sets.append(0)
    cache_set0 = copy.deepcopy(cache_sets)
    cache_set1 = copy.deepcopy(cache_sets)
    cache_set2 = copy.deepcopy(cache_sets)
    cache_set3 = copy.deepcopy(cache_sets)

    cache_ways.append(cache_set0)
    cache_ways.append(cache_set1)
    cache_ways.append(cache_set2)
    cache_ways.append(cache_set3)

    print("Starting Four Way Assocaitive Sim please wait....")

    with open(filename, "r") as command:
        command.readline()         
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[3], 16)
            addr = int(file_line[2], 16)
            #print("This is the address used: ", addr)
            
            tag = (addr >> 6) & 0x3FF
            index = (addr >> 2) & 0x7
            #print("This is the tag used: ", tag)
            t0 = CacheThread(target=setSearch, args= (cache_ways[0],tag,index))
            t1 = CacheThread(target=setSearch, args=(cache_ways[1],tag,index))
            t2 = CacheThread(target=setSearch, args = (cache_ways[2],tag,index))
            t3 = CacheThread(target=setSearch , args = (cache_ways[3],tag,index))

            t0.start()
            t1.start()
            t2.start()
            t3.start()

            result0 = t0.join()
            result1 = t1.join()
            result2 = t2.join()
            result3 = t3.join()
            

            if result0:
                if addr <= 65408 and addr >= 45056:
                        cache_hit += 1
            elif result1:
                if addr <= 65408 and addr >= 45056:
                        cache_hit += 1
            elif result2:
                if addr <= 65408 and addr >= 45056:
                        cache_hit += 1
            elif result3:
                if addr <= 65408 and addr >= 45056:
                        cache_hit += 1
            else:
                if addr <= 65408 and addr >= 45056:
                    cache_miss += 1
                ranway = random.randint(0,3)
                tag_data = (tag << 16) | data
                cache_ways[ranway][index] = tag_data                             

    print("Number of Cache Hits for Four Way Assocaitive: ", cache_hit)
    print("Number of Cache Misses for Four Way Assocative: ", cache_miss)
    print("-------------------------------------------------------------")

                    





def main():

    print("""
   ______                __               ______    _                
 .' ___  |              [  |            .' ____ \  (_)               
/ .'   \_| ,--.   .---.  | |--.  .---.  | (___ \_| __   _ .--..--.   
| |       `'_\ : / /'`\] | .-. |/ /__\\  _.____`. [  | [ `.-. .-. |  
\ `.___.'\// | |,| \__.  | | | || \__., | \____) | | |  | | | | | |  
 `.____ .'\'-;__/'.___.'[___]|__]'.__.'  \______.'[___][___||__||__] 
                                                                     
""")
    print("Starting Direct Mapping now...")
    directMapping()
    print("Direct Mapping All Done")
    print("Starting Fully Assocative....")
    fullAssocative()
    print("Fully Assocative all done")
    print("4-Part Set Assocative is next...")
    fourWayAssocaitve()
    print("All Done")
if __name__ == '__main__':
    main()








