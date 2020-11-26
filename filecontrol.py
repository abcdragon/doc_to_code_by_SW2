import pickle


def load_data(full_path):
    try:
        with open(full_path + '/project_data.pyprojt', 'rb') as file:
            data = pickle.load(file)
        return data

    except FileNotFoundError:
        return None

    except:
        return None


def save_data(data, full_path):
    with open(full_path + '/project_data.pyprojt', 'wb') as file:
        pickle.dump(data, file)
