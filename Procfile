# Procfile - usado pelo Railway e Heroku para iniciar a aplicação em produção
# O Gunicorn é o servidor web que roda o Django em produção
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 2
