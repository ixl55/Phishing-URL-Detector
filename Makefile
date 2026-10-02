.PHONY: install dev-backend dev-frontend test lint build run

install:
	pip install -r backend/requirements-dev.txt
	npm --prefix frontend install

dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	npm --prefix frontend run dev

test:
	cd backend && python -m pytest -q
	npm --prefix frontend test

lint:
	cd backend && ruff check .
	npm --prefix frontend run lint

build:
	npm --prefix frontend run build

run: build
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
