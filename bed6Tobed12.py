# -*- coding: utf-8 -*-
"""
@aim: transform bed6 to bed12 according to the fourth column.
	blocks with the same fourth column couldn't overlap!
@usage: bed6Tobed12.py file.bed(6) > file_new.bed(12)
@author: Miki Cao
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
	exons = my_dict[gene]

	# split each block(exon)
	exon_start = []
	exon_end = []
	for exon in exons:
		exon_features = exon.split()
		chrom = exon_features[0]
		gene_id = exon_features[3]
		strand = exon_features[5]
		exon_start.append( int(exon_features[1]) )
		exon_end.append( int(exon_features[2]) )

	# sort exon positions, exons couldn't overlap!!!!
	exon_start.sort()
	exon_end.sort()

	# calculate length and relative start each exon
	exon_len = []
	exon_rela_start = []
	for i in range(len(exon_start)):
		exon_len.append( exon_end[i] - exon_start[i] )
		exon_rela_start.append( exon_start[i] - exon_start[0] )

	# print standard BED12 format
	print(chrom, exon_start[0], exon_end[-1], gene_id, '0', strand,
		exon_start[0], exon_end[-1], '255,0,0', len(exon_start), sep='\t', end='\t')

	for i in range(len(exon_len)):
		print(exon_len[i], end='')
		if (i+1) != len(exon_len):
			print(',',end='')

	print("\t", end='')

	for i in range(len(exon_rela_start)):
		print(exon_rela_start[i], end='')
		if (i+1) != len(exon_rela_start):
			print(',',end='')

	print('')
