# Setup instructions
- Populate valid .env file
- Run `docker compose up --build`

# Actions within container
## Tests
- Run `docker exec -it django-docker python manage.py test`

## Linting Fixer
- Run `docker exec -it django-docker ruff check --fix`

## Import data_dumps
- Run `docker exec -it django-docker python manage.py loaddata myapp/migrations/data_dumps/...`
