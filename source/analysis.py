import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def compare_two_words(df, word1, word2):
    """
    Compare the occure of two words in the headlines over time
    """
    df[word1] = df['headline'].str.contains(word1, case=False)
    df[word2] = df['headline'].str.contains(word2, case=False)
    df['month'] = df['date'].dt.to_period('M')
    df.groupby('month')[word1].sum().plot()
    df.groupby('month')[word2].sum().plot()
    plt.title(f"Comparing {word1} and {word2}")
    plt.ylabel("Number of Headlines per month")
    plt.xlabel("Time")
    # add legend
    plt.legend([word1, word2])
    plt.show()


def compare_occurence(df, *words):
    """
    Compare the occurence of multiple words in the headlines over time
    """
    for word in words:
        df.loc[:,word] = df['headline'].str.contains(word, case=False)
    df.loc[:,'month'] = df['date'].dt.to_period('M')
    
    fig, ax = plt.subplots()
    for word in words:
        df.groupby('month')[word].sum().plot(ax=ax)
    plt.title(f"Comparing {', '.join(words)}")
    # labels
    plt.ylabel("Number of Headlines per month")
    plt.xlabel("Time")
    # add legend
    plt.legend(words)
    #plt.show()
    return fig, ax