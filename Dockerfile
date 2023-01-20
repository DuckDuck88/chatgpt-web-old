FROM python:3.9

WORKDIR /chatgpt-web
# 先跑 run，否则 文件内容变动会导致构建时重新 pip install 依赖  速度较慢
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "-c", "gunicorn.py", "app:server"]
