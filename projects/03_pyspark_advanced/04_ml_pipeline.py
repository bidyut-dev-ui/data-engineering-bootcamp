#!/usr/bin/env python3
"""
Advanced PySpark Tutorial 4: ML Pipelines with MLlib on 8GB RAM

This tutorial covers PySpark MLlib for machine learning on resource-constrained
environments, comparing with scikit-learn and optimizing for 8GB RAM.

Key Concepts:
- PySpark MLlib vs scikit-learn comparison
- Feature engineering with PySpark transformers
- ML pipeline construction and evaluation
- Cross-validation and hyperparameter tuning
- Model serialization and deployment

Optimized for 8GB RAM with practical ML examples.
"""

import time
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, rand
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType
from pyspark.ml.feature import VectorAssembler, StringIndexer, OneHotEncoder, StandardScaler
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, GBTClassifier
from pyspark.ml.regression import LinearRegression, RandomForestRegressor
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator, RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml import Pipeline
import sklearn
from sklearn.ensemble import RandomForestClassifier as SklearnRF
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

def create_ml_optimized_spark_session():
    """Create a SparkSession optimized for ML workloads on 8GB RAM"""
    return SparkSession.builder \
        .appName("ML-Pipeline-Tutorial") \
        .master("local[2]") \
        .config("spark.driver.memory", "2g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.ml.evaluation.metric", "f1") \
        .getOrCreate()

def generate_ml_datasets(spark, num_samples=50000):
    """Generate classification and regression datasets for ML examples"""
    print(f"Generating ML datasets with {num_samples:,} samples...")
    
    # Classification dataset: Customer churn prediction
    np.random.seed(42)
    
    classification_data = []
    for i in range(num_samples):
        # Features
        age = np.random.randint(18, 80)
        tenure = np.random.randint(0, 60)  # months
        monthly_charges = np.random.uniform(20, 120)
        total_charges = monthly_charges * tenure
        contract_type = np.random.choice(["Month-to-month", "One year", "Two year"])
        payment_method = np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"])
        
        # Create target with some logic
        churn_prob = 0.3
        if contract_type == "Month-to-month":
            churn_prob += 0.3
        if payment_method == "Electronic check":
            churn_prob += 0.1
        if monthly_charges > 80:
            churn_prob += 0.2
        if tenure < 12:
            churn_prob += 0.2
        
        churn = 1 if np.random.random() < churn_prob else 0
        
        classification_data.append({
            "customer_id": f"CUST{i:06d}",
            "age": age,
            "tenure": tenure,
            "monthly_charges": round(monthly_charges, 2),
            "total_charges": round(total_charges, 2),
            "contract_type": contract_type,
            "payment_method": payment_method,
            "churn": churn
        })
    
    classification_schema = StructType([
        StructField("customer_id", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("tenure", IntegerType(), True),
        StructField("monthly_charges", DoubleType(), True),
        StructField("total_charges", DoubleType(), True),
        StructField("contract_type", StringType(), True),
        StructField("payment_method", StringType(), True),
        StructField("churn", IntegerType(), True)
    ])
    
    classification_df = spark.createDataFrame(classification_data, schema=classification_schema)
    
    # Regression dataset: House price prediction
    regression_data = []
    for i in range(num_samples):
        # Features
        square_footage = np.random.randint(800, 4000)
        bedrooms = np.random.randint(1, 6)
        bathrooms = np.random.randint(1, 4)
        year_built = np.random.randint(1950, 2023)
        location_zone = np.random.choice(["A", "B", "C", "D"])
        
        # Price calculation with some noise
        base_price = 100000
        price = (base_price + 
                 square_footage * 150 +
                 bedrooms * 50000 +
                 bathrooms * 30000 +
                 (2023 - year_built) * -1000)
        
        if location_zone == "A":
            price *= 1.5
        elif location_zone == "B":
            price *= 1.2
        elif location_zone == "C":
            price *= 1.0
        else:
            price *= 0.8
        
        # Add noise
        price *= np.random.uniform(0.9, 1.1)
        price = round(price, 2)
        
        regression_data.append({
            "house_id": f"HOUSE{i:06d}",
            "square_footage": square_footage,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "year_built": year_built,
            "location_zone": location_zone,
            "price": price
        })
    
    regression_schema = StructType([
        StructField("house_id", StringType(), True),
        StructField("square_footage", IntegerType(), True),
        StructField("bedrooms", IntegerType(), True),
        StructField("bathrooms", IntegerType(), True),
        StructField("year_built", IntegerType(), True),
        StructField("location_zone", StringType(), True),
        StructField("price", DoubleType(), True)
    ])
    
    regression_df = spark.createDataFrame(regression_data, schema=regression_schema)
    
    print(f"Generated datasets:")
    print(f"  Classification: {classification_df.count():,} samples (churn prediction)")
    print(f"  Regression: {regression_df.count():,} samples (house price prediction)")
    
    # Show class distribution
    churn_dist = classification_df.groupBy("churn").count().orderBy("churn")
    print("\nChurn distribution:")
    churn_dist.show()
    
    return classification_df, regression_df

def demonstrate_feature_engineering(classification_df):
    """Show PySpark feature engineering techniques"""
    print("\n" + "="*80)
    print("FEATURE ENGINEERING WITH PYSPARK MLIB")
    print("="*80)
    
    # Split data
    train_df, test_df = classification_df.randomSplit([0.8, 0.2], seed=42)
    print(f"Training set: {train_df.count():,} samples")
    print(f"Test set: {test_df.count():,} samples")
    
    # Step 1: String indexing for categorical features
    print("\n1. String Indexing (Converting categorical to numerical):")
    contract_indexer = StringIndexer(inputCol="contract_type", outputCol="contract_index")
    payment_indexer = StringIndexer(inputCol="payment_method", outputCol="payment_index")
    
    # Step 2: One-hot encoding
    print("2. One-Hot Encoding (Creating dummy variables):")
    contract_encoder = OneHotEncoder(inputCol="contract_index", outputCol="contract_encoded")
    payment_encoder = OneHotEncoder(inputCol="payment_index", outputCol="payment_encoded")
    
    # Step 3: Feature assembly
    print("3. Feature Assembly (Creating feature vector):")
    feature_cols = ["age", "tenure", "monthly_charges", "total_charges", 
                    "contract_encoded", "payment_encoded"]
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    
    # Step 4: Standard scaling
    print("4. Standard Scaling (Normalizing features):")
    scaler = StandardScaler(inputCol="features", outputCol="scaled_features", 
                           withStd=True, withMean=True)
    
    # Create pipeline
    feature_pipeline = Pipeline(stages=[
        contract_indexer, payment_indexer,
        contract_encoder, payment_encoder,
        assembler, scaler
    ])
    
    # Fit pipeline
    print("\nFitting feature engineering pipeline...")
    start_time = time.time()
    feature_model = feature_pipeline.fit(train_df)
    feature_time = time.time() - start_time
    
    # Transform data
    train_transformed = feature_model.transform(train_df)
    test_transformed = feature_model.transform(test_df)
    
    print(f"Pipeline fitting time: {feature_time:.2f} seconds")
    print(f"Transformed training features shape: {train_transformed.count()} samples")
    
    # Show transformed features
    print("\nSample of transformed features:")
    train_transformed.select("scaled_features", "churn").show(5, truncate=False)
    
    return train_transformed, test_transformed, feature_model

def demonstrate_classification_pipeline(train_df, test_df):
    """Build and evaluate classification models"""
    print("\n" + "="*80)
    print("CLASSIFICATION PIPELINES")
    print("="*80)
    
    # Model 1: Logistic Regression
    print("\n1. Logistic Regression:")
    start_time = time.time()
    
    lr = LogisticRegression(featuresCol="scaled_features", labelCol="churn",
                           maxIter=100, regParam=0.01, elasticNetParam=0.8)
    
    lr_model = lr.fit(train_df)
    lr_time = time.time() - start_time
    
    # Make predictions
    lr_predictions = lr_model.transform(test_df)
    
    # Evaluate
    evaluator = BinaryClassificationEvaluator(labelCol="churn", 
                                             rawPredictionCol="rawPrediction",
                                             metricName="areaUnderROC")
    lr_auc = evaluator.evaluate(lr_predictions)
    
    multi_evaluator = MulticlassClassificationEvaluator(labelCol="churn",
                                                       predictionCol="prediction",
                                                       metricName="f1")
    lr_f1 = multi_evaluator.evaluate(lr_predictions)
    
    print(f"Training time: {lr_time:.2f} seconds")
    print(f"AUC-ROC: {lr_auc:.4f}")
    print(f"F1 Score: {lr_f1:.4f}")
    
    # Model 2: Random Forest
    print("\n2. Random Forest Classifier:")
    start_time = time.time()
    
    rf = RandomForestClassifier(featuresCol="scaled_features", labelCol="churn",
                               numTrees=50, maxDepth=10, seed=42)
    
    rf_model = rf.fit(train_df)
    rf_time = time.time() - start_time
    
    rf_predictions = rf_model.transform(test_df)
    rf_auc = evaluator.evaluate(rf_predictions)
    rf_f1 = multi_evaluator.evaluate(rf_predictions)
    
    print(f"Training time: {rf_time:.2f} seconds")
    print(f"AUC-ROC: {rf_auc:.4f}")
    print(f"F1 Score: {rf_f1:.4f}")
    
    # Model 3: Gradient Boosted Trees
    print("\n3. Gradient Boosted Trees:")
    start_time = time.time()
    
    gbt = GBTClassifier(featuresCol="scaled_features", labelCol="churn",
                       maxIter=50, maxDepth=5, seed=42)
    
    gbt_model = gbt.fit(train_df)
    gbt_time = time.time() - start_time
    
    gbt_predictions = gbt_model.transform(test_df)
    gbt_auc = evaluator.evaluate(gbt_predictions)
    gbt_f1 = multi_evaluator.evaluate(gbt_predictions)
    
    print(f"Training time: {gbt_time:.2f} seconds")
    print(f"AUC-ROC: {gbt_auc:.4f}")
    print(f"F1 Score: {gbt_f1:.4f}")
    
    # Summary
    print("\n" + "-"*40)
    print("CLASSIFICATION MODEL SUMMARY:")
    print(f"Logistic Regression: AUC={lr_auc:.4f}, F1={lr_f1:.4f}, Time={lr_time:.1f}s")
    print(f"Random Forest:       AUC={rf_auc:.4f}, F1={rf_f1:.4f}, Time={rf_time:.1f}s")
    print(f"Gradient Boosted:    AUC={gbt_auc:.4f}, F1={gbt_f1:.4f}, Time={gbt_time:.1f}s")
    
    return lr_model, rf_model, gbt_model

def demonstrate_regression_pipeline(regression_df):
    """Build and evaluate regression models"""
    print("\n" + "="*80)
    print("REGRESSION PIPELINES")
    print("="*80)
    
    # Feature engineering for regression
    print("Preparing regression features...")
    
    # String index location zone
    location_indexer = StringIndexer(inputCol="location_zone", outputCol="location_index")
    location_encoder = OneHotEncoder(inputCol="location_index", outputCol="location_encoded")
    
    # Assemble features
    reg_feature_cols = ["square_footage", "bedrooms", "bathrooms", "year_built", "location_encoded"]
    reg_assembler = VectorAssembler(inputCols=reg_feature_cols, outputCol="features")
    reg_scaler = StandardScaler(inputCol="features", outputCol="scaled_features")
    
    # Create regression pipeline
    reg_pipeline = Pipeline(stages=[location_indexer, location_encoder, reg_assembler, reg_scaler])
    
    # Split data
    train_df, test_df = regression_df.randomSplit([0.8, 0.2], seed=42)
    
    # Fit pipeline
    reg_model = reg_pipeline.fit(train_df)
    train_transformed = reg_model.transform(train_df)
    test_transformed = reg_model.transform(test_df)
    
    # Model 1: Linear Regression
    print("\n1. Linear Regression:")
    start_time = time.time()
    
    lin_reg = LinearRegression(featuresCol="scaled_features", labelCol="price",
                              maxIter=100, regParam=0.01, elasticNetParam=0.8)
    
    lin_reg_model = lin_reg.fit(train_transformed)
    lin_reg_time = time.time() - start_time
    
    lin_reg_predictions = lin_reg_model.transform(test_transformed)
    
    # Evaluate
    reg_evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction")
    lin_reg_rmse = reg_evaluator.evaluate(lin_reg_predictions, {reg_evaluator.metricName: "rmse"})
    lin_reg_r2 = reg_evaluator.evaluate(lin_reg_predictions, {reg_evaluator.metricName: "r2"})
    
    print(f"Training time: {lin_reg_time:.2f} seconds")
    print(f"RMSE: ${lin_reg_rmse:,.2f}")
    print(f"R² Score: {lin_reg_r2:.4f}")
    
    # Model 2: Random Forest Regressor
    print("\n2. Random Forest Regressor:")
    start_time = time.time()
    
    rf_reg = RandomForestRegressor(featuresCol="scaled_features", labelCol="price",
                                  numTrees=50, maxDepth=10, seed=42)
    
    rf_reg_model = rf_reg.fit(train_transformed)
    rf_reg_time = time.time() - start_time
    
    rf_reg_predictions = rf_reg_model.transform(test_transformed)
    rf_reg_rmse = reg_evaluator.evaluate(rf_reg_predictions, {reg_evaluator.metricName: "rmse"})
    rf_reg_r2 = reg_evaluator.evaluate(rf_reg_predictions, {reg_evaluator.metricName: "r2"})
    
    print(f"Training time: {rf_reg_time:.2f} seconds")
    print(f"RMSE: ${rf_reg_rmse:,.2f}")
    print(f"R² Score: {rf_reg_r2:.4f}")
    
    # Summary
    print("\n" + "-"*40)
    print("REGRESSION MODEL SUMMARY:")
    print(f"Linear Regression: RMSE=${lin_reg_rmse:,.2f}, R²={lin_reg_r2:.4f}, Time={lin_reg_time:.1f}s")
    print(f"Random Forest:     RMSE=${rf_reg_rmse:,.2f}, R²={rf_reg_r2:.4f}, Time={rf_reg_time:.1f}s")
    
    return lin_reg_model, rf_reg_model

def demonstrate_hyperparameter_tuning(train_df):
    """Show cross-validation and hyperparameter tuning"""
    print("\n" + "="*80)
    print("HYPERPARAMETER TUNING WITH CROSS-VALIDATION")
    print("="*80)
    
    # Create a simpler pipeline for tuning demonstration
    lr = LogisticRegression(featuresCol="scaled_features", labelCol="churn")
    
    # Create parameter grid
    param_grid = ParamGridBuilder() \
        .addGrid(lr.regParam, [0.01, 0.1, 1.0]) \
        .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
        .addGrid(lr.maxIter, [50, 100]) \
        .build()
    
    # Create cross-validator
    evaluator = BinaryClassificationEvaluator(labelCol="churn", 
                                             rawPredictionCol="rawPrediction",
                                             metricName="areaUnderROC")
    
    cv = CrossValidator(estimator=lr,
                       estimatorParamMaps=param_grid,
                       evaluator=evaluator,
                       numFolds=3,  # 3-fold CV for speed
                       parallelism=2,  # Parallel jobs
                       seed=42)
    
    print(f"Tuning Logistic Regression with {len(param_grid)} parameter combinations")
    print(f"Using 3-fold cross-validation (2 parallel jobs)")
    
    start_time = time.time()
    cv_model = cv.fit(train_df)
    tune_time = time.time() - start_time
    
    print(f"\nTuning completed in {tune_time:.2f} seconds")
    
    # Get best model
    best_model = cv_model.bestModel
    print(f"\nBest Model Parameters:")
    print(f"  regParam: {best_model.getRegParam():.4f}")
    print(f"  elasticNetParam: {best_model.getElasticNetParam():.4f}")
    print(f"  maxIter: {best_model.getMaxIter()}")
    
    # Get cross-validation results
    print(f"\nCross-Validation Results:")
    avg_metrics = cv_model.avgMetrics
    for i, params in enumerate(param_grid):
        print(f"  Params {i+1}: AUC = {avg_metrics[i]:.4f}")
    
    print(f"\nBest AUC: {max(avg_metrics):.4f}")
    
    return cv_model

def compare_pyspark_vs_sklearn(classification_df):
    """Compare PySpark MLlib with scikit-learn"""
    print("\n" + "="*80)
    print("PYSPARK MLlib vs SCIKIT-LEARN COMPARISON")
    print("="*80)
    
    # Convert to pandas for sklearn
    print("Converting to pandas for sklearn comparison...")
    pdf = classification_df.toPandas()
    
    # Prepare features for sklearn
    from sklearn.preprocessing import LabelEncoder, StandardScaler as SklearnStandardScaler
    
    # Encode categorical features
    le_contract = LabelEncoder()
    le_payment = LabelEncoder()
    
    pdf['contract_encoded'] = le_contract.fit_transform(pdf['contract_type'])
    pdf['payment_encoded'] = le_payment.fit_transform(pdf['payment_method'])
    
    # Feature columns
    feature_cols = ['age', 'tenure', 'monthly_charges', 'total_charges', 
                   'contract_encoded', 'payment_encoded']
    X = pdf[feature_cols].values
    y = pdf['churn'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = SklearnStandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Sklearn Random Forest
    print("\n1. scikit-learn Random Forest:")
    start_time = time.time()
    
    sklearn_rf = SklearnRF(n_estimators=50, max_depth=10, random_state=42, n_jobs=2)
    sklearn_rf.fit(X_train_scaled, y_train)
    
    sklearn_time = time.time() - start_time
    
    sklearn_pred = sklearn_rf.predict(X_test_scaled)
    sklearn_accuracy = accuracy_score(y_test, sklearn_pred)
    sklearn_f1 = f1_score(y_test, sklearn_pred)
    
    print(f"Training time: {sklearn_time:.2f} seconds")
    print(f"Accuracy: {sklearn_accuracy:.4f}")
    print(f"F1 Score: {sklearn_f1:.4f}")
    
    # PySpark Random Forest (for comparison)
    print("\n2. PySpark MLlib Random Forest:")
    
    # We need to prepare the PySpark data
    from pyspark.ml.feature import VectorAssembler
    from pyspark.ml.classification import RandomForestClassifier
    
    # Create feature vector
    assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
    spark_df = assembler.transform(classification_df)
    
    # Split
    train_spark, test_spark = spark_df.randomSplit([0.8, 0.2], seed=42)
    
    start_time = time.time()
    
    pyspark_rf = RandomForestClassifier(featuresCol="features", labelCol="churn",
                                       numTrees=50, maxDepth=10, seed=42)
    pyspark_model = pyspark_rf.fit(train_spark)
    
    pyspark_time = time.time() - start_time
    
    pyspark_pred = pyspark_model.transform(test_spark)
    evaluator = MulticlassClassificationEvaluator(labelCol="churn",
                                                 predictionCol="prediction",
                                                 metricName="f1")
    pyspark_f1 = evaluator.evaluate(pyspark_pred)
    
    print(f"Training time: {pyspark_time:.2f} seconds")
    print(f"F1 Score: {pyspark_f1:.4f}")
    
    # Comparison
    print("\n" + "-"*40)
    print("COMPARISON SUMMARY:")
    print(f"scikit-learn: Time={sklearn_time:.1f}s, F1={sklearn_f1:.4f}")
    print(f"PySpark MLlib: Time={pyspark_time:.1f}s, F1={pyspark_f1:.4f}")
    print(f"\nKey Differences:")
    print("1. PySpark is designed for distributed data (scales to large datasets)")
    print("2. scikit-learn is optimized for single-machine performance")
    print("3. PySpark includes built-in feature engineering pipelines")
    print("4. PySpark models can be saved/loaded for distributed serving")

def ml_best_practices_for_8gb():
    """Provide ML best practices for 8GB RAM systems"""
    print("\n" + "="*80)
    print("ML BEST PRACTICES FOR 8GB RAM SYSTEMS")
    print("="*80)
    
    print("""
1. **Data Size Management:**
   - Start with 10K-50K samples for experimentation
   - Use .sample() for quick iterations
   - Process data in chunks if > 100K samples
   - Cache only transformed DataFrames, not raw data

2. **Model Selection:**
   - Linear models (Logistic/Linear Regression) are memory efficient
   - Tree-based models (Random Forest, GBT) need more memory
   - Limit tree depth (maxDepth=5-10) and number of trees (n_estimators=10-50)
   - Use feature importance to reduce dimensionality

3. **Hyperparameter Tuning:**
   - Use small parameter grids (2-3 values per parameter)
   - Use 3-fold CV instead of 5 or 10
   - Set parallelism=2 for CrossValidator
   - Cache training data before tuning

4. **Memory Optimization:**
   - Use .unpersist() after model training
   - Clear cache with spark.catalog.clearCache()
   - Monitor memory in Spark UI during training
   - Use MEMORY_AND_DISK storage level for large feature matrices

5. **Production Considerations:**
   - Save models using model.save("path")
   - Load models with Model.load("path")
   - Test model serving performance
   - Consider model size for deployment
""")

def ml_exercises(classification_df, regression_df):
    """Provide hands-on ML exercises"""
    print("\n" + "="*80)
    print("MACHINE LEARNING EXERCISES")
    print("="*80)
    
    print("""
Exercise 1: Feature Engineering Pipeline
------------------------------------------------
1. Build a complete feature engineering pipeline for the classification dataset
2. Include: StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
3. Compare performance with/without feature scaling
4. Measure pipeline fitting time

Exercise 2: Model Comparison
------------------------------------------------
1. Train Logistic Regression, Random Forest, and Gradient Boosted Trees
2. Compare training time, AUC-ROC, and F1 score
3. Determine which model is best for your 8GB system
4. Analyze feature importance for tree-based models

Exercise 3: Hyperparameter Tuning
------------------------------------------------
1. Create a parameter grid for Random Forest
2. Use CrossValidator with 3-fold cross-validation
3. Find optimal maxDepth and numTrees
4. Compare tuned vs default performance

Exercise 4: PySpark vs scikit-learn
------------------------------------------------
1. Train the same model in both PySpark and scikit-learn
2. Compare training time and performance
3. Analyze memory usage differences
4. Determine when to use each framework

Exercise 5: Model Serialization
------------------------------------------------
1. Save a trained PySpark model using model.save()
2. Load the model in a new Spark session
3. Make predictions with the loaded model
4. Compare predictions with original model
""")

def main():
    """Main execution function"""
    print("="*80)
    print("ADVANCED PYSPARK: ML PIPELINES WITH MLlib ON 8GB RAM")
    print("="*80)
    print("This tutorial covers machine learning with PySpark MLlib.")
    print("All examples optimized for 8GB RAM systems.\n")
    
    # Initialize Spark
    global spark
    spark = create_ml_optimized_spark_session()
    
    try:
        # Generate ML datasets
        classification_df, regression_df = generate_ml_datasets(spark, num_samples=20000)
        
        # Run demonstrations
        train_transformed, test_transformed, feature_model = demonstrate_feature_engineering(classification_df)
        demonstrate_classification_pipeline(train_transformed, test_transformed)
        demonstrate_regression_pipeline(regression_df)
        demonstrate_hyperparameter_tuning(train_transformed)
        compare_pyspark_vs_sklearn(classification_df)
        ml_best_practices_for_8gb()
        ml_exercises(classification_df, regression_df)
        
        print("\n" + "="*80)
        print("TUTORIAL COMPLETE")
        print("="*80)
        print("Key Takeaways:")
        print("1. PySpark MLlib provides scalable ML for distributed data")
        print("2. Feature engineering pipelines are essential for production ML")
        print("3. Tree-based models need careful parameter tuning for 8GB RAM")
        print("4. Cross-validation helps prevent overfitting")
        print("5. Model serialization enables deployment")
        print("\nNext: Run 05_streaming_analytics.py for PySpark Streaming tutorials")
        
    finally:
        # Cleanup
        spark.catalog.clearCache()
        spark.stop()
        print("\nSpark session stopped.")

if __name__ == "__main__":
    main()