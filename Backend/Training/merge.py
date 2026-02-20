import pandas as pd

styles_path = "styles.csv"
combined_path = "combined_metadata.csv"

print("Loading CSVs...")

styles = pd.read_csv(
    styles_path,
    on_bad_lines='skip',
    engine='python'
)

combined = pd.read_csv(
    combined_path,
    on_bad_lines='skip',
    engine='python'
)

print(f"Styles rows: {len(styles)}")
print(f"Combined rows: {len(combined)}")

# Ensure same dtype
styles["id"] = styles["id"].astype(str)
combined["id"] = combined["id"].astype(str)

# Merge useful columns
cols_to_add = [
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "usage"
]

merged = combined.merge(
    styles[["id"] + cols_to_add],
    on="id",
    how="left"
)

merged.to_csv("combined_metadata_enriched.csv", index=False)

print("Merge complete!")
