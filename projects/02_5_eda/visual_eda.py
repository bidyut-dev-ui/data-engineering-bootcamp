import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Ensure output directory exists
os.makedirs('plots', exist_ok=True)

def perform_visual_eda():
    print("🚀 Starting Visual EDA...")
    
    # 1. Load Data
    df = pd.read_csv('customer_data.csv')
    print(f"Loaded {len(df)} rows.")
    
    # Set Seaborn style
    sns.set_theme(style="whitegrid")
    
    # ---------------------------------------------------------
    # 1. OUTLIER DETECTION: Boxplots
    # ---------------------------------------------------------
    print("📊 Generating Boxplots (Outlier Detection)...")
    plt.figure(figsize=(12, 6))
    
    # Create subplots for Income and Age
    plt.subplot(1, 2, 1)
    sns.boxplot(y=df['income'])
    plt.title('Income Distribution (Check for Outliers)')
    
    plt.subplot(1, 2, 2)
    sns.boxplot(y=df['age'])
    plt.title('Age Distribution (Check for Outliers)')
    
    plt.tight_layout()
    plt.savefig('plots/01_outliers_boxplot.png')
    plt.close()
    print("   -> Saved plots/01_outliers_boxplot.png")
    
    # ---------------------------------------------------------
    # 2. CORRELATION: Heatmap
    # ---------------------------------------------------------
    print("🔥 Generating Heatmap (Correlation)...")
    plt.figure(figsize=(10, 8))
    
    # Calculate correlation matrix (numeric only)
    corr = df.select_dtypes(include=['number']).corr()
    
    # Draw heatmap
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title('Correlation Matrix')
    
    plt.tight_layout()
    plt.savefig('plots/02_correlation_heatmap.png')
    plt.close()
    print("   -> Saved plots/02_correlation_heatmap.png")
    
    # ---------------------------------------------------------
    # 3. DISTRIBUTION: Histograms/KDE
    # ---------------------------------------------------------
    print("📈 Generating Distributions (Histograms)...")
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    sns.histplot(df['purchase_amount'], kde=True, color='green')
    plt.title('Purchase Amount Distribution')
    
    plt.subplot(1, 2, 2)
    sns.histplot(df['age'], kde=True, color='orange')
    plt.title('Age Distribution')
    
    plt.tight_layout()
    plt.savefig('plots/03_distributions_hist.png')
    plt.close()
    print("   -> Saved plots/03_distributions_hist.png")
    
    # ---------------------------------------------------------
    # 4. RELATIONSHIPS: Pairplot
    # ---------------------------------------------------------
    print("🔗 Generating Pairplot (Relationships)...")
    # Pairplot is computationally expensive, so we sample if data is huge
    sample_df = df.sample(min(500, len(df)))
    
    # Color by 'category' to see clusters
    sns.pairplot(sample_df, hue='category', vars=['age', 'income', 'purchase_amount'])
    
    plt.savefig('plots/04_pairplot.png')
    plt.close()
    print("   -> Saved plots/04_pairplot.png")
    
    # ---------------------------------------------------------
    # 5. CATEGORICAL: Bar Plot
    # ---------------------------------------------------------
    print("📊 Generating Bar Plots (Categorical)...")
    plt.figure(figsize=(10, 6))
    
    sns.countplot(x='category', data=df, palette='viridis')
    plt.title('Count of Customers by Category')
    
    plt.tight_layout()
    plt.savefig('plots/05_categorical_bar.png')
    plt.close()
    print("   -> Saved plots/05_categorical_bar.png")

if __name__ == "__main__":
    perform_visual_eda()
