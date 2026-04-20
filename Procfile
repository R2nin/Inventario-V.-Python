# Procfile - usado pelo Railway e Heroku para iniciar a aplicação em produção
# O Gunicorn é o servidor web que roda o Django em produção
release: python manage.py migrate --noinput
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
