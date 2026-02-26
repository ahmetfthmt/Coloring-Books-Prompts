import pandas as pd

try:
    df = pd.read_excel("d:/Çalışmalarım/Coloring Books Prompts/Coloring Books Prompts.xlsx")
    print("Column 1 (Unnamed: 1) Value Counts:")
    print(df.iloc[:, 1].value_counts().head())
    print("\nColumn 2 (Unnamed: 2) Value Counts:")
    print(df.iloc[:, 2].value_counts().head())
    
    print("\nSample Data:")
    print(df.head(5).to_string())
except Exception as e:
    print(f"Error: {e}")
