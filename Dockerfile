FROM python:3.9

RUN useradd -m appuser
USER appuser
WORKDIR /chatgpt-web

ENV PATH="/home/appuser/.local/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn.py", "app:server"]
