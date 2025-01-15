"""
Processing module for data
"""
import gender_guesser.detector as detector
from transformers import pipeline
import pandas as pd

def guess_gender(full_names):
    """
    """
    d = detector.Detector()
    # Process each name in the input list.
    genders = []  # Initialize an empty list to store the results.
    for name in full_names:
        # Handle "No author found" case.
        if name == "No author found":
            genders.append("No name provided")
            continue

        # Extract the first name.
        first_name = name.split()[0]

        # Predict gender using the detector.
        gender = d.get_gender(first_name)

        # Add the predicted gender to the list.
        genders.append(gender)

    # Step 5: Return the list of predicted genders.
    return genders

def process_gender_df(df):
    """
    Process the dataframe to add a 'gender' column by guessing the gender of names.
    """
    names = df["authors"].tolist()
    df["gender"] = guess_gender(names)
    return df
def process_sentiment_df(df):
    """
    Perform sentiment analysis on the headlines column of the DataFrame
    and add 'sentiment' and 'sentiment_score' columns.
    """
    # Step 1: Initialize the sentiment analysis pipeline.
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

    # Step 2: Apply sentiment analysis to each headline and extract results.
    sentiments = df["headline"].apply(lambda text: sentiment_pipeline(text)[0])

    # Step 3: Add sentiment results to the DataFrame.
    df["sentiment"] = sentiments.apply(lambda x: x["label"])
    df["sentiment_score"] = sentiments.apply(lambda x: x["score"])

    return df


if __name__ == "__main__":
    df = pd.read_csv("output/guardian_headlines_full.csv")
    df = process_gender_df(df)
    #df.to_csv("output/guardian_headlines_full_gender_processed.csv", index=False)
    df = process_sentiment_df(df)
    df.to_csv("output/guardian_headlines_full_processed.csv", index=False)