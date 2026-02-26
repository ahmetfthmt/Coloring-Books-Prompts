import pandas as pd
import json
import os

# Paths
INPUT_FILE = "Coloring Books Prompts.xlsx"
OUTPUT_DIR = "js"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "data.js")

def process_excel():
    try:
        print(f"Reading {INPUT_FILE}...")
        df = pd.read_excel(INPUT_FILE)
        
        # Select columns: 'Prompt' and the 3rd column (index 2) for component/category
        # Rename columns for clarity. 
        # Note: Based on previous inspection, Column 0 is 'Prompt', Column 2 is likely Category/Tags
        
        # Let's double check column indices from previous inspection:
        # Columns: ['Prompt', 'Unnamed: 1', 'Unnamed: 2']
        
        df_clean = df.iloc[:, [0, 2]].copy()
        df_clean.columns = ['text', 'category']
        
        # Clean data
        df_clean = df_clean.dropna(subset=['text']) # Drop rows where prompt is missing
        df_clean['category'] = df_clean['category'].fillna('General') # Fill missing categories
        
        # Convert to dictionary list
        prompts = df_clean.to_dict(orient='records')
        
        # Ensure directory exists
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        # Write to JS file
        js_content = f"const promptsData = {json.dumps(prompts, indent=2)};"
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Successfully processed {len(prompts)} prompts to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error processing data: {e}")

if __name__ == "__main__":
    process_excel()
