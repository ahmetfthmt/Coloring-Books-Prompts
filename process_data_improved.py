import pandas as pd
import json
import os
import re

# Paths
INPUT_FILE = "Coloring Books Prompts.xlsx"
OUTPUT_DIR = "js"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "data.js")

def categorize_prompt(text):
    """Intelligently categorize prompts based on content"""
    text_lower = text.lower()
    
    # Define category keywords
    categories = {
        'Animals': ['animal', 'dog', 'cat', 'kitten', 'bear', 'lion', 'zebra', 'elephant', 'giraffe', 
                    'monkey', 'parrot', 'snake', 'dinosaur', 'rabbit', 'squirrel', 'dragon', 'unicorn',
                    'fish', 'mermaid', 'sea creatures', 'wildlife', 'farm', 'safari', 'jungle', 'cow', 'chicken', 'pig'],
        'Fantasy & Magic': ['fairy', 'castle', 'dragon', 'unicorn', 'magic', 'mystical', 'mermaid', 'superhero'],
        'Nature & Landscape': ['forest', 'tree', 'flower', 'landscape', 'mountain', 'river', 'stream', 'ocean', 
                               'underwater', 'coral', 'seaweed', 'nature', 'park', 'garden', 'rv landscapes'],
        'Vehicles': ['truck', 'car', 'ship', 'pirate ship', 'fire truck', 'spaceship', 'vehicle', 
                    'bulldozer', 'crane', 'cement mixer', 'construction'],
        'Seasons & Weather': ['winter', 'summer', 'spring', 'fall', 'snow', 'snowman', 'snowflake', 
                             'ice', 'sun', 'rain', 'cloud'],
        'Special Occasions': ['birthday', 'party', 'celebration', 'cake', 'candle', 'confetti', 'holiday'],
        'Space & Science': ['space', 'planet', 'astronaut', 'science', 'microbe', 'virus', 'microscope', 'outer space'],
        'People & Professions': ['firefighter', 'superhero', 'ballerina', 'dancer', 'pirate'],
        'Indoor & Activities': ['kitchen', 'playroom', 'toy', 'ballet', 'dance', 'picnic', 'playground'],
        'Art & Design': ['mandala', 'pattern', 'intricate', 'cityscape', 'graffiti', 'line art']
    }
    
    # Check for matches
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    # Default category
    return 'Other'

def process_excel():
    try:
        print(f"Reading {INPUT_FILE}...")
        df = pd.read_excel(INPUT_FILE)
        
        # Select columns: 'Prompt' (column 0) only, ignore the original category column
        df_clean = df.iloc[:, [0]].copy()
        df_clean.columns = ['text']
        
        # Clean data
        df_clean = df_clean.dropna(subset=['text'])
        df_clean['text'] = df_clean['text'].astype(str).str.strip()
        
        # Remove very short entries (likely incomplete)
        df_clean = df_clean[df_clean['text'].str.len() > 10]
        
        # Apply intelligent categorization
        df_clean['category'] = df_clean['text'].apply(categorize_prompt)
        
        # Convert to dictionary list
        prompts = df_clean.to_dict(orient='records')
        
        # Print category distribution
        print("\nCategory Distribution:")
        for cat, count in df_clean['category'].value_counts().items():
            print(f"  {cat}: {count}")
        
        # Ensure directory exists
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        # Write to JS file
        js_content = f"const promptsData = {json.dumps(prompts, indent=2, ensure_ascii=False)};"
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        print(f"\nSuccessfully processed {len(prompts)} prompts to {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"Error processing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_excel()
