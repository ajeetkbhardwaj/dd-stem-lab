import pandas as pd
import numpy as np

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').drop_duplicates(subset=['date']).reset_index(drop=True)
    
    # Exclude random variables
    df = df.drop(columns=['rv1', 'rv2'], errors='ignore')
    return df
