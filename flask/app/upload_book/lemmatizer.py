import logging
from nltk.corpus.reader import POS_LIST
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class Lemmatizer():

    STOPWORDS = stopwords.words('english')
    ADVERB_TO_ADJECTIVE_THRESH = 0.8
    WORD_NET_LEMMATIZER = WordNetLemmatizer()

    logger = logging.getLogger(__name__)

    def is_stopword(self, word):
        return word in self.STOPWORDS

    def convert_adverb_to_adjective(self, adverb):
        possible_adj = []
        for lemma in wn.lemmas(adverb):
            for ps in lemma.pertainyms():
                possible_adj.append(ps.name())

        if len(possible_adj) == 0:
            return ''

        adjective = possible_adj[0]
        adv_len = len(adverb)
        adj_len = len(adjective)
        intersection = set(adverb).intersection(set(adverb))
        common_part_len = len(intersection)
        rel = common_part_len*1.0/min(adv_len, adj_len)

        if rel > self.ADVERB_TO_ADJECTIVE_THRESH:
            return adjective
        else:
            return ''

    def lemmatize(self, word):
        pos_to_lemma = {}

        for pos in POS_LIST:
            lemma = self.WORD_NET_LEMMATIZER.lemmatize(word, pos)
            pos_to_lemma[pos] = lemma

        changed_words = set([lemma for lemma in pos_to_lemma.values() if lemma != word])

        if len(changed_words) == 0:
            return ''

        if len(changed_words) > 1:
            self.logger.warning("More than one lemma for word '%s': %s" % (word, changed_words))

        return changed_words.pop()


