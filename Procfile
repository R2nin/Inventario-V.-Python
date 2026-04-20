# Procfile - usado pelo Railway e Heroku para iniciar a aplicação em produção
# O Gunicorn é o servidor web que roda o Django em produção
web: python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
