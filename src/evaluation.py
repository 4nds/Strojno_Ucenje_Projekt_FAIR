import warnings
import numpy as np              # 1.22.0
import pandas as pd             # 1.3.4

try:
    from IPython.display import display
except:
    pass

warnings.simplefilter(action="ignore", \
    category=pd.core.common.SettingWithCopyWarning)

class Evaluator:

    def getRelatedCorrectness(self, actual_stances, predicted_stance):
        both_related = np.logical_and(actual_stances != 'unrelated',
            predicted_stance != 'unrelated')
        return np.sum(both_related) / np.size(actual_stances != 'unrelated')

    def getUnrelatedCorrectness(self, actual_stances, predicted_stance):
        both_unrelated = np.logical_and(actual_stances == 'unrelated',
            predicted_stance == 'unrelated')
        return np.sum(both_unrelated) / np.size(actual_stances == 'unrelated')

    def getIsRelatedCorrectness(self, actual_stances, predicted_stance):
        both_unrelated = np.logical_and(actual_stances == 'unrelated',
            predicted_stance == 'unrelated')
        both_related = np.logical_and(actual_stances != 'unrelated',
            predicted_stance != 'unrelated')
        return (np.sum(both_unrelated) + np.sum(both_related)) / actual_stances.size

    def getRelationshipCorrectness(self, actual_stances, predicted_stance):
        both_related = np.logical_and(actual_stances != 'unrelated',
            predicted_stance != 'unrelated')
        both_related_and_same = np.logical_and(both_related,
            actual_stances == predicted_stance)
        return np.sum(both_related_and_same) / np.sum(both_related)

    def getScore(self, actual_stances, predicted_stance):
        both_unrelated = np.logical_and(actual_stances == 'unrelated',
            predicted_stance == 'unrelated')
        both_related = np.logical_and(actual_stances != 'unrelated',
            predicted_stance != 'unrelated')
        both_related_and_same = np.logical_and(both_related,
            actual_stances == predicted_stance)
        score = (0.25*np.sum(both_unrelated) + 0.25*np.sum(both_related) 
            + 0.75*np.sum(both_related_and_same))
        return score

    def getScorePercentage(self, actual_stances, predicted_stance):
        score = self.getScore(actual_stances, predicted_stance)
        maximal_score = (0.25*np.sum(actual_stances == 'unrelated')
            + np.sum(actual_stances != 'unrelated'))
        return score / maximal_score

    def getScoreMatrix(self, actual_stances, predicted_stance):
        stances = pd.DataFrame(data=dict(
            ActualStances=actual_stances,
            PredictedStance=predicted_stance,
        ))
        score_matrix = pd.DataFrame(dict({
            '': ['Agree', 'Disagree', 'Discuss', 'Unrelated', 'Overall'],
            'Agree': np.zeros(5, dtype=int),
            'Disagree': np.zeros(5, dtype=int),
            'Discuss': np.zeros(5, dtype=int),
            'Unrelated': np.zeros(5, dtype=int),
            'Accuracy (%)': np.zeros(5),
        }))
        stances_types = ['Agree', 'Disagree', 'Discuss', 'Unrelated']
        for predicted_stance in stances_types:
            for row in range(4):
                actual_stance = stances_types[row]
                #score_matrix.loc[:row, actual_stance] = \
                #score_matrix.at[predicted_stance, row] = \
                score_matrix[predicted_stance].iloc[row] = \
                    np.sum((stances['ActualStances'] == actual_stance.lower()) & \
                        (stances['PredictedStance'] == predicted_stance.lower()))
        for row in range(4):
            actual_stance = stances_types[row]
            score_matrix['Accuracy (%)'].iloc[row] = \
                round(100 * (score_matrix[actual_stance].iloc[row]
                    / np.sum(score_matrix.iloc[row][stances_types])), 2)
        score_matrix['Accuracy (%)'].iloc[4] = \
            round(100 * (sum(score_matrix[stance].iloc[row] for row, stance \
                in enumerate(stances_types)) / stances.shape[0]), 2)
        return score_matrix

    def print(self, actual_stances, predicted_stance, decimals=4):
        print('Results:')
        print('    score:', self.getScore(actual_stances, predicted_stance))
        print('    score percentage: {:.{precision}f}'. \
            format(100 * self.getScorePercentage(actual_stances, predicted_stance), \
                precision=decimals))
        return


    def show(self, actual_stances, predicted_stance, decimals=4):        
        display(self.getScoreMatrix(actual_stances, predicted_stance))
        self.print(actual_stances, predicted_stance, decimals)
        return
        