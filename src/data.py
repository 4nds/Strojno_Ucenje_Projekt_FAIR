import os
import pandas as pd             # 1.3.4
import sklearn                  # 1.1.1
import sklearn.model_selection

class FncData:

    def __init__(self, bodies_csv_path, stances_csv_path, max_length=None):        
        self.bodies_csv_path = bodies_csv_path
        self.stances_csv_path = stances_csv_path
        self.max_length = max_length
        self.cache = pd.DataFrame()
        self.headlines_and_bodies_train = None
        self.headlines_and_bodies_test = None
        self.stances_train = None
        self.stances_test = None
        self.load()
        return

    def load(self):
        self.bodies = pd.read_csv(self.bodies_csv_path)
        self.headlines_and_stances = pd.read_csv(self.stances_csv_path)
        if self.max_length:
            self.bodies = self.bodies.iloc[:self.max_length]
            self.headlines_and_stances = \
                self.headlines_and_stances.iloc[:self.max_length]
        self.headlines_bodies_and_stances = pd.merge(
            self.headlines_and_stances, self.bodies, on='Body ID')
        return

    def splitIntoTrainAndTest(self, test_size=0.3):
        self.headlines_and_bodies_train, self.headlines_and_bodies_test,\
            self.stances_train, self.stances_test = \
                sklearn.model_selection.train_test_split(
                    self.headlines_bodies_and_stances[
                        ['Headline', 'articleBody']],
                    self.headlines_bodies_and_stances[['Stance']],
                    test_size=test_size, random_state=42
                )
        return


if __name__ == '__main__':
    FNC_DATA_PATH = '../fnc-1/'
    bodies_csv_path = os.path.join(FNC_DATA_PATH, 'train_bodies.csv')
    stances_csv_path = os.path.join(FNC_DATA_PATH, 'train_stances.csv')
    fnc_data = FncData(bodies_csv_path, stances_csv_path)
    fnc_data.splitIntoTrainAndTest()
    print(fnc_data.headlines_bodies_and_stances.head())