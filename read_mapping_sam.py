#!/usr/bin/env python
"""
This takes a sam file and list of contigs, and writes the coordinates of reads
for which both paired reads map to the same contig.
"""

import sys
import re

if len(sys.argv) != 4:
    print "Usage: ./read_mapping_sam.py <sam file> <list of target scaffolds>\
           <outfile>\n"
    quit()

sam = open(sys.argv[1], "r")
sequences = open(sys.argv[2], "r")

# Reads the list of contigs into a set
scaffolds = set([])
for line in sequences:
    header = line.strip()
    scaffolds.add(header)

length_dict = {}
read_dict = {}
used_reads = set([])
out = open(sys.argv[3], "w")
out.write("Scaffold\tScaffold length\tFirst read position\tSecond read\
           position\n")

# Reads the sam file and writes the mapping coordinates if the read pair both
# maps to the same contig and that contig is in the target list
for line in sam:
    if line.startswith("@SQ"):
        regex = re.match(".*?SN:(.*?)\tLN:(\d+)\n", line)
        contig = regex.group(1)
        length = regex.group(2)
        if contig in scaffolds:
            length_dict[contig] = length
    elif line.startswith("@PG") or line.startswith("@HD"):
        pass
    else:
        regex = re.match("(.*?)\t(\d+)\t(.*?)\t(\d+)\t.*?\t.*?\t(.*?)\t\
                          (\d+)\t.*?\n", line)
        read = regex.group(1)
        mapped_contig = regex.group(3)
        position = regex.group(4)
        pair = regex.group(5)
        pair_position = regex.group(6)
        if (mapped_contig in scaffolds and pair == "=" and
                read not in used_reads):
            out.write("%s\t%s\t%s\t%s\n" % (mapped_contig,
                                            length_dict[mapped_contig],
                                            position, pair_position))
            used_reads.add(read)
