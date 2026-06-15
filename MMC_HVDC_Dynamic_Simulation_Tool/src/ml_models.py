import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def load_dataset(dataset_path):
    data = pd.read_csv(dataset_path)

    X = data[["N", "modulation_index"]]
    y = data["THD_percent"]

    return X, y


def train_linear_regression(dataset_path):
    X, y = load_dataset(dataset_path)

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)
    r2 = r2_score(y, predictions)

    return model, mae, r2


def train_neural_network(dataset_path):
    X, y = load_dataset(dataset_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42
    )

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("neural_network", MLPRegressor(
            hidden_layer_sizes=(32, 16),
            activation="relu",
            max_iter=5000,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    return model, mae, r2