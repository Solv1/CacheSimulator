# 16 bit/2 byte word size 
#4096-byte cache




import argparse
import numpy as np

argparse = argparse.ArgumentParser()
argparse.add_argument("-f", "--file", help="name of cache data file you are passing in.")



def directMapping():
    cache_lines = []
    cache_line = []

    print("Clearing and Initiailzing Cache Lines...")
    for data in range(0,32):
        cache_line.append(0)


    for lines in range(0,32):
        cache_lines.append(cache_line)

    with open("crc_trace.txt", "r") as command:
        command.readline() #Gets read of that pesky readline 
        for line in command:
            file_line = line.split(',')

            cycle_count = file_line[0]
            instr = file_line[1]
            if instr == 'w':
                continue
            data = int(file_line[2],16)
            addr = int(file_line[3],16)

            offset = addr & 0x1F 
            index = (addr >> 5) & 0x1F
            tag = (addr >> 10) & 0x1F
            valid = addr & 0x8000

            if (cache_lines[index][offset] & 0x80000000) and ((cache_lines[index][offset] & 0x7FFF0000) == tag):
                #Cache Hit
                print("Cache Hit at Cycle Count: ", cycle_count)
            else:
                #Cache Miss
                print("Cache Miss at Cycle Count: ", cycle_count)
                cache_lines[index][offset] = ((tag << 16) | data) | 0x80000000



def fullAssocative():

    






def main():

    print("Starting Direct Mapping now...")
    directMapping()
    print("Direct Mapping All Done")

if __name__ == '__main__':
    main()








