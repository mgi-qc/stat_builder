__author__ = 'Thomas Antonacci'
"""
Script to generate sheet with all rows from all results files found in work order directories in either the WGS or Exome directory.
"""


import argparse
import csv
import os
import glob
from datetime import datetime

mmddyy = datetime.now().strftime('%m%d%y')

# get argument, must have -wgs or -e flag
parser = argparse.ArgumentParser()
parser.add_argument('-e', help='Generate Exome stats file', action='store_true')
parser.add_argument('-wgs', help='Generate WGS stats file', action='store_true')
args = parser.parse_args()

# get dir script was run from
run_from = os.getcwd()

# Set stats file and working dir based on flags
if args.e:
    stat_file = 'cwl.exome.all.{}.tsv'.format(mmddyy)
    os.chdir('/gscmnt/gc2783/qc/GMSworkorders/Exome')
    print('Stats file in: \n/gscmnt/gc2783/qc/GMSworkorders/Exome/exomestats')
elif args.wgs:
    stat_file = 'cwl.WGS.all.{}.tsv'.format(mmddyy)
    os.chdir('/gscmnt/gc2783/qc/GMSworkorders/WGS')
    print('Stats file in: \n/gscmnt/gc2783/qc/GMSworkorders/WGS/wgsstats')
else:
    exit('Needs -wgs or -e argument; -h or --help for usage')

wo_list = []
results_files = []
# get list of results files if they exist

list_of_files = glob.glob('*/*.results.*.tsv')

# standard header from metrics parser
header_std = ['Admin','WorkOrder','date_QC','sample_name','common_name','model_name','last_succeeded_build',
              'data_directory','cram_file','status','ALIGNED_READS','mapped_rate','FOP: PF_MISMATCH_RATE',
              'SOP: PF_MISMATCH_RATE','FREEMIX','HAPLOID COVERAGE','PCT_10X','PCT_20X','PCT_30X','discordant_rate',
              'inter-chromosomal_Pairing rate','HET_SNP_Q','HET_SNP_SENSITIVITY','MEAN_COVERAGE','SD_COVERAGE',
              'MEAN_INSERT_SIZE','STANDARD_DEVIATION','PCT_ADAPTER','PF_READS','PF_ALIGNED_BASES','PERCENT_DUPLICATION',
              'TOTAL_READS','properly_paired-rate','PF_HQ_ALIGNED_Q20_BASE','PF_READS_ALIGNED','GENOME_TERRITORY',
              'SEQ_ID','BAIT_SET','GENOME_SIZE','BAIT_TERRITORY','TARGET_TERRITORY','BAIT_DESIGN_EFFICIENCY',
              'TOTAL_READS','PF_READS','PF_UNIQUE_READS','PCT_PF_READS','PCT_PF_UQ_READS','PF_UQ_READS_ALIGNED',
              'PCT_PF_UQ_READS_ALIGNED','PF_BASES_ALIGNED','PF_UQ_BASES_ALIGNED','ON_BAIT_BASES','NEAR_BAIT_BASES',
              'OFF_BAIT_BASES','ON_TARGET_BASES','PCT_SELECTED_BASES','PCT_OFF_BAIT','ON_BAIT_VS_SELECTED',
              'MEAN_BAIT_COVERAGE','MEAN_TARGET_COVERAGE','MEDIAN_TARGET_COVERAGE','MAX_TARGET_COVERAGE','PCT_USABLE_BASES_ON_BAIT',
              'PCT_USABLE_BASES_ON_TARGET','FOLD_ENRICHMENT','ZERO_CVG_TARGETS_PCT','PCT_EXC_DUPE','PCT_EXC_MAPQ',
              'PCT_EXC_BASEQ','PCT_EXC_OVERLAP','PCT_EXC_OFF_TARGET','FOLD_80_BASE_PENALTY','PCT_TARGET_BASES_1X',
              'PCT_TARGET_BASES_2X','PCT_TARGET_BASES_10X','PCT_TARGET_BASES_20X','PCT_TARGET_BASES_30X',
              'PCT_TARGET_BASES_40X','PCT_TARGET_BASES_50X','PCT_TARGET_BASES_100X','HS_LIBRARY_SIZE','HS_PENALTY_10X',
              'HS_PENALTY_20X','HS_PENALTY_30X','HS_PENALTY_40X','HS_PENALTY_50X','HS_PENALTY_100X','AT_DROPOUT','GC_DROPOUT',
              'HET_SNP_SENSITIVITY','HET_SNP_Q','SAMPLE','LIBRARY','READ_GROUP','QC_Status','QC_failed_metrics']

# Open results files and write rows to stats file if header is standard
with open(stat_file.format(mmddyy), 'w') as osf:
    osf_writer = csv.DictWriter(osf, fieldnames=header_std, delimiter='\t')
    osf_writer.writeheader()

    for file in list_of_files:
        with open(file, 'r') as rif:
            rif_reader = csv.DictReader(rif, delimiter='\t')
            header = rif_reader.fieldnames

            is_std_header = True
            for item in header_std:
                if is_std_header and item not in header:
                    is_std_header = False

            if is_std_header:
                for line in rif_reader:
                    osf_writer.writerow(line)

# move file to *stats directory:
if args.e:
    if not os.path.exists('exomestats'):
        os.mkdir('exomestats')
    os.rename(stat_file,'exomestats/' + stat_file)

if args.wgs:
    if not os.path.exists('wgsstats'):
        os.mkdir('wgsstats')
    os.rename(stat_file, 'wgsstats/' + stat_file)

os.chdir(run_from)
# Upload to smartsheet?
# statistics from sheet(s)?


