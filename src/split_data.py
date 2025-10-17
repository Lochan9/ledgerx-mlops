import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

def main():
    df = pd.read_csv("data/processed/sroie_cleaned.csv")
    df_ok = df[df["has_all"] == True]
    train, temp = train_test_split(df_ok, test_size=0.3, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    out_dir = Path("data/splits")
    out_dir.mkdir(parents=True, exist_ok=True)
    train.to_csv(out_dir/"train.csv", index=False)
    val.to_csv(out_dir/"val.csv", index=False)
    test.to_csv(out_dir/"test.csv", index=False)
    print("[OK] Train/Val/Test CSVs created in data/splits/")

if __name__ == "__main__":
    main()
