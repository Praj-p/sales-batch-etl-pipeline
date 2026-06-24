import pandas as pd
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales.csv"

df = pd.read_csv(DATA_PATH)
# ---------------- EXTRACT ----------------
#df = pd.read_csv(
 #   r"C:\Users\Ritesh\PycharmProjects\batch_etl_project\data\sales.csv"
#)

print("Rows:", len(df))
print("Columns:", len(df.columns))


# ---------------- TRANSFORM : DATA QUALITY CHECK ----------------
print("\nNull values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

invalid_age = df[(df["age"] < 18) | (df["age"] > 100)]
print("Invalid age rows:", len(invalid_age))

invalid_rating = df[
    (df["customer_exp_rating"] < 1) |
    (df["customer_exp_rating"] > 5)
]
print("Invalid rating rows:", len(invalid_rating))

invalid_purchase = df[df["total_purchase"] < 0]
print("Negative purchase rows:", len(invalid_purchase))


# ---------------- TRANSFORM : AGE GROUP ----------------
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

print("\nAge Group Count:")
print(df["age_group"].value_counts())


# ---------------- ANALYSIS 1 : AGE GROUP SALES ----------------
age_summary = (
    df.groupby("age_group")["total_purchase"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTotal Purchase by Age Group:")
print(age_summary)


# ---------------- ANALYSIS 2 : PRODUCT CATEGORY SALES ----------------
product_sales = (
    df.groupby("product_category")["total_purchase"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTotal Sales by Product Category:")
print(product_sales.head(5))


# ---------------- ANALYSIS 3 : AVG PURCHASE ----------------
avg_purchase = (
    df.groupby("product_category")["total_purchase"]
      .mean()
      .sort_values(ascending=False)
)

print("\nAverage Purchase by Category:")
print(avg_purchase.head(5))


# ---------------- ANALYSIS 4 : ORDER COUNT ----------------
order_count = (
    df.groupby("product_category")["order_id"]
      .count()
      .sort_values(ascending=False)
)

print("\nOrder Count by Category:")
print(order_count.head(5))


# ---------------- TRANSFORMATION : NET REVENUE ----------------
df["net_revenue"] = (
    df["total_purchase_after_discount"] - df["shipping_cost"]
)

print(
    df[
        [
            "product_category",
            "total_purchase_after_discount",
            "shipping_cost",
            "net_revenue"
        ]
    ].head(10)
)


# ---------------- ANALYSIS : PRODUCT NET REVENUE ----------------
product_net_revenue = (
    df.groupby("product_category")["net_revenue"]
      .sum()
      .sort_values(ascending=False)
)

print("\nTop Product Categories by Net Revenue:")
print(product_net_revenue.head(5))

# ---------------- LOAD ----------------
print("\nSaving files...")

OUTPUT_DIR = BASE_DIR / "output"

#df.to_csv(OUTPUT_DIR / "cleaned_sales.csv", index=False)
df.head(100).to_csv(OUTPUT_DIR / "cleaned_sales_sample.csv", index=False)
age_summary.to_csv(OUTPUT_DIR /"age_summary.csv")
product_sales.to_csv(OUTPUT_DIR /"product_sales.csv")
product_net_revenue.to_csv(OUTPUT_DIR /"product_net_revenue.csv")

print("Files saved successfully!")