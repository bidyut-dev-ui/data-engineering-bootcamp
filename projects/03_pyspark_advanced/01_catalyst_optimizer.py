#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 1: Catalyst Optimizer Deep Dive

This tutorial explores Spark's Catalyst Optimizer - the brain behind Spark SQL's performance.
Learn how Catalyst transforms logical plans into physical plans and optimizes your queries.

Key Concepts:
- Logical vs Physical Query Plans
- Predicate Pushdown
- Column Pruning
- Constant Folding
- Cost-Based Optimization

Optimized for 8GB RAM with local[2] execution.
"""

import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum as spark_sum, avg, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
import pandas as pd

def create_optimized_spark_session():
    """Create a SparkSession optimized for 8GB RAM"""
    return SparkSession.builder \
        .appName("Catalyst-Optimizer-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
        .getOrCreate()

def generate_sample_data(spark, num_rows=100000):
    """Generate sample transaction data for optimization exercises"""
    print(f"Generating {num_rows:,} sample transactions...")
    
    # Create schema for transaction data
    schema = StructType([
        StructField("transaction_id", StringType(), True),
        StructField("customer_id", StringType(), True),
        StructField("product_id", StringType(), True),
        StructField("category", StringType(), True),
        StructField("amount", DoubleType(), True),
        StructField("quantity", IntegerType(), True),
        StructField("transaction_date", StringType(), True),
        StructField("region", StringType(), True),
        StructField("discount_applied", DoubleType(), True),
        StructField("payment_method", StringType(), True)
    ])
    
    # Generate data using pandas for simplicity
    import numpy as np
    np.random.seed(42)
    
    data = {
        'transaction_id': [f'TX{i:08d}' for i in range(num_rows)],
        'customer_id': [f'CUST{np.random.randint(1000, 9999)}' for _ in range(num_rows)],
        'product_id': [f'PROD{np.random.randint(100, 999)}' for _ in range(num_rows)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], num_rows),
        'amount': np.random.uniform(10, 1000, num_rows).round(2),
        'quantity': np.random.randint(1, 10, num_rows),
        'transaction_date': pd.date_range('2024-01-01', periods=num_rows, freq='H').strftime('%Y-%m-%d').tolist(),
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_rows),
        'discount_applied': np.random.uniform(0, 0.3, num_rows).round(2),
        'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], num_rows)
    }
    
    pdf = pd.DataFrame(data)
    df = spark.createDataFrame(pdf, schema=schema)
    
    # Cache the DataFrame for reuse
    df.cache()
    df.count()  # Trigger caching
    
    print(f"Generated {df.count():,} transactions with {len(df.columns)} columns")
    return df

def demonstrate_query_plans(df):
    """Show different query plans and how Catalyst optimizes them"""
    print("\n" + "="*80)
    print("DEMONSTRATION 1: Query Plan Analysis")
    print("="*80)
    
    # Example 1: Simple filter query
    print("\n1. Simple Filter Query:")
    query1 = df.filter(col("amount") > 500).select("transaction_id", "customer_id", "amount")
    print("Logical Plan:")
    query1.explain(extended=True)  # Show logical plan
    
    # Example 2: Complex query with multiple operations
    print("\n2. Complex Aggregation Query:")
    query2 = df.filter(col("category") == "Electronics") \
               .filter(col("region") == "North") \
               .groupBy("customer_id") \
               .agg(
                   spark_sum("amount").alias("total_spent"),
                   avg("amount").alias("avg_transaction"),
                   count("*").alias("transaction_count")
               ) \
               .filter(col("total_spent") > 1000) \
               .orderBy(col("total_spent").desc())
    
    print("Optimized Physical Plan:")
    query2.explain()  # Show physical plan
    
    # Example 3: Show predicate pushdown
    print("\n3. Predicate Pushdown Demonstration:")
    # Create a Parquet file to demonstrate predicate pushdown
    df.write.mode("overwrite").parquet("/tmp/transactions_sample.parquet")
    
    # Read with filter - Catalyst pushes filter to scan
    parquet_df = spark.read.parquet("/tmp/transactions_sample.parquet")
    pushed_query = parquet_df.filter(col("amount") > 500).select("transaction_id", "amount")
    print("Plan with predicate pushdown (filter before scan):")
    pushed_query.explain()

def benchmark_optimizations(df):
    """Benchmark optimized vs non-optimized queries"""
    print("\n" + "="*80)
    print("DEMONSTRATION 2: Performance Benchmarking")
    print("="*80)
    
    # Non-optimized query: Multiple separate operations
    print("\n1. Non-optimized Query (Multiple separate filters):")
    start_time = time.time()
    
    result1 = df.filter(col("amount") > 500)
    result2 = result1.filter(col("category") == "Electronics")
    result3 = result2.filter(col("region") == "North")
    result4 = result3.select("transaction_id", "customer_id", "amount", "category")
    final_result = result4.groupBy("customer_id").agg(spark_sum("amount").alias("total"))
    
    non_opt_count = final_result.count()
    non_opt_time = time.time() - start_time
    print(f"Result count: {non_opt_count:,}")
    print(f"Execution time: {non_opt_time:.2f} seconds")
    
    # Optimized query: Combined operations
    print("\n2. Optimized Query (Combined operations):")
    start_time = time.time()
    
    optimized_result = df.filter((col("amount") > 500) & 
                                 (col("category") == "Electronics") & 
                                 (col("region") == "North")) \
                         .select("transaction_id", "customer_id", "amount", "category") \
                         .groupBy("customer_id").agg(spark_sum("amount").alias("total"))
    
    opt_count = optimized_result.count()
    opt_time = time.time() - start_time
    print(f"Result count: {opt_count:,}")
    print(f"Execution time: {opt_time:.2f} seconds")
    
    # Show performance improvement
    improvement = ((non_opt_time - opt_time) / non_opt_time) * 100
    print(f"\nPerformance Improvement: {improvement:.1f}% faster")
    
    # Show query plans comparison
    print("\nNon-optimized query plan:")
    final_result.explain()
    
    print("\nOptimized query plan:")
    optimized_result.explain()

def demonstrate_column_pruning(df):
    """Show how Catalyst prunes unused columns"""
    print("\n" + "="*80)
    print("DEMONSTRATION 3: Column Pruning")
    print("="*80)
    
    # Create a wide DataFrame with many columns
    print("Creating wide DataFrame with 20 columns...")
    
    # Add more columns to demonstrate pruning
    from pyspark.sql.functions import lit
    wide_df = df
    for i in range(10):
        wide_df = wide_df.withColumn(f"extra_col_{i}", lit(f"value_{i}"))
    
    print(f"Wide DataFrame has {len(wide_df.columns)} columns")
    
    # Query that only uses 3 columns - Catalyst should prune others
    print("\nQuery selecting only 3 columns:")
    pruned_query = wide_df.filter(col("amount") > 100) \
                          .select("transaction_id", "customer_id", "amount") \
                          .groupBy("customer_id").agg(spark_sum("amount").alias("total"))
    
    print("Query plan showing column pruning:")
    pruned_query.explain()
    
    # Compare with query that uses all columns
    print("\nQuery using all columns (no pruning):")
    full_query = wide_df.filter(col("amount") > 100) \
                        .groupBy("customer_id").agg(spark_sum("amount").alias("total"))
    
    print("Query plan without pruning:")
    full_query.explain()

def demonstrate_constant_folding():
    """Show constant folding optimization"""
    print("\n" + "="*80)
    print("DEMONSTRATION 4: Constant Folding")
    print("="*80)
    
    # Create a simple DataFrame
    data = [("A", 10), ("B", 20), ("C", 30)]
    schema = StructType([
        StructField("name", StringType(), True),
        StructField("value", IntegerType(), True)
    ])
    
    simple_df = spark.createDataFrame(data, schema)
    
    # Query with constant expressions
    print("Query with constant expressions (10 * 2 + 5):")
    folded_query = simple_df.select(
        col("name"),
        col("value"),
        (lit(10) * lit(2) + lit(5)).alias("constant_calc")
    )
    
    print("Query plan showing constant folding:")
    folded_query.explain()
    
    # Show that Catalyst computes the constant at compile time
    print("\nActual result:")
    folded_query.show()

def advanced_optimization_techniques(df):
    """Show advanced Catalyst optimization techniques"""
    print("\n" + "="*80)
    print("DEMONSTRATION 5: Advanced Optimization Techniques")
    print("="*80)
    
    # 1. Join reordering
    print("\n1. Join Reordering Optimization:")
    
    # Create two additional DataFrames for join demonstration
    customers_data = [
        ("CUST1001", "John Doe", "North", "Premium"),
        ("CUST1002", "Jane Smith", "South", "Standard"),
        ("CUST1003", "Bob Johnson", "East", "Premium"),
        ("CUST1004", "Alice Brown", "West", "Standard")
    ]
    
    customers_schema = StructType([
        StructField("customer_id", StringType(), True),
        StructField("customer_name", StringType(), True),
        StructField("region", StringType(), True),
        StructField("membership", StringType(), True)
    ])
    
    customers_df = spark.createDataFrame(customers_data, customers_schema)
    
    # Complex join query
    print("Complex join query with multiple tables:")
    join_query = df.alias("t") \
                   .join(customers_df.alias("c"), col("t.customer_id") == col("c.customer_id")) \
                   .filter(col("t.amount") > 100) \
                   .filter(col("c.membership") == "Premium") \
                   .select("t.transaction_id", "c.customer_name", "t.amount", "t.category")
    
    print("Join query plan (Catalyst may reorder joins):")
    join_query.explain()
    
    # 2. Subquery elimination
    print("\n2. Subquery Elimination:")
    
    # Create a subquery that Catalyst might eliminate
    subquery_df = df.filter(col("amount") > 500).select("customer_id", "amount")
    main_query = df.join(subquery_df, "customer_id") \
                   .groupBy("customer_id") \
                   .agg(spark_sum("amount").alias("total_amount"))
    
    print("Query with subquery (Catalyst may eliminate it):")
    main_query.explain()

def practical_exercises(df):
    """Provide hands-on exercises for learners"""
    print("\n" + "="*80)
    print("PRACTICAL EXERCISES")
    print("="*80)
    
    print("""
Exercise 1: Identify Optimization Opportunities
------------------------------------------------
1. Run the following query and examine its plan:
   df.filter(col("amount") > 100).filter(col("category") == "Electronics").filter(col("region") == "North")
   
2. Rewrite it as a single filter and compare execution plans.

Exercise 2: Column Pruning Analysis
------------------------------------------------
1. Create a query that selects only 2 out of 10 columns from a DataFrame.
2. Use explain() to verify that Catalyst pruned the unused columns.
3. Compare performance with a query that selects all columns.

Exercise 3: Join Optimization
------------------------------------------------
1. Create two DataFrames and join them with a filter on both sides.
2. Examine the join plan to see if Catalyst reordered the joins.
3. Try adding broadcast hint and compare performance.

Exercise 4: Constant Folding
------------------------------------------------
1. Create a query with complex constant expressions.
2. Use explain() to see if Catalyst folded the constants.
3. Verify by checking the physical plan.
""")

def main():
    """Main execution function"""
    print("="*80)
    print("ADVANCED PYSPARK: CATALYST OPTIMIZER DEEP DIVE")
    print("="*80)
    print("This tutorial explores Spark's Catalyst Optimizer internals.")
    print("All examples optimized for 8GB RAM systems.\n")
    
    # Initialize Spark
    global spark
    spark = create_optimized_spark_session()
    
    try:
        # Generate sample data
        df = generate_sample_data(spark, num_rows=50000)
        
        # Run demonstrations
        demonstrate_query_plans(df)
        benchmark_optimizations(df)
        demonstrate_column_pruning(df)
        demonstrate_constant_folding()
        advanced_optimization_techniques(df)
        practical_exercises(df)
        
        print("\n" + "="*80)
        print("TUTORIAL COMPLETE")
        print("="*80)
        print("Key Takeaways:")
        print("1. Catalyst transforms logical plans to optimized physical plans")
        print("2. Predicate pushdown reduces data scanned")
        print("3. Column pruning eliminates unused columns")
        print("4. Constant folding computes expressions at compile time")
        print("5. Join reordering improves performance")
        print("\nNext: Run 02_memory_management.py for memory optimization techniques")
        
    finally:
        # Cleanup
        spark.stop()
        print("\nSpark session stopped.")

if __name__ == "__main__":
    main()