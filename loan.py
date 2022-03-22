
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


from sklearn.model_selection import train_test_split




# load mortgage data from a csv file for training
from sklearn.tree import DecisionTreeClassifier

new_training = 'static/numeric_testData.csv'
new_train_df = pd.read_csv(new_training)

new_y = new_train_df.values[:, 11]

new_X = new_train_df.values[:, 0:11]

new_X_train, new_X_test, new_y_train, new_y_test = train_test_split(new_X, new_y, test_size=0.3, random_state=0)

dt_clf_gini = DecisionTreeClassifier(criterion="gini",
                                     random_state=0,
                                     max_depth=15,
                                     min_samples_leaf=5)
dt_clf_gini.fit(new_X_train, new_y_train)
y_pred_gini = dt_clf_gini.predict(new_X_test)

print("Decision Tree using Gini Index\nAccuracy is ",
      accuracy_score(new_y_test, y_pred_gini) * 100)


def loan_prediction(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 11)
    result = dt_clf_gini.predict(to_predict)

    return result[0]