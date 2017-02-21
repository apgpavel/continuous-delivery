FROM python:3.5
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD gunicorn -w 4 helloworld:app -b localhost:5000
