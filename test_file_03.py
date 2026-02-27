import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from utils.extractor import extract_from_file
import glob
import os

all_files = glob.glob('EXPERIMENT DATA/*.xlsx')
f = [f for f in all_files if '03_Master' in f][0]
print("Testing File 03: " + os.path.basename(f))

records, err = extract_from_file(f, exp_id=888)
if err:
    print("Error: " + str(err))
else:
    nitro = [r for r in records if r['parameter'] == 'HPS_Nitrogen']
    print("Found " + str(len(nitro)) + " Nitrogen records")
    if nitro:
        print("First 3 values:")
        for r in nitro[:3]:
            print("  Day " + str(r['day']) + " = " + str(r['value']))
    
    # Check HPS_API too
    api = [r for r in records if r['parameter'] == 'HPS_API']
    print("Found " + str(len(api)) + " HPS_API records")
