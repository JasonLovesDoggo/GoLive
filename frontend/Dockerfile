FROM --platform=linux/amd64 python:alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN pip install waitress

CMD ["waitress-serve", "--port=8000", "app:app"]
