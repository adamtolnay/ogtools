import sys

import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def make_prediction(colX, colY):
    # Ensure colX and colY are integers
    colX = int(colX)
    colY = int(colY)

    # Connect to MySQL database using SQLAlchemy
    engine = create_engine('mysql+mysqlconnector://root:Halloween123!@localhost/ogtools')

    # Fetch gene expression data (features) from the "data" table
    gene_query = "SELECT * FROM data"
    gene_data = pd.read_sql(gene_query, engine)

    # Fetch metadata (target) from the "metadata" table
    metadata_query = f"SELECT column_{colY} FROM metadata"
    metadata_data = pd.read_sql(metadata_query, engine)

    # Prepare the feature matrix (gene expression) and the target (metadata column)
    # Restrict X to columns from colX onwards
    X = gene_data.iloc[colX:, 1:].T.values  # All rows, starting from column colX to the end
    y = metadata_data.iloc[:, 0].values  # All rows, only the colY-th column

    # Debugging prints to check the matrices
    print(f"Selected column range for X: {colX} to end")
    print(f"X shape: {X.shape}")
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

    # Return the R-squared score
    return r2


import sys

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 predict.py <colX> <colY>")
        sys.exit(1)

    colX = int(sys.argv[1])
    colY = int(sys.argv[2])
    
    result = make_prediction(colX, colY)
    print(result)
