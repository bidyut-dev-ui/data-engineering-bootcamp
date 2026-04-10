#!/usr/bin/env python3
"""
Complete ETL Pipeline with PySpark

End-to-end data pipeline demonstrating:
1. Extract from multiple sources
2. Transform with business logic
3. Load to analytical format
4. Monitor and optimize for 8GB RAM
"""

import sys
import time
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum, avg, count, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

def create_etl_spark_session():
    """Create SparkSession optimized for ETL workloads."""
    
    return SparkSession.builder \
        .appName("ETL-Pipeline") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "8") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

def extract(spark):
    """Extract data from multiple sources."""
    
    print("\n" + "="*60)
    print("EXTRACT: Reading from multiple sources")
    print("="*60)
    
    # Source 1: Sales data (CSV)
    print("\n1. Reading sales data (CSV):")
    sales_schema = StructType([
        StructField("transaction_id", IntegerType(), True),
        StructField("customer_id", IntegerType(), True),
        StructField("product_id", IntegerType(), True),
        StructField("category", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("total_amount", DoubleType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("region", StringType(), True),
        StructField("payment_method", StringType(), True)
    ])
    
    sales_df = spark.read \
        .schema(sales_schema) \
        .option("header", "true") \
        .csv("data/sales_large.csv")
    
    print(f"   Rows: {sales_df.count():,}")
    print(f"   Size: {sales_df.rdd.getNumPartitions()} partitions")
    
    # Source 2: Customer data (CSV)
    print("\n2. Reading customer data (CSV):")
    customers_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("data/customers.csv")
    
    print(f"   Rows: {customers_df.count():,}")
    
    # Source 3: Product data (CSV) - small lookup table
    print("\n3. Reading product data (CSV):")
    products_df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv("data/products.csv")
    
    print(f"   Rows: {products_df.count():,}")
    
    return sales_df, customers_df, products_df

def transform(sales_df, customers_df, products_df):
    """Apply business transformations."""
    
    print("\n" + "="*60)
    print("TRANSFORM: Applying business logic")
    print("="*60)
    
    # 1. Data cleaning
    print("\n1. Data Cleaning:")
    
    # Remove null transactions
    initial_count = sales_df.count()
    sales_clean = sales_df.dropna(subset=["transaction_id", "customer_id", "total_amount"])
    cleaned_count = sales_clean.count()
    print(f"   Removed {initial_count - cleaned_count:,} rows with null values")
    
    # Remove negative amounts
    sales_clean = sales_clean.filter(col("total_amount") > 0)
    print(f"   Removed negative amounts: {sales_clean.count():,} rows remaining")
    
    # 2. Add derived columns
    print("\n2. Adding derived columns:")
    
    # Convert date string to date type
    from pyspark.sql.functions import to_date
    sales_with_date = sales_clean.withColumn(
        "transaction_date_parsed",
        to_date(col("transaction_date"), "yyyy-MM-dd")
    )
    
    # Extract date parts for partitioning
    sales_with_date = sales_with_date \
        .withColumn("transaction_year", year(col("transaction_date_parsed"))) \
        .withColumn("transaction_month", month(col("transaction_date_parsed"))) \
        .withColumn("transaction_day", dayofmonth(col("transaction_date_parsed")))
    
    # Add transaction size category
    sales_with_date = sales_with_date.withColumn(
        "transaction_size",
        when(col("total_amount") < 100, "Small")
        .when(col("total_amount") < 500, "Medium")
        .when(col("total_amount") < 1000, "Large")
        .otherwise("X-Large")
    )
    
    print("   Added: transaction_date_parsed, year, month, day, size_category")
    
    # 3. Join with dimension tables
    print("\n3. Joining with dimension tables:")
    
    # Broadcast join with products (small table)
    from pyspark.sql.functions import broadcast
    sales_with_products = sales_with_date.join(
        broadcast(products_df),
        "product_id",
        "left"
    )
    
    # Join with customers
    sales_enriched = sales_with_products.join(
        customers_df,
        "customer_id",
        "left"
    )
    
    print(f"   Enriched dataset: {sales_enriched.count():,} rows")
    print(f"   Columns: {len(sales_enriched.columns)}")
    
    # 4. Aggregations
    print("\n4. Creating aggregated views:")
    
    # Daily sales summary
    daily_summary = sales_enriched.groupBy(
        "transaction_date_parsed",
        "transaction_year",
        "transaction_month",
        "transaction_day"
    ).agg(
        count("*").alias("transaction_count"),
        sum("total_amount").alias("daily_revenue"),
        avg("total_amount").alias("avg_transaction_value"),
        countDistinct("customer_id").alias("unique_customers")
    ).orderBy("transaction_date_parsed")
    
    print(f"   Daily summary: {daily_summary.count():,} days")
    
    # Category performance
    category_performance = sales_enriched.groupBy("category").agg(
        count("*").alias("transaction_count"),
        sum("total_amount").alias("category_revenue"),
        avg("total_amount").alias("avg_transaction"),
        countDistinct("customer_id").alias("unique_customers")
    ).orderBy(col("category_revenue").desc())
    
    print(f"   Category performance: {category_performance.count()} categories")
    
    # Customer segmentation
    customer_segments = sales_enriched.groupBy("customer_id", "membership_tier").agg(
        count("*").alias("total_transactions"),
        sum("total_amount").alias("total_spent"),
        avg("total_amount").alias("avg_transaction_value"),
        countDistinct("category").alias("categories_purchased")
    ).orderBy(col("total_spent").desc())
    
    print(f"   Customer segments: {customer_segments.count():,} customers")
    
    return sales_enriched, daily_summary, category_performance, customer_segments

def load(spark, sales_enriched, daily_summary, category_performance, customer_segments):
    """Load transformed data to analytical storage."""
    
    print("\n" + "="*60)
    print("LOAD: Writing to analytical storage")
    print("="*60)
    
    output_base = "data/etl_output"
    
    # 1. Write enriched transactions (partitioned by date)
    print("\n1. Writing enriched transactions (partitioned by year/month):")
    transactions_path = f"{output_base}/transactions"
    
    sales_enriched.write \
        .partitionBy("transaction_year", "transaction_month") \
        .mode("overwrite") \
        .parquet(transactions_path)
    
    print(f"   Location: {transactions_path}")
    print("   Format: Parquet (columnar)")
    print("   Partitioned by: year, month")
    
    # 2. Write daily summary
    print("\n2. Writing daily summary:")
    daily_path = f"{output_base}/daily_summary"
    
    daily_summary.write \
        .mode("overwrite") \
        .parquet(daily_path)
    
    print(f"   Location: {daily_path}")
    print(f"   Rows: {daily_summary.count():,}")
    
    # 3. Write category performance
    print("\n3. Writing category performance:")
    category_path = f"{output_base}/category_performance"
    
    category_performance.write \
        .mode("overwrite") \
        .parquet(category_path)
    
    print(f"   Location: {category_path}")
    
    # 4. Write customer segments
    print("\n4. Writing customer segments:")
    customer_path = f"{output_base}/customer_segments"
    
    customer_segments.write \
        .mode("overwrite") \
        .parquet(customer_path)
    
    print(f"   Location: {customer_path}")
    print(f"   Rows: {customer_segments.count():,}")
    
    # 5. Create a summary report
    print("\n5. Creating summary report:")
    report_path = f"{output_base}/etl_report.txt"
    
    # Collect summary stats
    total_transactions = sales_enriched.count()
    total_revenue = sales_enriched.agg(sum("total_amount")).collect()[0][0]
    unique_customers = sales_enriched.select("customer_id").distinct().count()
    date_range = sales_enriched.agg(
        min("transaction_date_parsed").alias("start_date"),
        max("transaction_date_parsed").alias("end_date")
    ).collect()[0]
    
    # Write report
    with open(report_path, "w") as f:
        f.write("ETL Pipeline Summary Report\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total Transactions: {total_transactions:,}\n")
        f.write(f"Total Revenue: ${total_revenue:,.2f}\n")
        f.write(f"Unique Customers: {unique_customers:,}\n")
        f.write(f"Date Range: {date_range['start_date']} to {date_range['end_date']}\n")
        f.write(f"Output Location: {output_base}\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    print(f"   Report: {report_path}")
    
    return output_base

def validate_results(spark, output_base):
    """Validate ETL results."""
    
    print("\n" + "="*60)
    print("VALIDATE: Checking data quality")
    print("="*60)
    
    # Read back some data to verify
    transactions_path = f"{output_base}/transactions"
    
    if os.path.exists(transactions_path.replace("data/", "")):
        # Read a partition to verify
        sample_df = spark.read.parquet(transactions_path).limit(10)
        
        print("\n1. Sample of loaded data:")
        sample_df.select(
            "transaction_id", "customer_id", "category", 
            "total_amount", "transaction_date_parsed"
        ).show(5)
        
        # Check row counts match
        print("\n2. Data quality checks:")
        
        # Check for nulls in key columns
        null_check = sample_df.filter(
            col("transaction_id").isNull() | 
            col("customer_id").isNull() |
            col("total_amount").isNull()
        ).count()
        
        print(f"   Rows with null key values: {null_check}")
        
        # Check for negative amounts
        negative_check = sample_df.filter(col("total_amount") < 0).count()
        print(f"   Rows with negative amounts: {negative_check}")
        
        # Check date validity
        date_check = sample_df.filter(col("transaction_date_parsed").isNull()).count()
        print(f"   Rows with invalid dates: {date_check}")
        
        if null_check == 0 and negative_check == 0 and date_check == 0:
            print("\n   ✅ All data quality checks passed!")
        else:
            print("\n   ⚠️ Some data quality issues found")
    
    else:
        print("   Output directory not found for validation")

def monitor_performance(start_time):
    """Monitor ETL pipeline performance."""
    
    print("\n" + "="*60)
    print("PERFORMANCE: ETL Pipeline Metrics")
    print("="*60)
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = elapsed % 60
    
    print(f"\nTotal execution time: {minutes}m {seconds:.2f}s")
    print(f"Memory constraint: 8GB RAM (2GB driver, 1GB executor)")
    
    print("\nPerformance tips for 8GB RAM:")
    print("1. Use .cache() strategically for reused DataFrames")
    print("2. Broadcast small lookup tables (<10MB)")
    print("3. Write intermediate results to disk if needed")
    print("4. Monitor Spark UI at http://localhost:4040")
    print("5. Adjust spark.sql.shuffle.partitions based on data size")

def main():
    """Main ETL pipeline execution."""
    
    print("="*60)
    print("COMPLETE ETL PIPELINE WITH PYSPARK")
    print("="*60)
    print("\nRunning on 8GB RAM configuration")
    
    start_time = time.time()
    spark = create_etl_spark_session()
    
    try:
        # ETL Process
        print("\n" + "="*60)
        print("STARTING ETL PIPELINE")
        print("="*60)
        
        # Extract
        sales_df, customers_df, products_df = extract(spark)
        
        # Transform
        sales_enriched, daily_summary, category_performance, customer_segments = transform(
            sales_df, customers_df, products_df
        )
        
        # Load
        output_base = load(spark, sales_enriched, daily_summary, category_performance, customer_segments)
        
        # Validate
        validate_results(spark, output_base)
        
        # Monitor
        monitor_performance(start_time)
        
        # Success
        print("\n" + "="*60)
        print("✅ ETL PIPELINE COMPLETE!")
        print("="*60)
        
        print("\nOutput generated in:")
        print(f"  {output_base}/")
        print("  ├── transactions/ (partitioned Parquet)")
        print("  ├── daily_summary/ (aggregated metrics)")
        print("  ├── category_performance/ (business insights)")
        print("  ├── customer_segments/ (analytical views)")
        print("  └── etl_report.txt (summary)")
        
        print("\nSkills demonstrated:")
        print("1. Multi-source data extraction")
        print("2. Data cleaning and validation")
        print("3. Business logic transformations")
        print("4. Efficient joins (broadcast for small tables)")
        print("5. Partitioned storage for performance")
        print("6. Memory management on 8GB RAM")
        
        print("\nReady for production use!")
        print("Integrate with Airflow for scheduling (see projects/08_airflow_platform)")
        
    except Exception as e:
        print(f"\n❌ ETL PIPELINE FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    finally:
        # Clean up
        spark.stop()
        print("\nSpark session stopped. Memory freed.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())