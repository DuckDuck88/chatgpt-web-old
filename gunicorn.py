# gunicorn.conf
# 并行工作进程数
workers = 1
# 指定每个工作者的线程数
threads = 8
bind = '0.0.0.0:8888'
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# 工作模式协程
worker_class = 'gevent'
worker_connections = 2000
pidfile = '/var/run/gunicorn.pid'
accesslog = '/var/log/gunicorn_acess.log'
errorlog = '/var/log/gunicorn_error.log'
loglevel = 'debug'
reload = False
