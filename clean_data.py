import pandas as pd
df=pd.read_csv("/content/pharmeasy_orders_raw.csv")
#Remove exact duplicate rows
before=len(df)
df=df.drop_duplicates().copy()
duplicates_removed=before-len(df)
print("Duplicates removed:", duplicates_removed)
print("Rows after duplicates:", len(df))
#Normalize Region column
df["region"]=df["region"].str.strip().str.title()
#Impute missing category using a product
product_category_lookup=(df.dropna(subset=["category"]).drop_duplicates(subset=["category"]).set_index("product")["category"].to_dict())
#Fill missing category
df["category"]=df["category"].fillna(df["product"].map(product_category_lookup))
#calculate profit margin for rows where profit is available
df["profit_margin"]=df["profit_inr"]/df["sales_inr"]
#Average profit margin for each category
category_mean_margin=(df.dropna(subset=["profit_margin"]).groupby("category")["profit_margin"].mean())
#Finding rows where profit is missing
missing_profit=df["profit_inr"].isna()
print("Missing profit rows:", missing_profit.sum())
df.loc[missing_profit, "profit_inr"] = (df.loc[missing_profit, "sales_inr"]* df.loc[missing_profit, "category"].map(category_mean_margin)).round(2)
#Remove temporary column
df=df.drop(columns=["profit_margin"])
#save the cleaned dataset
df.to_csv("orders_clean.csv",index=False)
print("clean dataset saved as orders_clean.csv")
print("Total number of rows:",len(df))
print("Total number of columns:",len(df.columns))
