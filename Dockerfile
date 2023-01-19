FROM python:3.9

WORKDIR /chatgpt-web
COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
