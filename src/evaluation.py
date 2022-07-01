import numpy as np              # 1.22.0

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