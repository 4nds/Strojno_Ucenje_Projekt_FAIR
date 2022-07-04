import re                       # 2.2.1
import sklearn                  # 1.1.1
import gensim                   # 4.2.0
import nltk                     # 3.2.2
#from sklearn import preprocessing

class WordTokenizer:

    def __init__(self, library='nltk'):
        self.library = library
        count_vectorizer = sklearn.feature_extraction.text.CountVectorizer()
        self.sklearn_tokenize = count_vectorizer.build_tokenizer()
        if self.library == 'builtin':
            self.tokenize_method = self.tokenizeSplit
        elif self.library == 'nltk':
            self.tokenize_method = self.tokenizeNltk
        elif self.library == 'sklearn':
            self.tokenize_method = self.tokenizeSklearn
        elif self.library == 'gensim':
            self.tokenize_method = self.tokenizeGensim
        else:
            raise ValueError('Property WordTokenizer.library should be ' \
                + 'one of "builtin", "nltk", "sklearn" and "gensim", ' \
                + 'but {} is used'.format(self.library))
        return

    def tokenizeSplit(self, text):
        return text.split()

    def tokenizeNltk(self, text):
        return nltk.tokenize.word_tokenize(text)

    def tokenizeSklearn(self, text):
        return self.sklearn_tokenize(text)

    def tokenizeGensim(self, text):
        return list(gensim.utils.tokenize(text))

    def tokenize(self, text):
        return self.tokenize_method(text)

class SentenceTokenizer:

    Alphabets= '([A-Za-z])'
    Prefixes = '(Mr|St|Mrs|Ms|Dr)[.]'
    Suffixes = '(Inc|Ltd|Jr|Sr|Co)'
    Starters = ''.join([
        '(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s',
        '|But\s|However\s|That\s|This\s|Wherever)'
    ])
    Acronyms = '([A-Z][.][A-Z][.](?:[A-Z][.])?)'
    Websites = '[.](com|net|org|io|gov)'

    def __init__(self, library='re'):
        self.library = library
        if self.library == 're':
            self.tokenize_method = self.tokenizeRegex
        elif self.library == 'nltk':
            self.tokenize_method = self.tokenizeNltk
        else:
            raise ValueError('Property SentenceTokenizer.library should be ' \
                + 'one "re" or "nltk", but {} is used'.format(self.library))
        return

    def tokenizeRegex(self, text):
        text = ' {}  '.format(text)
        text = text.replace('\n', ' ').replace('\r\n', ' ')
        text = re.sub(self.Prefixes, '\\1<prd>', text)
        text = re.sub(self.Websites, '<prd>\\1', text)
        if 'Ph.D' in text:
            text = text.replace('Ph.D.', 'Ph<prd>D<prd>')
        text = re.sub('\s{}[.] '.format(self.Alphabets),' \\1<prd> ', text)
        text = re.sub('{} {}'.format(self.Acronyms, self.Starters), \
            '\\1<stop> \\2', text)
        text = re.sub('{0}[.]{0}[.]{0}[.]'.format(self.Alphabets), \
            '\\1<prd>\\2<prd>\\3<prd>', text)
        text = re.sub('{0}[.]{0}[.]'.format(self.Alphabets), \
            '\\1<prd>\\2<prd>', text)
        text = re.sub(' {}[.]{}'.format(self.Suffixes, self.Starters), \
            ' \\1<stop> \\2', text)
        text = re.sub(' {}[.]'.format(self.Suffixes), ' \\1<prd>', text)
        text = re.sub(' {}[.]'.format(self.Alphabets), ' \\1<prd>', text)
        if '”' in text:
            text = text.replace('.”', '”.')
        if '\'' in text:
            text = text.replace('.\'', '\'.')
        if '!' in text:
            text = text.replace('!\'', '\'!')
        if '?' in text:
            text = text.replace('?\'', '\'?')
        text = text.replace('.', '.<stop>')
        text = text.replace('?', '?<stop>')
        text = text.replace('!', '!<stop>')
        text = text.replace('<prd>', '.')
        sentences = text.split('<stop>')
        sentences = [s.strip() for s in sentences]
        if not sentences[-1]:
            sentences = sentences[:-1]
        return sentences

    def tokenizeNltk(self, text):
        return nltk.tokenize.sent_tokenize(text)

    def tokenize(self, text):
        return self.tokenize_method(text)

if __name__ == '__main__':

    text1 = ' '.join([
        'If you’re experiencing a bit of a post-Christmas hangover in the',
        'warm and fuzzy, feel-good department, look no further—there’s',
        'a video for that. On Christmas Day, Joe Riquelme,',
        'creator of the successful Videoshop editing app,',
        'gave his parents a Christmas to remember. Riquelme casually hands',
        'his parents an envelope with this present inside:',
    ])
    preprocessed_text1 = ' '.join([
       ' you’re experiencing bit post christmas hangover warm fuzzy',
       'feel good department look no further—there’s video christmas',
       'day joe riquelme creator successful videoshop editing app gave',
       'parents christmas remember riquelme casually hands parents',
       'envelope present inside',
    ])
    text2 = ''.join([
        'We took a look at the photo said to show the body of',
        'Islamic State leader Abu Bakr Al-Baghdadi (right)',
        'and found it was really an ethnic Albanian militant killed',
        "in 2013 (left)  -- with Al-Baghdadi's head and watch added.",
        'See a news report on the death of Sami Hafez Al-Abdullah',
        'here: http://hournews.net/news.php?id=21302.',
    ])
    preprocessed_text2 = ' '.join([
        'took look photo said body islamic state leader abu bakr',
        'al baghdadi right ethnic albanian militant killed 2013',
        'left al baghdadi head watch added news report death',
        'sami hafez al abdullah http hournews net news php id 21302',
    ])

    texts_and_preprocessed_texts = [
        (text1, preprocessed_text1),
        (text2, preprocessed_text2),
    ]
    for text, preprocessed_text in texts_and_preprocessed_texts:
        print('Text:\n{}'.format(text))
        print()
        for library in ('builtin', 'nltk', 'sklearn', 'gensim'):
            word_tokenizer = WordTokenizer(library=library)
            print('Text tokenized into words with {} tokenizer:\n{}'.format(
                library,
                word_tokenizer.tokenize(text)
            ))
            print()
        for library in ('builtin', 'nltk', 'sklearn', 'gensim'):
            word_tokenizer = WordTokenizer(library=library)
            print('Preprocessed text tokenized into words' \
                + ' with {} tokenizer:\n{}'.format(
                    library,
                    word_tokenizer.tokenize(preprocessed_text)
                )
            )
            print()
        print('\n')

    for text, preprocessed_text in texts_and_preprocessed_texts:
        print('Text:\n{}'.format(text))
        print()
        for library in ('re', 'nltk'):
            sentence_tokenizer = SentenceTokenizer(library=library)
            print('Text tokenized into sentence with {} tokenizer:\n{}'.format(
                library,
                sentence_tokenizer.tokenize(text)
            ))
            print()
        print('\n')
        

