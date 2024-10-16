import pandas as pd
from sklearn.linear_model import LinearRegression

data = pd.read_csv("housing.csv")

x = data[['latitude']]
y = data['households']

model = LinearRegression()

model.fit(x, y)

# Evaluate the model
r2_score = model.score(x, y)
print(f"R-squared value: {r2_score}")

