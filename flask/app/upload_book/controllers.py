import re
import chardet
import logging
from flask import Blueprint, render_template, request, make_response
from app.upload_book.lemmatizer import Lemmatizer

MAX_FILE_SIZE = 1024 * 1024 + 1

uploader = Blueprint('uploader', __name__)

lemmatizer = Lemmatizer()
alpha_pattern = re.compile('[^a-zA-Z]+', re.UNICODE)

logger = logging.getLogger(__name__)

@uploader.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        args["method"] = "POST"
        files = request.files.getlist("file[]")
        combined_file = ""
        for file in files:
            file_content = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_content) == MAX_FILE_SIZE
            if len(file_content) == MAX_FILE_SIZE:
                logger.error("Max file size %s exceeded for file %s" % (MAX_FILE_SIZE, file))
                return render_template("upload_book/index.html", args=args)

            encoding = chardet.detect(file_content)
            logger.debug("Detected encoding for file %s is %s" % (file, encoding))
            file_content = file_content.decode(encoding['encoding'])
            combined_file = "%s %s" % (combined_file, file_content)

        stats, converted_lemmatized = count_number_of_words(combined_file)
        args["stats"] = stats
        if "list" in request.form:
            return download_list(converted_lemmatized)

    return render_template("upload_book/index.html", args=args)


def download_list(converted_lemmatized):
    lemmas = list(converted_lemmatized)
    lemmas.sort()
    str = ""
    for lemma in lemmas:
        str += lemma
        str += "\r\n"
    response = make_response(str)
    cd = 'attachment; filename=list.txt'
    response.headers['Content-Disposition'] = cd
    response.mimetype='text/plain'
    return response


def count_number_of_words(file_content):
    file_content = re.sub(alpha_pattern, ' ', file_content)
    total_count = 0
    no_stopwords = set()
    lemmatized = set()
    converted_lemmatized = set()

    for word in file_content.split():
        word = word.lower()
        total_count += 1
        if lemmatizer.is_stopword(word):
            continue
        no_stopwords.add(word)

        lemma = lemmatizer.lemmatize(word)
        if len(lemma) != 0:
            lemmatized.add(lemma)
        else:
            lemmatized.add(word)

        adjective = lemmatizer.convert_adverb_to_adjective(word)
        if len(adjective) == 0:
            adjective = word
        lemma = lemmatizer.lemmatize(adjective)
        if len(lemma) != 0:
            converted_lemmatized.add(lemma)
        else:
            converted_lemmatized.add(adjective)

    no_stopwords_count = len(no_stopwords)
    lemmatized_count = len(lemmatized)
    converted_lemmatized_count = len(converted_lemmatized)
    stats = {"Total number of words": total_count,
             "Number of unique words": no_stopwords_count,
             "Number of unique lemmas": lemmatized_count,
             "Number of unique lemmas with conversion": converted_lemmatized_count}

    logger.info(stats)
    return stats, converted_lemmatized
