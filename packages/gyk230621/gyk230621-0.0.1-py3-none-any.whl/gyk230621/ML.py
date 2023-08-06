import math
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def calculate_normal_distribution(x, mean, std_dev):
  coefficient = 1 / (std_dev * math.sqrt(2 * math.pi))
  exponent = -((x - mean) ** 2) / (2 * (std_dev ** 2))
  return coefficient * math.exp(exponent)

def multiple_linear_regression(X, y):
  X = np.column_stack((np.ones((X.shape[0], 1)), X))
  coefficients = np.linalg.inv(X.T @ X) @ X.T @ y
  return coefficients

def train_linear_regression(data, target_column):
  X = data.drop(columns=[target_column])
  y = data[target_column]
  model = LinearRegression()
  model.fit(X, y)
  return model
