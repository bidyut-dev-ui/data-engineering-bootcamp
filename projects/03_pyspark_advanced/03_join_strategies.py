#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 3: Join Strategies & Data Skew Handling

This tutorial covers PySpark join algorithms, optimization techniques, 
and handling data skew in resource-constrained environments.

Key Concepts:
- Broadcast Join vs Sort Merge Join
- Data Skew Detection and Mitigation
- Salting Techniques for Skewed Joins
- Bucketing for Join Optimization
- Adaptive Query Execution for Joins

Optimized for 8GB RAM with practical examples.
"""

import time
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, rand, when, lit, concat, sha2
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.sql import functions as F

def create_join_optimized_spark_session():
    """Create a SparkSession optimized for join operations on 8GB RAM"""
    return SparkSession.builder \
        .appName("Join-Strategies-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.autoBroadcastJoinThreshold", "10485760")  # 10MB \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.enabled", "true") \
        .config("spark.sql.adaptive.skewJoin.skewedPartitionFactor", "5") \
        .config("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB") \
        .getOrCreate()

def generate_skewed_datasets(spark):
    """Generate datasets with intentional skew for join demonstrations"""
    print("Generating datasets with controlled skew...")
    
    # Dataset 1: Transactions (large, moderately skewed)
    transactions_data = []
    for i in range(100000):
        # Create skew: 70% of transactions from top 10% customers
        if i < 70000:
            customer_id = f"CUST{np.random.randint(1, 100)}"  # Top 100 customers
        else:
            customer_id = f"CUST{np.random.randint(101, 1000)}"  # Remaining 900 customers
        
        transactions_data.append({
            "transaction_id": f"TX{i:08d}",
            "customer_id": customer_id,
            "amount": np.random.uniform(10, 1000),
            "product_id": f"PROD{np.random.randint(1, 100)}",
            "region": np.random.choice(["North", "South", "East", "West"])
        })
    
    transactions_schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("product_id", StringType(), True),
        StructField("region", StringType(), True)
    ])
    
    transactions_df = spark.createDataFrame(transactions_data, schema=transactions_schema)
    
    # Dataset 2: Customers (small, highly skewed for demonstration)
    customers_data = []
    # Create extreme skew: 80% of data in first 5 customers
    for i in range(1000):
        if i < 800:
            customer_id = f"CUST{np.random.randint(1, 6)}"  # First 5 customers
        else:
            customer_id = f"CUST{np.random.randint(6, 1000)}"
        
        customers_data.append({
            "customer_id": customer_id,
            "customer_name": f"Customer_{i}",
            "membership_tier": np.random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
            "join_date": f"2024-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}"
        })
    
    customers_schema = StructType([
        StructField("customer_id", StringType(), True),
        StructField("customer_name", StringType(), True),
        StructField("membership_tier", StringType(), True),
        StructField("join_date", StringType(), True)
    ])
    
    customers_df = spark.createDataFrame(customers_data, schema=customers_schema)
    
    # Dataset 3: Products (medium, uniform distribution)
    products_data = []
    for i in range(100):
        products_data.append({
            "product_id": f"PROD{i+1}",
            "product_name": f"Product_{i+1}",
            "category": np.random.choice(["Electronics", "Clothing", "Food", "Home", "Books"]),
            "price": np.random.uniform(5, 500)
        })
    
    products_schema = StructType([
        StructField("product_id", StringType(), True),
        StructField("product_name", StringType(), True),
        StructField("category", StringType(), True),
        StructField("price", DoubleType(), True)
    ])
    
    products_df = spark.createDataFrame(products_data, schema=products_schema)
    
    print(f"Generated datasets:")
    print(f"  Transactions: {transactions_df.count():,} rows")
    print(f"  Customers: {customers_df.count():,} rows")
    print(f"  Products: {products_df.count():,} rows")
    
    # Show skew statistics
    print("\nSkew Analysis:")
    cust_dist = customers_df.groupBy("customer_id").count().orderBy(col("count").desc())
    print("Top 10 customers by count:")
    cust_dist.show(10)
    
    return transactions_df, customers_df, products_df

def demonstrate_join_strategies(transactions_df, customers_df, products_df):
    """Compare different join strategies"""
    print("\n" + "="*80)
    print("JOIN STRATEGIES COMPARISON")
    print("="*80)
    
    # Clear cache for fair comparison
    spark.catalog.clearCache()
    
    # Strategy 1: Sort Merge Join (Default)
    print("\n1. Sort Merge Join (Default for large datasets):")
    start_time = time.time()
    
    sort_merge_result = transactions_df.alias("t") \
        .join(customers_df.alias("c"), "customer_id") \
        .join(products_df.alias("p"), "product_id") \
        .select("t.transaction_id", "c.customer_name", "p.product_name", "t.amount") \
        .filter(col("t.amount") > 100)
    
    sort_merge_count = sort_merge_result.count()
    sort_merge_time = time.time() - start_time
    
    print(f"Result count: {sort_merge_count:,}")
    print(f"Execution time: {sort_merge_time:.2f} seconds")
    print("Query plan:")
    sort_merge_result.explain()
    
    # Strategy 2: Broadcast Join (For small dimension tables)
    print("\n2. Broadcast Join (Products table is small):")
    start_time = time.time()
    
    # Hint Spark to broadcast products_df
    broadcast_result = transactions_df.alias("t") \
        .join(F.broadcast(products_df.alias("p")), "product_id") \
        .select("t.transaction_id", "p.product_name", "t.amount") \
        .filter(col("t.amount") > 100)
    
    broadcast_count = broadcast_result.count()
    broadcast_time = time.time() - start_time
    
    print(f"Result count: {broadcast_count:,}")
    print(f"Execution time: {broadcast_time:.2f} seconds")
    print(f"Improvement: {((sort_merge_time - broadcast_time)/sort_merge_time*100):.1f}% faster")
    print("Query plan (notice BroadcastHashJoin):")
    broadcast_result.explain()
    
    # Strategy 3: Bucket Join (Pre-partitioned tables)
    print("\n3. Bucketed Join (Simulated with repartition):")
    
    # Create bucketed versions (simulated with repartition)
    transactions_bucketed = transactions_df.repartition(4, "customer_id")
    customers_bucketed = customers_df.repartition(4, "customer_id")
    
    start_time = time.time()
    
    bucketed_result = transactions_bucketed.alias("t") \
        .join(customers_bucketed.alias("c"), "customer_id") \
        .select("t.transaction_id", "c.customer_name", "t.amount") \
        .filter(col("t.amount") > 100)
    
    bucketed_count = bucketed_result.count()
    bucketed_time = time.time() - start_time
    
    print(f"Result count: {bucketed_count:,}")
    print(f"Execution time: {bucketed_time:.2f} seconds")
    print("Query plan (notice Exchange hashpartitioning):")
    bucketed_result.explain()
    
    # Summary
    print("\n" + "-"*40)
    print("JOIN STRATEGY SUMMARY:")
    print(f"Sort Merge Join: {sort_merge_time:.2f}s")
    print(f"Broadcast Join:  {broadcast_time:.2f}s ({((sort_merge_time - broadcast_time)/sort_merge_time*100):.1f}% faster)")
    print(f"Bucketed Join:   {bucketed_time:.2f}s ({((sort_merge_time - bucketed_time)/sort_merge_time*100):.1f}% faster)")

def demonstrate_data_skew_handling(transactions_df, customers_df):
    """Show techniques for handling data skew"""
    print("\n" + "="*80)
    print("DATA SKEW HANDLING TECHNIQUES")
    print("="*80)
    
    # Analyze skew before handling
    print("\n1. Skew Detection:")
    skew_analysis = customers_df.groupBy("customer_id").count() \
        .agg(
            F.mean("count").alias("avg_count"),
            F.stddev("count").alias("std_count"),
            F.max("count").alias("max_count"),
            F.min("count").alias("min_count")
        )
    
    skew_stats = skew_analysis.collect()[0]
    print(f"Customer distribution statistics:")
    print(f"  Average count: {skew_stats['avg_count']:.1f}")
    print(f"  Std deviation: {skew_stats['std_count']:.1f}")
    print(f"  Max count: {skew_stats['max_count']}")
    print(f"  Min count: {skew_stats['min_count']}")
    print(f"  Skew ratio (max/avg): {skew_stats['max_count']/skew_stats['avg_count']:.1f}x")
    
    # Technique 1: Salting for Skewed Joins
    print("\n2. Salting Technique for Skewed Joins:")
    
    # Add salt to skewed key
    transactions_salted = transactions_df.withColumn(
        "customer_id_salted",
        concat(col("customer_id"), lit("_"), (rand() * 4).cast("int"))
    )
    
    customers_salted = customers_df.withColumn(
        "salt",
        F.array([lit(i) for i in range(4)])  # Create array of salt values
    ).select(
        col("customer_id"),
        col("customer_name"),
        col("membership_tier"),
        F.explode(col("salt")).alias("salt_id")
    ).withColumn(
        "customer_id_salted",
        concat(col("customer_id"), lit("_"), col("salt_id"))
    )
    
    print("Original join (with skew):")
    start_time = time.time()
    original_join = transactions_df.join(customers_df, "customer_id")
    original_count = original_join.count()
    original_time = time.time() - start_time
    print(f"Time: {original_time:.2f}s")
    
    print("\nSalted join (distributes skew):")
    start_time = time.time()
    salted_join = transactions_salted.join(customers_salted, "customer_id_salted")
    salted_count = salted_join.count()
    salted_time = time.time() - start_time
    print(f"Time: {salted_time:.2f}s")
    print(f"Improvement: {((original_time - salted_time)/original_time*100):.1f}% faster")
    
    # Technique 2: Adaptive Skew Join (Spark 3.0+)
    print("\n3. Adaptive Skew Join (Automatic):")
    print("""
Adaptive Query Execution (AQE) can automatically handle skew when:
- spark.sql.adaptive.enabled = true
- spark.sql.adaptive.skewJoin.enabled = true
- spark.sql.adaptive.skewJoin.skewedPartitionFactor > 1
- spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes is set

AQE detects skewed partitions at runtime and splits them.
""")
    
    # Enable AQE skew join and run query
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
    
    start_time = time.time()
    aqe_join = transactions_df.join(customers_df, "customer_id") \
        .groupBy("customer_id").agg(F.sum("amount").alias("total_spent"))
    aqe_count = aqe_join.count()
    aqe_time = time.time() - start_time
    
    print(f"AQE Skew Join time: {aqe_time:.2f}s")
    print("Check Spark UI for 'Skew Join' in SQL tab")
    
    # Reset config
    spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "false")

def demonstrate_join_optimization_tips():
    """Provide practical join optimization tips"""
    print("\n" + "="*80)
    print("JOIN OPTIMIZATION TIPS FOR 8GB RAM")
    print("="*80)
    
    print("""
1. **Choose the Right Join Strategy:**
   - Broadcast Join: When one table < 10MB
   - Sort Merge Join: Default for large tables
   - Shuffle Hash Join: Disabled by default in Spark 3.0+

2. **Handle Data Skew:**
   - Use salting for heavily skewed keys
   - Enable AQE skew join (Spark 3.0+)
   - Filter early to reduce skewed data
   - Consider breaking skewed keys into separate processing

3. **Optimize for 8GB RAM:**
   - Set spark.sql.autoBroadcastJoinThreshold = 10MB
   - Use spark.sql.shuffle.partitions = 4 (not default 200)
   - Cache dimension tables if reused
   - Use MEMORY_AND_DISK storage level for large joins

4. **Monitor Join Performance:**
   - Check Spark UI for shuffle size
   - Look for skewed partitions in task metrics
   - Monitor GC time during joins
   - Use df.explain() to see join type

5. **Avoid Common Pitfalls:**
   - Cartesian joins (cross join) without filters
   - Joining on non-equality conditions
   - Joining before filtering
   - Not caching reused broadcast tables
""")

def join_performance_exercises(transactions_df, customers_df, products_df):
    """Provide hands-on join optimization exercises"""
    print("\n" + "="*80)
    print("JOIN OPTIMIZATION EXERCISES")
    print("="*80)
    
    print("""
Exercise 1: Join Strategy Selection
------------------------------------------------
1. Join transactions_df (100K rows) with products_df (100 rows)
2. Try without hint - which join does Spark choose?
3. Force broadcast join with F.broadcast()
4. Compare execution times and plans

Exercise 2: Skew Detection and Mitigation
------------------------------------------------
1. Analyze customer distribution in customers_df
2. Identify the most skewed customer_id
3. Implement salting technique for the skewed join
4. Compare performance before/after salting

Exercise 3: Adaptive Query Execution
------------------------------------------------
1. Enable AQE skew join: spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
2. Run a join between transactions_df and customers_df
3. Check Spark UI for skew join indicators
4. Measure performance improvement

Exercise 4: Join Order Optimization
------------------------------------------------
1. Create a 3-way join: transactions_df → customers_df → products_df
2. Try different join orders
3. Use df.explain() to see join plan
4. Determine optimal join order for your data

Exercise 5: Bucketing for Join Optimization
------------------------------------------------
1. Repartition transactions_df and customers_df on customer_id
2. Create bucketed tables (simulate with repartition)
3. Compare join performance with/without bucketing
4. Check shuffle size reduction
""")

def main():
    """Main execution function"""
    print("="*80)
    print("ADVANCED PYSPARK: JOIN STRATEGIES & DATA SKEW HANDLING")
    print("="*80)
    print("This tutorial covers join optimization for 8GB RAM systems.")
    print("All examples use realistic skewed datasets.\n")
    
    # Initialize Spark
    global spark
    spark = create_join_optimized_spark_session()
    
    try:
        # Generate datasets with controlled skew
        transactions_df, customers_df, products_df = generate_skewed_datasets(spark)
        
        # Run demonstrations
        demonstrate_join_strategies(transactions_df, customers_df, products_df)
        demonstrate_data_skew_handling(transactions_df, customers_df)
        demonstrate_join_optimization_tips()
        join_performance_exercises(transactions_df, customers_df, products_df)
        
        print("\n" + "="*80)
        print("TUTORIAL COMPLETE")
        print("="*80)
        print("Key Takeaways:")
        print("1. Use broadcast join for small dimension tables (<10MB)")
        print("2. Implement salting for heavily skewed joins")
        print("3. Enable AQE for automatic skew handling")
        print("4. Monitor join performance in Spark UI")
        print("5. Choose join strategy based on data characteristics")
        print("\nNext: Run 04_ml_pipeline.py for PySpark MLlib tutorials")
        
    finally:
        # Cleanup
        spark.catalog.clearCache()
        spark.stop()
        print("\nSpark session stopped.")

if __name__ == "__main__":
    main()