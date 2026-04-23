#!/bin/sh

until nc -z postgresql 5432; do
  echo "Waiting for postgres..."
  sleep 2
done

alembic upgrade head

exec python main.py