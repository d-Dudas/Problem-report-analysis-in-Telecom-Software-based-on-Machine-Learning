FROM python:3

WORKDIR /app

ENV FLASK_APP=app.py

ENV FLASK_ENV=developement

COPY requirements.txt .

RUN pip install -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('words'); nltk.download('punkt')"

COPY . .

CMD ["python", "app.py"]
