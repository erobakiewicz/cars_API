## Description

Django REST API app with three basic functionalities. All of them accessible via API. First functionality is car
database. User can list, retrieve, delete and add cars. New cars can be added only if they are validated against
external API serving information about cars. Second functionality enables users to rate cars present in our local
database in scale 1 to 5. Third enables users to see list of cars in order of popularity (popularity is measured in
number of ratings).

## Installation

### Prerequisites

- Python
- Django / Django REST Framework
- Docker
- PostgreSQL
- Redis
- Celery

### Setup

1. Clone repository and fill `.env` file placed in root directory, with variables:
    - `SECRET_KEY` - django secret key
    - `DATABASE_URL` - postgres database url
2. Run in root directory `docker-compose up`

### Heroku

App is not ready to deploy with redis and celery on Heroku.