import pickle
import os


def load_data():
    try:
        with open('project_data.pyprojt', 'rb') as file:
            data = pickle.load(file)
        return data

    except FileNotFoundError:
        return []

    except:
        return []


def save_data(data, full_path):
    with open(full_path + '/project_data.pyprojt', 'wb') as file:
        pickle.dump(data, file)
