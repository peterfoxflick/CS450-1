from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from kNN.kNNClassifier import kNNClassifier


def test_cars():
    headers = [
        "buying", "maint", "doors", "persons", "lug_boot", "safety", "target"
    ]
    cars_data = pd.read_csv(
        "../datasets/car.data.csv", header=None, names=headers)
    test_one_hot(cars_data)


def run_model(data, targets, message):
    classifiers = [
        KNeighborsClassifier(n_neighbors=3),
        kNNClassifier(k=3, use_tree=True, scale=False)
    ]
    c_names = ["Sklearn", "Personal kNN w/ Tree"]
    train_d, test_d, train_t, test_t = train_test_split(
        data, targets, shuffle=True)
    for index, classifier in enumerate(classifiers):
        classifier.fit(train_d, train_t)
        predict = classifier.predict(test_d)
        diff = get_diff(predict, test_t)
        print("#################################")
        print(c_names[index])
        print(message)
        print("#################################")
        print(round(((test_t.size - len(diff)) / test_t.size) * 100, 2))


def get_diff(predicted_t, actual_t):
    diff = []
    for index, predicted in enumerate(predicted_t):
        if predicted != actual_t[index]:
            diff.append({
                'index': index,
                'predicted': predicted,
                'actual': actual_t[index]
            })
    return diff


def test_one_hot(cars_data):
    hb_cars = one_hot_car(cars_data)
    clean_up_targets = {
        "target": {
            "unacc": 0,
            "acc": 1,
            "good": 2,
            "vgood": 3
        }
    }
    hb_cars.replace(clean_up_targets, inplace=True)
    targets = hb_cars["target"].values
    column_names = hb_cars.columns.values
    data = hb_cars[column_names[1:]].values
    message = "Running one hot"
    run_model(data, targets, message)


def one_hot_car(dataset):
    # Hot box data
    return pd.get_dummies(
        dataset,
        columns=["buying", "maint", "doors", "persons", "lug_boot", "safety"])
