import numpy as np
from collections import defaultdict
from gdriveinterface import grab_soc_files, download_plaintext
import visualization

def wordcount(passages):
    freq_dict = defaultdict(int)
    for passage in passages:
        no_punctuation = filter(lambda x: x not in ",.?!", passage)
        split = no_punctuation.split(" ")

        for word in split:
            freq_dict[word.lower()] += 1

    return sum(freq_dict.values()), freq_dict

if __name__ == "__main__":
    files = grab_soc_files()
    passage = download_plaintext(files[0]['id'])
    count, freq_dict = wordcount([passage])
    print count
    print sorted(zip(freq_dict.keys(), freq_dict.values()), key=lambda x: x[1])
    visualization.word_frequency_plot(freq_dict)