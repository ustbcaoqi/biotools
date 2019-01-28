# -*- coding: utf-8 -*-
"""
@aim: transform bed6 to bed12 according to the fourth column.
	blocks with the same fourth column couldn't overlap!
@usage: python3 bed6Tobed12.py file.bed(6) > file_new.bed(12)
=============================================================
@author: ustbcaoqi (Miki Cao)
@date: Jan 24, 2019
"""

import sys



bed_file = sys.argv[1]

# read file
with open(bed_file) as file:
	bed6 = file.readlines()


# put blocks with the same fourth column under the same key
my_dict = {}

for bed6_line in bed6:
	bed6_cols = bed6_line.split()

	if bed6_cols[3] not in my_dict.keys():
		my_dict[bed6_cols[3]] = [ bed6_line ]
	else:
		my_dict[bed6_cols[3]].append( bed6_line )


# for each gene, print one line, caontaining block informations.
for gene in sorted(my_dict.keys()):
	blocks = my_dict[gene]

	# split each block(block)
	block_start = []
	block_end = []
	for block in blocks:
		block_features = block.split()
		chrom = block_features[0]
		gene_id = block_features[3]
		strand = block_features[5]
		block_start.append( int(block_features[1]) )
		block_end.append( int(block_features[2]) )

	# sort block positions, blocks couldn't overlap!!!!
	block_start.sort()
	block_end.sort()

	# calculate length and relative start each block
	block_len = []
	block_rela_start = []
	for i in range(len(block_start)):
		block_len.append( block_end[i] - block_start[i] )
		block_rela_start.append( block_start[i] - block_start[0] )

	blocks_num = len(block_len)
	# print standard BED12 format
	print(chrom, block_start[0], block_end[-1], gene_id, '0', strand,
		block_start[0], block_end[-1], '255,0,0', blocks_num, sep='\t', end='\t')

	for i in range(blocks_num):
		print(block_len[i], end=',')

	print("\t", end='')

	for i in range(blocks_num):
		print(block_rela_start[i], end=',')

	print('')


