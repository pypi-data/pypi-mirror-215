import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

def perform_eda(data):
    # Inspect the dimensions of the dataset
    print("Dataset dimensions:", data.shape)
    print()

    # Check the data types
    print("Data types:")
    print(data.dtypes)
    print()

    # Summary statistics
    
    print("Summary statistics:")
    print(data.describe())
    print()

    # Missing values
    print("Missing values:")
    print(data.isnull().sum())
    print()

    # Duplicate data
    duplicate_rows = data.duplicated()
    print("Duplicate rows:", duplicate_rows.sum())
    print()

    # Visualize distributions and relationships
    print("Data visualizations:")
    for column in data.columns:
        if data[column].dtype == 'object':
            # Categorical variable
            data[column].value_counts().plot(kind='bar', figsize=(8, 6))
            plt.title(column)
            plt.show()
        else:
            # Numeric variable
            data[column].hist(figsize=(8, 6))
            plt.title(column)
            plt.show()

            # Box plot
            sns.boxplot(data=data, x=column)
            plt.title(column + " (Box Plot)")
            plt.show()

            # Scatter plot (numeric vs. numeric)
            numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
            for numeric_column in numeric_columns:
                if numeric_column != column:
                    plt.scatter(data[column], data[numeric_column])
                    plt.xlabel(column)
                    plt.ylabel(numeric_column)
                    plt.title(column + " vs. " + numeric_column)
                    plt.show()

            # Kernel density plot
            sns.kdeplot(data[column], shade=True)
            plt.title(column + " (Kernel Density Plot)")
            plt.show()

    # Correlation matrix
    correlation_matrix = data.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

    # Pairwise scatter plot (numeric variables)
    sns.pairplot(data.select_dtypes(include=['int64', 'float64']))
    plt.title("Pairwise Scatter Plot")
    plt.show()

    # Cross-tabulation (categorical variables)
    categorical_columns = data.select_dtypes(include=['object']).columns
    if len(categorical_columns) > 1:
        for i in range(len(categorical_columns)):
            for j in range(i + 1, len(categorical_columns)):
                cross_tab = pd.crosstab(data[categorical_columns[i]], data[categorical_columns[j]])
                cross_tab.plot(kind='bar', stacked=True, figsize=(8, 6))
                plt.title(categorical_columns[i] + " vs. " + categorical_columns[j])
                plt.show()

    # Heatmap of missing values
    sns.heatmap(data.isnull(), cmap='viridis')
    plt.title("Missing Values Heatmap")
    plt.show()

    # Feature correlation with the target variable
    target_variable = "<target_variable_name>"  # Replace with the name of your target variable
    if target_variable in data.columns:
        correlations = data.corr()[target_variable].sort_values(ascending=False)
        plt.figure(figsize=(8, 6))
        sns.barplot(x=correlations.values, y=correlations.index, orient='h')
        plt.title("Feature Correlation with Target Variable")
        plt.xlabel("Correlation")
        plt.ylabel("Features")
        plt.show()

    # Outlier detection (numeric variables)
    numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
    for column in numeric_columns:
        # Calculate z-scores for outlier detection
        z_scores = (data[column] - data[column].mean()) / data[column].std()
        outliers = data[np.abs(z_scores) > 3][column]

        if not outliers.empty:
            print(f"Outliers in {column}:")
            print(outliers)
            print()

