import nltk
import logging


if __name__ == '__main__':
    logging.info("Downloading 'stopwords'...")
    nltk.download('stopwords')
    logging.info("DONE")

    logging.info("Downloading 'wordnet'...")
    nltk.download('wordnet')
    logging.info("DONE")

    logging.info("Downloading 'wordnet_ic'...")
    nltk.download('wordnet_ic')
    logging.info("DONE")