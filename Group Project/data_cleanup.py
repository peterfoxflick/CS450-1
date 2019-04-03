import pandas as pd


def load_data(use_means=True):
    data = pd.read_csv("../datasets/linkedenrollments.csv")
    if use_means:
        data = impute_means(data)
    else:
        data = impute_zero(data)
    data = drop_helper_columns(data)
    data = encode_courses(data)
    split = split_data_targets(data)
    return split


def impute_means(data):
    columns = ["currentScore", "finalScore", "CS 124", "CS 165", "CS 235"]
    for col in columns:
        data[col].fillna(data[col].mean(), inplace=True)
    return data


def impute_zero(data):
    columns = ["currentScore", "finalScore", "CS 124", "CS 165", "CS 235"]
    for col in columns:
        data[col].fillna(0, inplace=True)
    return data


def drop_helper_columns(data, columns=["teacherName"]):
    return data.drop(columns=columns)


def encode_courses(data):
    columns = [
        "currentGrade", "finalGrade", "userId", "courseCode", "courseId",
        "teacherId"
    ]
    for col in columns:
        data[col] = data[col].astype("category")
        data[col] = pd.factorize(data[col])[0] + 1
    return data


def split_data_targets(data):
    targets = data["currentScore"]
    data = data.drop(columns=["currentScore"])
    struct = {}
    struct["targets"] = targets
    struct["data"] = data
    return struct
