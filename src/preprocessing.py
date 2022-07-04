import string
import re                       # 2.2.1
import sklearn                  # 1.1.1
import gensim                   # 4.2.0
import nltk                     # 3.2.2

class Preprocessor:

    Alphabets= '([A-Za-z])'
    Prefixes = '(Mr|St|Mrs|Ms|Dr)[.]'
    Suffixes = '(Inc|Ltd|Jr|Sr|Co)'
    Starters = '(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)'
    Acronyms = '([A-Z][.][A-Z][.](?:[A-Z][.])?)'
    Websites = '[.](com|net|org|io|gov)'

    def __init__(self, **kwargs):
        self.use_nltk_stop_words = kwargs.get('use_nltk_stop_words', True)
        self.use_gensim_stop_words = kwargs.get('use_gensim_stop_words', True)
        self.use_sklearn_stop_words = kwargs.get('use_sklearn_stop_words', True)
        self.remove_negations_from_stop_words = kwargs.get(
            'remove_negations_from_stop_words', True)
        self.stop_words = self.getStopwords()
        return

    def getStopwords(self):
        stop_words = set()
        if self.use_nltk_stop_words:
            stop_words |= set(nltk.corpus.stopwords.words('english'))
        if self.use_gensim_stop_words:
            stop_words |= gensim.parsing.preprocessing.STOPWORDS
        if self.use_sklearn_stop_words:
            stop_words |= \
                sklearn.feature_extraction._stop_words.ENGLISH_STOP_WORDS
        if self.remove_negations_from_stop_words:
            for word in ('no', 'not', 'none', 'cannot'):
                stop_words.discard(word)
        return stop_words
    
    def stripNewLines(self, text):
        return ' '.join(text.split())
		
    def stripPunctuation(self, text):
        return text.translate(str.maketrans('', '', string.punctuation))
    	
    def removeStopwords(self, text):
        return gensim.parsing.preprocessing.remove_stopwords(text, \
            stopwords=self.stop_words)
            
    def preprocessBuiltin(self, text):
        filters = (self.stripPunctuation, self.stripNewLines, \
			lambda s: s.lower(), self.removeStopwords)
        for filter in filters:
            text = filter(text)
        return text

    def preprocess(self, text):
        return ' '.join(gensim.parsing.preprocessing.preprocess_string(
            text,
            filters=[
                gensim.parsing.preprocessing.strip_punctuation,
                lambda s: s.lower(),
                self.removeStopwords,
            ])
        )
        
    

if __name__ == '__main__':
    text1 = ' '.join([
        'If you’re experiencing a bit of a post-Christmas hangover in the',
        'warm and fuzzy, feel-good department, look no further—there’s',
        'a video for that. On Christmas Day, Joe Riquelme,',
        'creator of the successful Videoshop editing app,',
        'gave his parents a Christmas to remember. Riquelme casually hands',
        'his parents an envelope with this present inside:',
    ])
    text2 = ' '.join([
        'Video: Users of the new iPhone 6 are saying their hair is getting',
        'caught in between the screen and the phone’s aluminum back.',
        'The hashtag #hairgate saw thousands of tweets overnight.',
        'Carson Daly reports from the Orange Room.',
    ])
    text3 = ' '.join([
        'We took a look at the photo said to show the body of',
        'Islamic State leader Abu Bakr Al-Baghdadi (right)',
        'and found it was really an ethnic Albanian militant killed',
        "in 2013 (left)  -- with Al-Baghdadi's head and watch added.",
        'See a news report on the death of Sami Hafez Al-Abdullah',
        'here: http://hournews.net/news.php?id=21302.',
    ])

    preprocessor = Preprocessor()

    for text in (text1, text2, text3):
        print('Text:\n{}'.format(text))
        print('Preprocessed text:\n{}'.format(preprocessor.preprocess(text)))
        print()
