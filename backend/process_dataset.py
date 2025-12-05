"""
Script to process Women's Clothing E-Commerce Reviews dataset.

This script:
1. Removes specified columns (Clothing ID, Recommended IND, Rating)
2. Filters rows where Review Text > 100 chars and Title is not null
3. Categorizes age into groups (Youth, Early Adult, Mid Adult, Late Adult, Senior)
"""

import pandas as pd
import sys
from pathlib import Path


def categorize_age(age):
    """Categorize age into predefined groups."""
    if pd.isna(age):
        return None
    if age < 30:
        return "Youth"
    elif 30 <= age <= 44:
        return "Early Adult"
    elif 45 <= age <= 59:
        return "Mid Adult"
    elif 60 <= age <= 74:
        return "Late Adult"
    elif 75 <= age <= 90:
        return "Senior"
    else:
        return None  # Ages outside the defined ranges


def process_dataset(input_path, output_path):
    """Process the dataset according to specifications."""
    
    print(f"Loading dataset from: {input_path}")
    df = pd.read_csv(input_path)
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Step 1: Remove specified columns
    columns_to_remove = ['Clothing ID', 'Recommended IND', 'Rating']
    existing_columns_to_remove = [col for col in columns_to_remove if col in df.columns]
    
    if existing_columns_to_remove:
        df = df.drop(columns=existing_columns_to_remove)
        print(f"\nRemoved columns: {existing_columns_to_remove}")
    else:
        print(f"\nWarning: None of the columns to remove were found in the dataset")
    
    # Step 2: Filter rows
    # Filter for Review Text > 100 characters and non-null Title
    
    df = df[df['Title'].notna()]  # Remove null Review Text first
    df = df[df['Review Text'].str.len() < 100]
        
    df['Age Category'] = df['Age'].apply(categorize_age)
    
    # Step 3: Randomly sample 150 rows
    if len(df) >= 150:
        df = df.sample(n=170, random_state=42)
        print(f"\nRandomly sampled 150 rows")
    else:
        print(f"\nWarning: Only {len(df)} rows available, using all")
    
    # Calculate total characters
    total_chars = 0
    for col in df.columns:
        total_chars += df[col].astype(str).str.len().sum()
    
    print(f"Total characters in dataset: {total_chars:,}")
    
    # Save processed dataset
    df.to_csv(output_path, index=False)
    print(f"\nProcessed dataset saved to: {output_path}")
    
    return df


def main():
    """Main function to run the processing script."""
    
    # Allow command-line arguments or use script directory defaults
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        # Default: look in backend/data/ directory
        script_dir = Path(__file__).parent
        input_path = str(script_dir / "data" / "Womens Clothing E-Commerce Reviews.csv")
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    else:
        # Default: save to backend/data/
        script_dir = Path(__file__).parent
        output_path = str(script_dir / "data" / "processed_reviews.csv")
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        process_dataset(input_path, output_path)
        print("\n✓ Processing completed successfully!")
    except Exception as e:
        print(f"\n✗ Error during processing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
