import re
from flask import Blueprint, render_template, request
from app.upload_book.lemmatizer import Lemmatizer

MAX_FILE_SIZE = 1024 * 1024 + 1

uploader = Blueprint('uploader', __name__)

lemmatizer = Lemmatizer()
alphanumeric_pattern = re.compile('[\W_]+', re.UNICODE)


@uploader.errorhandler(413)
def request_entity_too_large(error):
    print("error in uploader")
    args = {"method": "GET"}
    return render_template("upload_book/index.html", args=args)


@uploader.route("/", methods=["POST", "GET"])
def index():
    args = {"method": "GET"}
    if request.method == "POST":
        #files = request.files.getlist("file[]")
        #print(files)
        #files[0].save()
        file = request.files["file"]
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args["file_size_error"] = len(file_bytes) == MAX_FILE_SIZE
            if len(file_bytes) != MAX_FILE_SIZE:
                file_content = file_bytes.decode("utf-8")
                count_number_of_words(file_content)
        args["method"] = "POST"

    return render_template("upload_book/index.html", args=args)


def count_number_of_words(file_content):
    file_content = re.sub(alphanumeric_pattern, ' ', file_content)
    total_count = 0
    no_stopwords = set()
    lemmatized = set()
    converted_lemmatized = set()

    for word in file_content.split():
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
    print("Total count: %s; no stop words: %s; lemmatized: %s; converted lemmatized %s" %
                 (total_count, no_stopwords_count, lemmatized_count, converted_lemmatized_count))