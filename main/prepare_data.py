import pandas as pd
import os

INPUT_DIR = "/home/cc/.cache/kagglehub/datasets/davidalexander01/tpc-h-dataset/versions/1"
OUTPUT_DIR = "datasets/denorm"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"Membaca data dari: {INPUT_DIR}")

cols = {
    'part': ['P_PARTKEY', 'P_NAME', 'P_MFGR', 'P_BRAND', 'P_TYPE', 'P_SIZE', 'P_CONTAINER', 'P_RETAILPRICE', 'P_COMMENT'],
    'supplier': ['S_SUPPKEY', 'S_NAME', 'S_ADDRESS', 'S_NATIONKEY', 'S_PHONE', 'S_ACCTBAL', 'S_COMMENT'],
    'partsupp': ['PS_PARTKEY', 'PS_SUPPKEY', 'PS_AVAILQTY', 'PS_SUPPLYCOST', 'PS_COMMENT'],
    'customer': ['C_CUSTKEY', 'C_NAME', 'C_ADDRESS', 'C_NATIONKEY', 'C_PHONE', 'C_ACCTBAL', 'C_MKTSEGMENT', 'C_COMMENT'],
    'orders': ['O_ORDERKEY', 'O_CUSTKEY', 'O_ORDERSTATUS', 'O_TOTALPRICE', 'O_ORDERDATE', 'O_ORDERPRIORITY', 'O_CLERK', 'O_SHIPPRIORITY', 'O_COMMENT'],
    'lineitem': ['L_ORDERKEY', 'L_PARTKEY', 'L_SUPPKEY', 'L_LINENUMBER', 'L_QUANTITY', 'L_EXTENDEDPRICE', 'L_DISCOUNT', 'L_TAX', 'L_RETURNFLAG', 'L_LINESTATUS', 'L_SHIPDATE', 'L_COMMITDATE', 'L_RECEIPTDATE', 'L_SHIPINSTRUCT', 'L_SHIPMODE', 'L_COMMENT'],
    'nation': ['N_NATIONKEY', 'N_NAME', 'N_REGIONKEY', 'N_COMMENT'],
    'region': ['R_REGIONKEY', 'R_NAME', 'R_COMMENT']
}

def load_table(name):
    print(f"Loading {name}...")
    path = os.path.join(INPUT_DIR, f"{name}.tbl")
    return pd.read_csv(path, sep='|', names=cols[name], index_col=False, encoding='latin-1')

# 3. Load Table
lineitem = load_table('lineitem')
orders = load_table('orders')
customer = load_table('customer')
part = load_table('part')
supplier = load_table('supplier')
partsupp = load_table('partsupp')
nation = load_table('nation')
region = load_table('region')

print(" Start JOIN (Denorm)...")

df = lineitem.merge(orders, 
left_on='L_ORDERKEY', right_on='O_ORDERKEY')
df = df.merge(customer, 
left_on='O_CUSTKEY', right_on='C_CUSTKEY')
df = df.merge(partsupp, 
left_on=['L_PARTKEY', 'L_SUPPKEY'], 
right_on=['PS_PARTKEY', 'PS_SUPPKEY'])
df = df.merge(part, left_on='L_PARTKEY', 
right_on='P_PARTKEY')
df = df.merge(supplier, left_on='L_SUPPKEY', 
right_on='S_SUPPKEY')

nation_cust = nation.rename(columns={
    'N_NATIONKEY': 'N1_NATIONKEY', 
    'N_NAME': 'N1_NAME', 
    'N_REGIONKEY': 'N1_REGIONKEY'
})
region_cust = region.rename(columns={
    'R_REGIONKEY': 'R1_REGIONKEY', 
    'R_NAME': 'R1_NAME'
})

# Supplier (N2, R2) --
nation_supp = nation.rename(columns={
    'N_NATIONKEY': 'N2_NATIONKEY', 
    'N_NAME': 'N2_NAME', 
    'N_REGIONKEY': 'N2_REGIONKEY'
})
region_supp = region.rename(columns={
    'R_REGIONKEY': 'R2_REGIONKEY', 
    'R_NAME': 'R2_NAME'
})

# 6. Join Nation/Region Customer
df = df.merge(nation_cust, left_on='C_NATIONKEY', right_on='N1_NATIONKEY')
df = df.merge(region_cust, left_on='N1_REGIONKEY', right_on='R1_REGIONKEY')

# 7. Join Nation/Region Supplier
df = df.merge(nation_supp, left_on='S_NATIONKEY', right_on='N2_NATIONKEY')
df = df.merge(region_supp, left_on='N2_REGIONKEY', right_on='R2_REGIONKEY')

print(f"Selesai JOIN. Total baris: {len(df)}")
print("Menyimpan ke CSV...")

mid_point = len(df) // 2
df.iloc[:mid_point].to_csv(os.path.join(OUTPUT_DIR, 'part-0.csv'), index=False)
df.iloc[mid_point:].to_csv(os.path.join(OUTPUT_DIR, 'part-1.csv'), index=False)

print("Sukses! Data denormalisasi (part-0.csv, part-1.csv) siap digunakan.")
