import pandas as pd
import json
import os

from toon_prompts import encode_table_to_toon

# Paths
INPUT_FILE = "Coloring Books Prompts.xlsx"
OUTPUT_TOON_FILE = "prompts_full.toon"
OUTPUT_JSON_FILE = "prompts_full.json"

def categorize_prompt(text):
    """Intelligently categorize prompts based on content"""
    text_lower = text.lower()
    
    categories = {
        'Animals': ['animal', 'dog', 'cat', 'kitten', 'bear', 'lion', 'zebra', 'elephant', 'giraffe', 
                    'monkey', 'parrot', 'snake', 'dinosaur', 'rabbit', 'squirrel', 'dragon', 'unicorn',
                    'fish', 'mermaid', 'sea creatures', 'wildlife', 'farm', 'safari', 'jungle', 'cow', 
                    'chicken', 'pig', 'bird', 'penguin', 'fox', 'wolf', 'shark', 'whale', 'pet'],
        'Fantasy & Magic': ['fairy', 'castle', 'dragon', 'unicorn', 'magic', 'mystical', 'wizard', 
                            'princess', 'prince', 'knight', 'enchanted'],
        'Nature & Landscape': ['forest', 'tree', 'flower', 'landscape', 'mountain', 'river', 'stream', 'ocean', 
                               'underwater', 'coral', 'seaweed', 'nature', 'park', 'garden', 'lake', 'beach'],
        'Vehicles': ['truck', 'car', 'ship', 'pirate ship', 'fire truck', 'spaceship', 'vehicle', 
                    'bulldozer', 'crane', 'cement mixer', 'construction', 'train', 'plane', 'boat', 'bicycle'],
        'Seasons & Weather': ['winter', 'summer', 'spring', 'fall', 'autumn', 'snow', 'snowman', 'snowflake', 
                             'ice', 'sun', 'rain', 'cloud', 'rainbow', 'season'],
        'Special Occasions': ['birthday', 'party', 'celebration', 'cake', 'candle', 'confetti', 'holiday', 
                             'christmas', 'halloween', 'easter'],
        'Space & Science': ['space', 'planet', 'astronaut', 'science', 'microbe', 'virus', 'microscope', 
                           'outer space', 'rocket', 'star', 'moon'],
        'People & Professions': ['firefighter', 'superhero', 'ballerina', 'dancer', 'pirate', 'doctor', 
                                'teacher', 'police', 'chef'],
        'Food & Treats': ['food', 'fruit', 'vegetable', 'ice cream', 'candy', 'cookie', 'pizza', 'dessert'],
        'Sports & Activities': ['sport', 'soccer', 'basketball', 'swimming', 'skating', 'skiing', 'playground'],
        'Indoor & Home': ['kitchen', 'playroom', 'toy', 'house', 'room', 'furniture'],
        'Art & Design': ['mandala', 'pattern', 'intricate', 'cityscape', 'graffiti', 'line art', 'geometric']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    return 'Other'

def clean_and_merge_prompts(df):
    """Clean data and merge continuation lines"""
    prompts = []
    current_prompt = ""
    
    for idx, row in df.iterrows():
        text = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""
        
        # Skip completely empty rows
        if not text:
            continue
            
        # If line is very short (< 50 chars), it's likely a continuation
        if len(text) < 50 and current_prompt:
            current_prompt += " " + text
        else:
            # Save previous prompt if exists and long enough
            if current_prompt and len(current_prompt) > 50:
                prompts.append(current_prompt)
            current_prompt = text
    
    # Don't forget the last prompt
    if current_prompt and len(current_prompt) > 50:
        prompts.append(current_prompt)
    
    return prompts

def process_all_sheets():
    try:
        print(f"Reading {INPUT_FILE}...")
        excel_file = pd.ExcelFile(INPUT_FILE)
        
        print(f"Found {len(excel_file.sheet_names)} sheets:")
        for sheet in excel_file.sheet_names:
            print(f"  - {sheet}")
        
        all_prompts = []
        
        for sheet_name in excel_file.sheet_names:
            print(f"\nProcessing sheet: {sheet_name}")
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            # Clean and merge prompts
            sheet_prompts = clean_and_merge_prompts(df)
            
            # Add category
            for prompt in sheet_prompts:
                all_prompts.append({
                    'text': prompt,
                    'category': categorize_prompt(prompt),
                    'sheet': sheet_name
                })
            
            print(f"  Extracted {len(sheet_prompts)} prompts")
        
        print(f"\n{'='*60}")
        print(f"TOTAL PROMPTS: {len(all_prompts)}")
        print(f"{'='*60}")
        
        # Category distribution
        category_counts = {}
        for p in all_prompts:
            cat = p['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print("\nCategory Distribution:")
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count}")
        
        # Save primary output as TOON
        toon_text = encode_table_to_toon(
            all_prompts,
            key="prompts",
            fields=("text", "category", "sheet"),
            delimiter="|",
            indent=2,
        )
        with open(OUTPUT_TOON_FILE, 'w', encoding='utf-8', newline='\n') as f:
            f.write(toon_text)

        print(f"\n✅ Successfully saved {len(all_prompts)} prompts to {OUTPUT_TOON_FILE}")

        # Legacy compatibility output
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_prompts, f, indent=2, ensure_ascii=False)
        print(f"✅ Legacy JSON compatibility file updated: {OUTPUT_JSON_FILE}")
        
        return all_prompts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    process_all_sheets()
