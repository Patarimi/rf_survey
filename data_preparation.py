import pandas as pd

if __name__ == "__main__":
    for techno in ["CMOS", "SiGe", "GaN", "GaAs", "InP", "LDMOS", "Others"]:
        data = pd.read_excel(io="data/raw/PA-Survey-v8.xlsx", sheet_name=techno, usecols="B:V")
        data.to_csv(f"data/cleaned/{techno}.csv")
