# Setup instructions
- Populate valid .env file
- Run `docker compose up --build`

# Test instructions
- Start containers (see above)
- Run `docker exec -it django-docker python manage.py test`