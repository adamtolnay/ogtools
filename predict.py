import sys
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Check for correct command-line argument usage
if len(sys.argv) != 2:
    print("Usage: python3 predict.py <metadata_column>")
    sys.exit(1)

# Get the metadata column to predict
metadata_column = int(sys.argv[1])
if metadata_column < 1 or metadata_column > 10:
    print("Please specify 1 to 10 for the metadata column.")
    sys.exit(1)

# Connect to MySQL database using SQLAlchemy
engine = create_engine('mysql+mysqlconnector://root:Halloween123!@localhost/ogtools')

# Fetch gene expression data (features) from the "data" table
gene_query = "SELECT * FROM data1"
gene_data = pd.read_sql(gene_query, engine)

# Fetch metadata (target) from the "metadata" table
metadata_query = f"SELECT column_{metadata_column} FROM metadata"
metadata_data = pd.read_sql(metadata_query, engine)

# Prepare the feature matrix (gene expression) and the target (metadata column)
X = gene_data.iloc[:, 1:].T.values  # All rows, all columns except the first (gene_id)
y = metadata_data.iloc[:, 0].values  # All rows, only the specified column

# Print X and y for debugging
print("Feature matrix (X):")
print(X)
print("Target vector (y):")
print(y)

# Run linear regression
model = LinearRegression()
model.fit(X, y)


# Predict and calculate the R-squared score
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)

# Output the R-squared score
print(f"R-squared: {r2:.10f}")
