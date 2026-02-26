"""
Automatic Prompt Translation Script
Translates all 1,965 prompts from English to Turkish
"""
import json
from deep_translator import GoogleTranslator
import time

from toon_prompts import parse_table_toon, encode_table_to_toon

INPUT_FILE = "prompts_full.toon"
OUTPUT_FILE = "prompts_bilingual.toon"

def translate_text(text, max_retries=3):
    """Translate English text to Turkish with retry logic"""
    translator = GoogleTranslator(source='en', target='tr')
    
    for attempt in range(max_retries):
        try:
            # Google Translate has a 5000 char limit
            if len(text) > 4500:
                # Split into chunks
                chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
                translated = ' '.join([translator.translate(chunk) for chunk in chunks])
            else:
                translated = translator.translate(text)
            return translated
        except Exception as e:
            print(f"  ⚠️ Translation error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retry
            else:
                return text  # Return original on final failure
    
    return text

def main():
    print("=" * 60)
    print("PROMPT TRANSLATION: English → Turkish")
    print("=" * 60)
    
    # Load prompts
    print(f"\n📖 Reading {INPUT_FILE}...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        prompts = parse_table_toon(
            f.read(),
            expected_key="prompts",
            expected_fields=("text", "category", "sheet"),
            strict=True,
        )
    
    print(f"✅ Loaded {len(prompts)} prompts")
    
    # Translate
    print("\n🔄 Starting translation...")
    translated_prompts = []
    
    for i, prompt in enumerate(prompts, 1):
        # Progress indicator
        if i % 50 == 0 or i == 1:
            print(f"  Progress: {i}/{len(prompts)} ({i/len(prompts)*100:.1f}%)")
        
        try:
            text_en = prompt['text']
            text_tr = translate_text(text_en)
            
            translated_prompts.append({
                'text_en': text_en,
                'text_tr': text_tr,
                'category': prompt['category'],
                'sheet': prompt.get('sheet', 'Unknown')
            })
            
            # Rate limiting - avoid overwhelming the API
            if i % 10 == 0:
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Translation interrupted by user!")
            print(f"Translated {len(translated_prompts)} out of {len(prompts)} prompts")
            user_input = input("Save progress? (y/n): ")
            if user_input.lower() == 'y':
                break
            else:
                return
        except Exception as e:
            print(f"\n❌ Error processing prompt {i}: {e}")
            # Keep original English as fallback
            translated_prompts.append({
                'text_en': prompt['text'],
                'text_tr': prompt['text'],  # Fallback to English
                'category': prompt['category'],
                'sheet': prompt.get('sheet', 'Unknown')
            })
    
    # Save
    print(f"\n💾 Saving {len(translated_prompts)} translated prompts to {OUTPUT_FILE}...")
    toon_text = encode_table_to_toon(
        translated_prompts,
        key="prompts_bilingual",
        fields=("text_en", "text_tr", "category", "sheet"),
        delimiter="|",
        indent=2,
    )
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        f.write(toon_text)
    
    print(f"✅ Successfully saved!")
    
    # Statistics
    print("\n" + "=" * 60)
    print("TRANSLATION COMPLETE")
    print("=" * 60)
    print(f"Total prompts: {len(translated_prompts)}")
    print(f"Output file: {OUTPUT_FILE}")
    
    # Sample translation
    if translated_prompts:
        print("\n📝 Sample translation:")
        sample = translated_prompts[0]
        print(f"  EN: {sample['text_en'][:100]}...")
        print(f"  TR: {sample['text_tr'][:100]}...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
