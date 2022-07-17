from Applications import *
from collections import Counter

import re


@app.task
def generate_proxies_mapping(read_path_dir: str, output_file_path: str):
    files = os.listdir(read_path_dir)
    filtered_files = []
    for file in files:
        if ('[BUILD]' in file) or ('[LIVE]' in file):
            filtered_files.append(file)

    full_cards_list = []
    for read_file in filtered_files:
        filepath = os.path.join(read_path_dir, read_file)
        with open(filepath) as f:
            for i, line in enumerate(f):
                if i == 0 or i > 99:  # exclude commander and cards outside 100 count
                    continue
                try:    
                    match = re.search(r'\t(.*?)\n', line, re.DOTALL).group(1)
                    cleaned = match.replace('\t', '').strip(' ')
                    full_cards_list.append(cleaned)
                except:
                    continue

    count_cards = Counter(full_cards_list).most_common()

    with open(output_file_path, 'w+') as g:
        for unique_card in count_cards:
            g.write('{0:<40} {1:>25}\n'.format(*unique_card))
            exists_in_files = []
            for read_file in filtered_files:
                filepath = os.path.join(read_path_dir, read_file)
                with open(filepath) as f:
                    for i, line in enumerate(f):
                        if i == 0 or i > 99:  # exclude commander and cards outside 100 count
                            continue
                        try:
                            if unique_card[0] in line:
                                exists_in_files.append(read_file)
                                break
                        except:
                            continue
            for file in exists_in_files:
                g.write('\t\t{0}\n'.format(file))