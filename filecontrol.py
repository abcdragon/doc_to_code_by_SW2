import pickle


def load_data():
    try:
        with open('data.save', 'rb') as file:
            data = pickle.load(file)
        return data

    except FileNotFoundError:
        return []

    except:
        return []


def save_data(data):
    with open('data.save', 'wb') as file:
        pickle.dump(data, file)
