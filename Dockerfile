FROM python:3-alpine3.18
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
RUN python -c "import nltk; nltk.download(['punkt', 'stopwords', 'averaged_perceptron_tagger', 'wordnet'])"
EXPOSE 3000
CMD python ./index.py