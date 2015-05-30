import pytest

from pandas import DataFrame
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelBinarizer
from sklearn.svm import SVC
import numpy as np

from sklearn_pandas import (
    DataFrameMapper,
    PassthroughTransformer,
    cross_val_score,
)

@pytest.fixture
def iris_dataframe():
    iris = load_iris()
    return DataFrame(
        data={
            iris.feature_names[0]: iris.data[:,0],
            iris.feature_names[1]: iris.data[:,1],
            iris.feature_names[2]: iris.data[:,2],
            iris.feature_names[3]: iris.data[:,3],
            "species": np.array([iris.target_names[e] for e in iris.target])
        }
    )

def test_with_iris_dataframe(iris_dataframe):
    pipeline = DataFrameMapper([
        ("petal length (cm)", PassthroughTransformer()),
        ("petal width (cm)", PassthroughTransformer()),
        ("sepal length (cm)", PassthroughTransformer()),
        ("sepal width (cm)", PassthroughTransformer()),
        ("species", LabelBinarizer()),
    ])
    data = iris_dataframe.drop("species", axis=1)
    labels = iris_dataframe["species"]
    clf = SVC(kernel='linear', C=1)
    scores = cross_val_score(clf, data, labels)
    assert scores.mean() > 0.96
    assert (scores.std() * 2) < 0.04