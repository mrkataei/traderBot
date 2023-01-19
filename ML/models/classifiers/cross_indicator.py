import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score
from sklearn import svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
import pickle


def read_data(address):
    data = pd.read_csv(address)
    # filling the places with no cross occurunce in the data with 2.0
    data['cross'] = data['cross'].fillna(2.0)
    # rounding the numbers to two decimal point
    data = data.round(2)
    # sorting the dataframe columns to the desired order
    data = data[['date', 'd[1]', 'd[2]', 'd[3]', 'd', 'k[1]', 'k[2]', 'k[3]', 'k', 'cross']]
    data.dropna(inplace=True)
    return data


def data_preprocess(data):
    # creating the columns containing the difference of k and d indicators
    data['difference1'] = data['d[1]'] - data['k[1]']
    data['difference2'] = data['d[2]'] - data['k[2]']
    data['difference3'] = data['d[3]'] - data['k[3]']
    data['difference'] = data['d'] - data['k']
    data.reset_index(inplace=True)
    return data


def train_test_prepration(data, columns):
    # splitting the dataset
    data_useful = data.copy()
    data_useful = data[columns]

    train_x, test_x, train_y, test_y = train_test_split(data_useful.iloc[:, :-1], data_useful['cross'], test_size=0.3,
                                                        shuffle=False)

    # splitting the date column from the train and test datasets
    train_date = train_x['date']
    test_date = test_x['date']
    train_x.drop(columns=['date'], inplace=True)
    test_x.drop(columns=['date'], inplace=True)

    return train_x, test_x, train_y, test_y, train_date, test_date


# scaling the train and test data
def scaling(train_x, test_x):
    scaler = MinMaxScaler()
    train_x = pd.DataFrame(scaler.fit_transform(train_x), columns=train_x.columns)
    test_x = pd.DataFrame(scaler.transform(test_x), columns=test_x.columns)
    return scaler, train_x, test_x


def classifier(clf_name, scores, train_x, test_x, train_y, test_y, save=False):
    """
    choose a classifier model by passing its name abbreviation:
    'knn' - 'svm' - 'dtree' - 'rf' - 'gb' - 'ada' - 'stack'
    """
    if clf_name == 'knn':
        clf = KNeighborsClassifier(n_neighbors=5)
    elif clf_name == 'svm':
        clf = svm.SVC(decision_function_shape='ovr', C=1.0, gamma='scale')

    elif clf_name == 'dtree':
        clf = svm.clf = DecisionTreeClassifier(random_state=0)

    elif clf_name == 'rf':
        clf = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)

    elif clf_name == 'gb':
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.5, max_depth=5, random_state=0)

    elif clf_name == 'ada':
        clf = AdaBoostClassifier(n_estimators=100, random_state=0)

    elif clf_name == 'stack':
        estimators = [
            ('rf_200', RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=0)),
            ('rf_100', RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)),
            ('rf_boot', RandomForestClassifier(n_estimators=100, bootstrap=False, criterion='entropy', random_state=0)),
            ('rf_gini', RandomForestClassifier(n_estimators=100, criterion='gini', random_state=0)),
            ('gb_0.5', GradientBoostingClassifier(n_estimators=100, learning_rate=0.5,
                                                  max_depth=7, random_state=0)),
            ('gb_0.2', GradientBoostingClassifier(n_estimators=100, learning_rate=0.2,
                                                  max_depth=4, random_state=0)),
            ('ada', AdaBoostClassifier(n_estimators=100, random_state=0)),
            ('svc', svm.SVC(decision_function_shape='ovr', C=1.0, gamma='scale')),
            ('knn', KNeighborsClassifier(n_neighbors=5))
        ]
        clf = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())
    if clf:
        X, y = train_x.values, train_y.values
        clf = clf.fit(X, y)
        y_pred = clf.predict(test_x.values)
        score_acc = accuracy_score(test_y, y_pred)
        score_prec = precision_score(test_y, y_pred, average="weighted")
        scores.append((clf_name, score_acc, score_prec))
        if save:
            filename = '{}.sav'.format(clf_name)
            pickle.dump(clf, open(filename, 'wb'))
        # loaded_model = pickle.load(open(filename, 'rb'))


if __name__ == '__main__':
    address = "crossover tradingview.csv"
    data = read_data(address)
    data = data_preprocess(data)
    columns = ['date', 'difference1', 'difference2', 'difference3', 'difference', 'd[1]', 'd[2]', 'd[3]', 'd', 'k[1]',
               'k[2]', 'k[3]', 'k', 'cross']

    """
    # different combination of columns for training - uncomment the one you want
    # data_useful = data[['date','difference3','difference','d[3]','d','k[3]','k','cross']]
    # data_useful = data[['date','d[1]','d[2]','d[3]','d','k[1]','k[2]','k[3]','k','cross']]
    # data_useful = data[['date','difference1','difference2','difference3','difference','cross']]
    """

    train_x, test_x, train_y, test_y, train_date, test_date = train_test_prepration(data, columns)
    scaler, train_x, test_x = scaling(train_x, test_x)
    scores = []
