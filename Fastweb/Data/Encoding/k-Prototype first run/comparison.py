import pandas as pd

# File names
file_2023 = "5_2023_urbanCategoryFound.csv"
file_2024 = "5_2024_urbanCategoryFound.csv"
file_cluster = "employee_cluster_assignment.csv"

# Read CSVs with the required encoding
df_2023 = pd.read_csv(file_2023, encoding="ISO-8859-1")
df_2024 = pd.read_csv(file_2024, encoding="ISO-8859-1")
df_cluster = pd.read_csv(file_cluster, encoding="ISO-8859-1")


def normalize_option(option):
    """
    Normalize text so it can safely become part of a column name.
    """
    option = str(option).strip().lower()
    option = option.replace(" ", "_")
    option = option.replace("/", "_")
    option = option.replace("-", "_")
    option = option.replace("'", "")
    option = option.replace('"', "")
    option = option.replace("(", "")
    option = option.replace(")", "")
    option = option.replace(",", "")
    option = option.replace(".", "")
    option = option.replace(":", "")
    option = option.replace(";", "")
    option = option.replace("&", "and")
    return option


def expand_choice_reason(df, year_suffix):
    """
    From a column like:
    economy^health^travel_time

    create binary columns like:
    choice_reason_2023_economy
    choice_reason_2023_health
    choice_reason_2023_travel_time
    """
    df = df.copy()

    # Replace NaN with empty string
    df["choice_reason"] = df["choice_reason"].fillna("").astype(str)

    # Extract unique options
    unique_options = set()
    for value in df["choice_reason"]:
        if value.strip() == "":
            continue
        parts = [x.strip() for x in value.split("^") if x.strip() != ""]
        unique_options.update(parts)

    unique_options = sorted(unique_options)

    # Create binary columns
    for option in unique_options:
        safe_option = normalize_option(option)
        col_name = f"choice_reason_{year_suffix}_{safe_option}"
        df[col_name] = df["choice_reason"].apply(
            lambda x: 1 if option in [p.strip() for p in str(x).split("^")] else 0
        )

    return df


# Expand choice_reason for 2023 and 2024
df_2023 = expand_choice_reason(df_2023, "2023")
df_2024 = expand_choice_reason(df_2024, "2024")

# Keep needed columns from 2023
cols_2023 = ["employee", "satisfaction_current_mode"] + \
            [col for col in df_2023.columns if col.startswith("choice_reason_2023_")]
df_2023 = df_2023[cols_2023].rename(
    columns={"satisfaction_current_mode": "satisfaction_current_mode_2023"}
)

# Keep needed columns from 2024
cols_2024 = ["employee", "satisfaction_current_mode"] + \
            [col for col in df_2024.columns if col.startswith("choice_reason_2024_")]
df_2024 = df_2024[cols_2024].rename(
    columns={"satisfaction_current_mode": "satisfaction_current_mode_2024"}
)

# Keep needed columns from cluster file
df_cluster = df_cluster[["employee", "main_mode2023", "main_mode2024", "cluster"]]

# Merge everything on employee
result = df_2023.merge(df_2024, on="employee", how="outer") \
                .merge(df_cluster, on="employee", how="outer")

# Save output to Excel
output_file = "post choice analysis.xlsx"
result.to_excel(output_file, index=False)

# Show first rows
print(result.head())
print(f"\nFile saved as: {output_file}")