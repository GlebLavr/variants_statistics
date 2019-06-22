import json 
from collections import defaultdict
import allel 
import sys

# vcf file import
callset = allel.read_vcf(sys.argv[1])

# variants count
variants_size = len(callset['variants/ALT'])

# DNA samples count
DNA_size = len(callset['samples'])

# dict, containing needed statistics
statistics_dict = defaultdict(int)
statistics_dict = {'Variants_count': variants_size,
                   'DNA_samples_count':DNA_size}

# writing to .json file
with open(sys.argv[2], 'w') as json_file:
    json.dump(statistics_dict, json_file)
