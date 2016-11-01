import numpy as np
import matplotlib.pyplot as plt

def word_frequency_plot(freq_dict, top_n=10):
    ignore_words = ["the", "a", "and", "i", "of", "in", "to", "is", "as", "my",
                    'i\xe2\x80\x99m']
    ordered = sorted(freq_dict, key=lambda x: freq_dict[x])[::-1]
    cleaned = filter(lambda x: x not in ignore_words, ordered)

    index = np.arange(top_n)

    plt.bar(index, [freq_dict[x] for x in cleaned[:top_n]], .35)
    plt.xticks(index, cleaned[:top_n], rotation=90)
    plt.show()


