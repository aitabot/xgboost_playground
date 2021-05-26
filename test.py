import pandas as pd  # load and manipulate data and for One-Hot Encoding
import numpy as np  # calculate the mean and standard deviation
import xgboost as xgb  # XGBoost stuff
import matplotlib.pyplot as plt
# split  data into training and testing sets
from sklearn.model_selection import train_test_split
# for scoring during cross validation
from sklearn.metrics import balanced_accuracy_score, roc_auc_score, make_scorer
from sklearn.model_selection import GridSearchCV  # cross validation
from sklearn.metrics import confusion_matrix  # creates a confusion matrix
from sklearn.metrics import plot_confusion_matrix  # draws a confusion matrix
from sklearn.metrics import mean_squared_error

df = pd.read_csv('data.csv')
df['shifted_adjusted_close'] = df['adjusted_close'].shift(-1)
df.dropna(inplace=True)
df.drop(['date'], axis=1, inplace=True)


def train_test_split2(data, perc):
    """
        data contains [X, y]
        perc is the percentage of data to use as testdata
        returns [X_80%, y_80%], [X_20%, y_20%]
    """
    data = data.values
    n = int(len(data) * (1 - perc))
    return data[:n], data[n:]


train, test = train_test_split2(df, 0.2)


def xgb_predict(train, y_test_0):
    """
        train  contains [...X, y]
        y_test is the value we use to test our prediction
    """
    train = np.array(train)
    X, y = train[:, :-1], train[:, -1]
    model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=1000)
    model.fit(X, y)
    pred = model.predict(y_test_0)
    return pred[0]


# print(test[0][:-1])
xgb_predict(train, test[0][:-1])
