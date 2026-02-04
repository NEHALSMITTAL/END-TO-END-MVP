Retail Insights & Loyalty Program Analytics
This repository contains a comprehensive dataset and analysis of retail operations, focusing on the intersection of store performance, customer loyalty, and promotional effectiveness.






main dataset-
Row ID => Unique ID for each row.
Order ID => Unique Order ID for each Customer.
Order Date => Order Date of the product.
Ship Date => Shipping Date of the Product.
Ship Mode=> Shipping Mode specified by the Customer.
Customer ID => Unique ID to identify each Customer.
Customer Name => Name of the Customer.
Segment => The segment where the Customer belongs.
Country => Country of residence of the Customer.
City => City of residence of of the Customer.
State => State of residence of the Customer.
Postal Code => Postal Code of every Customer.
Region => Region where the Customer belong.
Product ID => Unique ID of the Product.
Category => Category of the product ordered.
Sub-Category => Sub-Category of the product ordered.
Product Name => Name of the Product
Sales => Sales of the Product.
Quantity => Quantity of the Product.
Discount => Discount provided.
Profit => Profit/Loss incurred.



ulter dataset-


We will use 6 main entities:

CUSTOMERS
PRODUCTS
STORES (Location)
ORDERS (Transaction Header)
ORDER_ITEMS (Line Items)
PROMOTIONS (Optional)

 CUSTOMER_DETAILS

PK: customer_id

customer_name

segment

country

city

state

postal_code

region

STORE_SALES_HEADER (ORDERS)

PK: order_id
FK: customer_id, store_id

order_date

ship_date

ship_mode

 STORE_SALES_LINE_ITEMS

PK: line_item_id
FK: order_id, product_id, promotion_id (optional)

quantity

sales

discount

profit

 PRODUCTS

PK: product_id

product_name

category

sub_category
 STORES

PK: store_id

city

state

region

country
 PROMOTIONS (optional)

PK: promotion_id

discount_percentage




ER
CUSTOMERS ──< ORDERS >── STORES
               |
               |
           ORDER_ITEMS
           /         \
      PRODUCTS     PROMOTIONS


flow -
Raw Dataset (CSV)
      |
      ▼
Data Cleaning & Normalization
(Split into 6 logical tables)
      |
      ▼
Feature Engineering Layer
(RFM + behavior features)
      |
      ▼
Target Builder
(Next 30-day spend)
      |
      ▼
ML Model Training
      |
      ▼
Model Evaluation
      |
      ▼
Saved Model + Preprocessing
      |
      ▼
Inference API / UI



cleaning-
Raw CSV
   ↓
Schema Validation
   ↓
Null Handling
   ↓
Duplicate Removal
   ↓
Outlier Treatment
   ↓
Standardization
   ↓
Normalized Tables
