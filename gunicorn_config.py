# gunicorn_config.py

bind = '0.0.0.0:80'  # Bind to all network interfaces on port 80
workers = 2  # Use 2 worker processes
timeout = 600  # Set timeout to 60 seconds
keepalive = 5  # Set keepalive timeout to 5 seconds
accesslog = '-'  # Log access to stdout
errorlog = '-'  # Log errors to stdout
loglevel = 'info'  # Set log level to info
worker_class = 'gthread'  # Use the gthread worker class
