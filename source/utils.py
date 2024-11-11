"""
"""
import pandas as pd

def save_to_csv(df, filepath):
    """Save DataFrame to a CSV file."""
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
