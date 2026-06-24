import pandas as pd
from pathlib import Path

# =========================
# PATH SETUP
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales.csv"
OUTPUT_DIR = BASE_DIR / "output"

# Create output folder if missing
OUTPUT_DIR.mkdir(exist_ok=True)

# =========================
# EXTRACT
# =========================
df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print(df.shape)

# =========================
# DATA QUALITY CHECKS
# =========================
print("\nNull values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# Business validations
invalid_age = df[(df["age"] < 18) | (df["age"] > 100)]
print("Invalid age rows:", len(invalid_age))

invalid_rating = df[
    (df["customer_exp_rating"] < 1) |
    (df["customer_exp_rating"] > 5)
]
print("Invalid rating rows:", len(invalid_rating))

invalid_purchase = df[df["total_purchase"] < 0]
print("Negative purchase rows:", len(invalid_purchase))

# =========================
# TRANSFORMATION 1: AGE GROUP
# =========================
def get_age_group(age):
    if age <= 30:
        return "18-30"
    elif age <= 45:
        return "31-45"
    elif age <= 60:
        return "46-60"
    else:
        return "60+"


df["age_group"] = df["age"].apply(get_age_group)

print("\nAge Group Distribution:")
print(df["age_group"].value_counts())

# =========================
# ANALYSIS 1: AGE SUMMARY
# =========================
age_summary = (
    df.groupby("age_group")["total_purchase"]
    .sum()
    .sort_values(ascending=False)
)

print("\nAge Summary:")
print(age_summary)

# =========================
# ANALYSIS 2: PRODUCT SALES
# =========================
product_sales = (
    df.groupby("product_category")["total_purchase"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Product Categories by Sales:")
print(product_sales.head(5))

# Average purchase per category
avg_purchase = (
    df.groupby("product_category")["total_purchase"]
    .mean()
    .sort_values(ascending=False)
)

print("\nAverage Purchase by Category:")
print(avg_purchase.head(5))

# Order count per category
order_count = (
    df.groupby("product_category")["order_id"]
    .count()
    .sort_values(ascending=False)
)

print("\nOrder Count by Category:")
print(order_count.head(5))

# =========================
# TRANSFORMATION 2: NET REVENUE
# =========================
df["net_revenue"] = (
    df["total_purchase_after_discount"] - df["shipping_cost"]
)

print("\nNet Revenue Validation:")
print(
    df[
        [
            "product_category",
            "total_purchase_after_discount",
            "shipping_cost",
            "net_revenue",
        ]
    ].head(10)
)

# =========================
# ANALYSIS 3: PRODUCT NET REVENUE
# =========================
product_net_revenue = (
    df.groupby("product_category")["net_revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop Product Categories by Net Revenue:")
print(product_net_revenue.head(5))

# =========================
# LOAD CSV REPORTS
# =========================
print("\nSaving CSV reports...")

# optional sample instead of huge file
df.head(100).to_csv(
    OUTPUT_DIR / "cleaned_sales_sample.csv",
    index=False
)

age_summary.to_csv(OUTPUT_DIR / "age_summary.csv")
product_sales.to_csv(OUTPUT_DIR / "product_sales.csv")
product_net_revenue.to_csv(OUTPUT_DIR / "product_net_revenue.csv")

print("CSV reports saved successfully!")

# =========================
# EXCEL REPORT GENERATION
# =========================
print("\nGenerating Excel report...")

# Convert Series to DataFrame for cleaner Excel sheets
age_summary_df = age_summary.reset_index()
product_sales_df = product_sales.reset_index()
product_net_revenue_df = product_net_revenue.reset_index()

REPORT_PATH = OUTPUT_DIR / "sales_report.xlsx"

with pd.ExcelWriter(REPORT_PATH, engine="openpyxl") as writer:
    age_summary_df.to_excel(
        writer,
        sheet_name="Age Summary",
        index=False
    )

    product_sales_df.to_excel(
        writer,
        sheet_name="Product Sales",
        index=False
    )

    product_net_revenue_df.to_excel(
        writer,
        sheet_name="Net Revenue",
        index=False
    )

print("Excel report generated successfully!")
print("\nETL Pipeline completed successfully!")