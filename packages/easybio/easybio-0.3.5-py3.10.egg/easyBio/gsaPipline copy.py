from collections import defaultdict
import os
import pandas as pd

from easybio_conda.easyBio.Utils.gsaDownLoadUtils import gsaProject

from .runvelocyto import buildLoomFile

from .Utils import tidySummary, getProResults, sraMd5Cal
from .Utils import get_num_threads, calMd5

from .changeSRAName import renames1, renames2, renames3
from .Utils import check_file_exists, cellrangerRun, splitSRAfun, downLoadSRA, cellrangerRun2
import argparse
import re

inputName = "PRJCA014236"
# inputName = "HRA003747"

dirs = "/home/data/user/lei/SRAData/GSE"
fq_path = "/home/data/user/lei/SRAData/GSE/PRJCA014236/raw/fq"

gsap = gsaProject(inputName=inputName, dirs_path=dirs)
mapping = gsap.getFileMapping()
dirs_path = f"{dirs}/{inputName}"
raw_path = f"{dirs_path}/raw"
fq_path = f"{raw_path}/fq"

def rename_files(files, folder_path, mapping, srr_counts):
    name_add_mapping = {}
    name_add_srr_mapping = {}
    for file in files:
        srr_match = re.match(r'(HRR\d+)_[fr](\d)', file)
        if srr_match:
            srr, number = srr_match.groups()
            name = mapping[srr]
            read_type = ''
            if srr_counts[srr] == 2:
                read_type = 'R1' if number == '1' else 'R2'
            elif srr_counts[srr] == 3:
                read_type = 'I1' if number == '1' else (
                    'R1' if number == '2' else 'R2')

            if srr in name_add_srr_mapping:
                lane_number = name_add_srr_mapping[srr]
            else:
                name_add_mapping[name] = name_add_mapping.get(name, 0) + 1
                name_add_srr_mapping[srr] = name_add_mapping[name]
                lane_number = name_add_srr_mapping[srr]
            
            lane_number_str = ""
            if lane_number < 10:
                lane_number_str = f"00{lane_number}"
            elif lane_number < 100:
                lane_number_str = f"0{lane_number}"
            else:
                lane_number_str = f"{lane_number}"

            new_name = f"HRR{name}_S1_L{lane_number_str}_{read_type}_001.fastq.gz"
            # os.rename(os.path.join(folder_path, file),os.path.join(folder_path, new_name))
            print(f'Renamed {file} to {new_name}')

            



def renamegsa(gsap, folder_path):
    mapping = gsap.getFileMapping()
    files, srr_counts = count_hrr_occurrences(folder_path)
    rename_files(files, folder_path, mapping, srr_counts)


renamegsa(gsap, fq_path)



def main():
    num_threads = get_num_threads()
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process GSE number, directory and threads")
    parser.add_argument("-i", "--inputName", help="Project Number")
    parser.add_argument("-d", "--dirs", default=os.getcwd(),
                        help="Directory (default: current directory)")
    parser.add_argument("-t", "--threads", type=int, default=num_threads,
                        help="Number of threads (default: your cpucounts)")

    args = parser.parse_args()
    inputName = args.inputName
    dirs = args.dirs
    threads = args.threads

    gsap = gsaProject(inputName=inputName, dirs_path=dirs)
    gsap.downloadFiles(threads=threads)
    
    dirs_path = f"{dirs}/{inputName}"
    raw_path = f"{dirs_path}/raw"
    fq_path = f"{raw_path}/fq"
    renamegsa(gsap, fq_path)
    


