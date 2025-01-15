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


def sentiment_analysis(data):
    """
    Perform sentiment analysis on the given text
    """
    # Perform sentiment analysis using a pre-trained model
    # This is a placeholder function and should be replaced with actual sentiment analysis code
    sentiment_pipeline = pipeline("sentiment-analysis")
    sentiment_dict = sentiment_pipeline(data)
    return sentiment_dict 

def process_sentiment_df(df):
    """
    """
    sentiment_dict = df["headline"].apply(sentiment_analysis)
    df["sentiment"] = sentiment_dict['label']
    df["sentiment_score"] = sentiment_dict['score']

    return df


if __name__ == "__main__":
    df = pd.read_csv("output/guardian_headlines_full.csv")
    df = process_gender_df(df)
    df.to_csv("output/guardian_headlines_full_gender_processed.csv", index=False)
    df = process_sentiment_df(df)
    df.to_csv("output/guardian_headlines_full_fully_processed.csv", index=False)