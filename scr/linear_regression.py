import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk


class LinearRegression:
    """
    A class to perform simple linear regression analysis.

    This class implements a simple linear regression model using statsmodels,
    calculating the relationship between a single feature (independent variable)
    and a target (dependent variable).

    Attributes:
        _feature_name (str): Name of the feature/independent variable
        _feature (pd.Series): Data series containing the feature values
        _target_name (str): Name of the target/dependent variable
        _target (pd.Series): Data series containing the target values
        _predictions (np.array): Model predictions
        _intercept (float): Y-intercept of the regression line
        _slope (float): Slope of the regression line
        _r_squared (float): R-squared value of the model
        _mse (float): Mean squared error of the model
    """

    def __init__(self, feature: pd.Series, target: pd.Series):
        """
        Initialize the LinearRegression model with feature and target data.

        Args:
            feature (pd.Series): The independent variable series
            target (pd.Series): The dependent variable series
            
        Raises:
            TypeError: If the input data contains non-numeric values
            ValueError: If the input data is empty or lengths don't match
        """
        # Validate input data
        if len(feature) != len(target):
            raise ValueError("Feature and target must have the same length")
        
        if len(feature) == 0:
            raise ValueError("Input data cannot be empty")
            
        # Check for non-numeric data
        if not np.issubdtype(feature.dtype, np.number) or not np.issubdtype(target.dtype, np.number):
            raise TypeError("Feature and target must contain only numeric values")

        # Store the data series from selected columns
        self._feature_name = feature.name
        self._feature = feature
        self._target_name = target.name
        self._target = target

        self._predictions = None
        self._intercept = None
        self._slope = None
        self._r_squared = None
        self._mse = None
        
        self.create_regression(self._feature, self._target)

    @property
    def feature_name(self):
        return self._feature_name

    @property
    def target_name(self):
        return self._target_name

    @property
    def predictions(self):
        return np.array(self._predictions)

    @property
    def intercept(self):
        return self._intercept

    @property
    def slope(self):
        return self._slope

    @property
    def r_squared(self):
        return self._r_squared if not np.isnan(self._r_squared) else 0.0

    @property
    def mse(self):
        return self._mse

    def create_regression(self, feature, target):
        """
        Create and fit the linear regression model.

        This method performs the following steps:
        1. Adds a constant term to the feature for the intercept
        2. Fits the OLS model
        3. Extracts model parameters and statistics
        4. Generates predictions
        5. Calculates mean squared error

        Args:
            feature (pd.Series): The independent variable
            target (pd.Series): The dependent variable
        """
        # Add a column of ones for the intercept term
        feature_with_intercept = sm.add_constant(feature)

        # Train the model
        model_training = sm.OLS(target, feature_with_intercept)
        modelofin = model_training.fit()

        # Get intercept and slope coefficients
        self._intercept, self._slope = modelofin.params
        
        # Handle constant target case
        if np.var(target) == 0:
            self._r_squared = 0.0
        else:
            self._r_squared = modelofin.rsquared

        # Generate model predictions and convert to numpy array
        self._predictions = np.array(modelofin.predict(feature_with_intercept))

        # Calculate MSE (Mean Squared Error)
        self._mse = np.mean((np.array(target) - self._predictions) ** 2)
    

        
        


