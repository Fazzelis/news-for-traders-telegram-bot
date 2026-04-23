#!/bin/sh

until nc -z postgresql-news-tg-bot 5432; do
  echo "Waiting for postgres..."
  sleep 2
done

alembic upgrade head

exec python main.py