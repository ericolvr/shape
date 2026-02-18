# ANSI color codes
COLOR_RESET=\033[0m
COLOR_BOLD=\033[1m
COLOR_GREEN=\033[32m
COLOR_YELLOW=\033[33m
COLOR_BLUE=\033[34m
COLOR_RED=\033[31m

ENV_FILE = .env.$(ENV)
DB_VOLUME_NAME=postgres_data_shape
CONTAINER_NAME=shape-postgres

.PHONY: install 

help:
	@echo ""
	@echo "  $(COLOR_BLUE)Local Development:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)install$(COLOR_RESET)		- Install dependencies"
	@echo "  $(COLOR_GREEN)env$(COLOR_RESET)			- Create .env from .env.example"
	@echo "  $(COLOR_GREEN)run$(COLOR_RESET)			- Run development server"
	@echo ""
	@echo "  $(COLOR_BLUE)Database:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)db-start$(COLOR_RESET)		- Start database container"
	@echo "  $(COLOR_GREEN)db-stop$(COLOR_RESET)		- Stop database container"
	@echo "  $(COLOR_GREEN)db-clean$(COLOR_RESET)		- Clean database data"
	@echo ""
	@echo "  $(COLOR_BLUE)Tracing (Jaeger):$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)tracing-start$(COLOR_RESET)	- Start Jaeger container"
	@echo "  $(COLOR_GREEN)tracing-stop$(COLOR_RESET)	- Stop Jaeger container"
	@echo "  $(COLOR_GREEN)tracing-ui$(COLOR_RESET)		- Open Jaeger UI in browser"
	@echo ""
	@echo "  $(COLOR_BLUE)Migrations (Alembic):$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)migrate$(COLOR_RESET)		- Run pending migrations"
	@echo "  $(COLOR_GREEN)migrate-create$(COLOR_RESET)	- Create new migration"
	@echo "  $(COLOR_GREEN)migrate-history$(COLOR_RESET)	- Show migration history"
	@echo "  $(COLOR_GREEN)migrate-rollback$(COLOR_RESET)	- Rollback last migration"
	@echo ""
	@echo "  $(COLOR_BLUE)Testing:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)test$(COLOR_RESET)			- Run unit tests"
	@echo "  $(COLOR_GREEN)test-cov$(COLOR_RESET)		- Run tests with coverage report"
	@echo ""
	@echo "  $(COLOR_BLUE)Code Quality:$(COLOR_RESET)"
	@echo "  $(COLOR_GREEN)lint$(COLOR_RESET)			- Run linting (flake8)"
	@echo "  $(COLOR_GREEN)format$(COLOR_RESET)		- Format code with black"
	@echo "  $(COLOR_GREEN)format-check$(COLOR_RESET)	- Check code formatting"
	@echo ""


install:
	@echo "$(COLOR_YELLOW)Installing dependencies...$(COLOR_RESET)"
	pip install -r requirements.txt
	@echo "$(COLOR_GREEN)Dependencies installed successfully!$(COLOR_RESET)"

install-dev:
	@echo "$(COLOR_YELLOW)Installing dev dependencies...$(COLOR_RESET)"
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	@echo "$(COLOR_GREEN)Dev dependencies installed successfully!$(COLOR_RESET)"

test:
	@echo "$(COLOR_YELLOW)Running unit tests...$(COLOR_RESET)"
	pytest tests/unit/ -v
	@echo "$(COLOR_GREEN)✅ Unit tests passed!$(COLOR_RESET)"

test-cov:
	@echo "$(COLOR_YELLOW)Running tests with coverage...$(COLOR_RESET)"
	pytest tests/unit/ --cov=app --cov-report=html --cov-report=term
	@echo "$(COLOR_GREEN)✅ Coverage report generated in htmlcov/$(COLOR_RESET)"

env:
	@echo "$(COLOR_YELLOW)Setting up environment...$(COLOR_RESET)"
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "$(COLOR_BLUE)Creating .env from .env.example...$(COLOR_RESET)"; \
			cp .env.example .env; \
			echo "$(COLOR_GREEN) .env file created!$(COLOR_RESET)"; \
		else \
			echo "$(COLOR_RED) .env.example not found!$(COLOR_RESET)"; \
			exit 1; \
		fi; \
	else \
		echo "$(COLOR_BLUE).env file already exists$(COLOR_RESET)"; \
	fi

run:
	@echo "$(COLOR_YELLOW)Starting development server...$(COLOR_RESET)"
	@if [ ! -f .env ]; then \
		if [ -f .env.example ]; then \
			echo "$(COLOR_BLUE) .env not found, creating from .env.example...$(COLOR_RESET)"; \
			cp .env.example .env; \
		else \
			echo "$(COLOR_RED) .env.example not found!$(COLOR_RESET)"; \
			exit 1; \
		fi; \
	fi
	@echo "$(COLOR_GREEN)Starting FastAPI with uvicorn...$(COLOR_RESET)"
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


db-start:
	@echo "$(COLOR_YELLOW)Starting Postgres container for $(ENV) environment...$(COLOR_RESET)"
	@if [ "$(ENV)" = "local" ]; then \
		if [ ! -f .env ]; then \
			if [ -f .env.example ]; then \
				echo "$(COLOR_BLUE) .env not found, creating from .env.example...$(COLOR_RESET)"; \
				cp .env.example .env; \
			else \
				echo "$(COLOR_RED) .env.example not found!$(COLOR_RESET)"; \
				exit 1; \
			fi; \
		fi; \
		echo "$(COLOR_BLUE)Using .env file$(COLOR_RESET)"; \
	else \
		if [ ! -f $(ENV_FILE) ]; then \
			echo "$(COLOR_BLUE)Environment file $(ENV_FILE) not found, creating from .env.example...$(COLOR_RESET)"; \
			cp .env.example $(ENV_FILE); \
		fi; \
		echo "$(COLOR_BLUE)Loading environment from: $(ENV_FILE)$(COLOR_RESET)"; \
		cp $(ENV_FILE) .env; \
	fi
	docker compose --env-file .env up postgres -d
	@echo "$(COLOR_GREEN)✅ Database container started!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Database: $$(grep DB_NAME .env | cut -d'=' -f2) on localhost:$$(grep DB_PORT .env | cut -d'=' -f2)$(COLOR_RESET)"

db-stop:
	@echo "$(COLOR_YELLOW)Stopping and removing database container...$(COLOR_RESET)"
	docker compose down postgres
	@echo "$(COLOR_GREEN)✅ Database container removed!$(COLOR_RESET)"

db-clean:
	@echo "$(COLOR_YELLOW)Cleaning database data...$(COLOR_RESET)"
	docker compose down postgres
	docker volume rm $(DB_VOLUME_NAME) 2>/dev/null || true
	@echo "$(COLOR_GREEN)✅ Database data cleaned!$(COLOR_RESET)"

tracing-start:
	@echo "$(COLOR_YELLOW)Starting Jaeger container...$(COLOR_RESET)"
	docker compose up jaeger -d
	@echo "$(COLOR_GREEN)✅ Jaeger started!$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)Jaeger UI: http://localhost:16686$(COLOR_RESET)"

tracing-stop:
	@echo "$(COLOR_YELLOW)Stopping Jaeger container...$(COLOR_RESET)"
	docker compose down jaeger
	@echo "$(COLOR_GREEN)✅ Jaeger stopped!$(COLOR_RESET)"

tracing-ui:
	@echo "$(COLOR_BLUE)Opening Jaeger UI in browser...$(COLOR_RESET)"
	open http://localhost:16686

migrate:
	@echo "$(COLOR_YELLOW)Running database migrations...$(COLOR_RESET)"
	alembic upgrade head
	@echo "$(COLOR_GREEN)✅ Migrations applied successfully!$(COLOR_RESET)"

migrate-create:
	@echo "$(COLOR_YELLOW)Creating new migration...$(COLOR_RESET)"
	@read -p "Enter migration message: " msg; \
	alembic revision --autogenerate -m "$$msg"
	@echo "$(COLOR_GREEN)✅ Migration created!$(COLOR_RESET)"

migrate-history:
	@echo "$(COLOR_BLUE)Migration history:$(COLOR_RESET)"
	alembic history --verbose

migrate-rollback:
	@echo "$(COLOR_YELLOW)Rolling back last migration...$(COLOR_RESET)"
	alembic downgrade -1
	@echo "$(COLOR_GREEN)✅ Migration rolled back!$(COLOR_RESET)"

lint:
	@echo "$(COLOR_YELLOW)Running linting checks...$(COLOR_RESET)"
	flake8 app/ tests/
	@echo "$(COLOR_GREEN)✅ Linting passed!$(COLOR_RESET)"

format:
	@echo "$(COLOR_YELLOW)Formatting code with black...$(COLOR_RESET)"
	black app/ tests/
	@echo "$(COLOR_GREEN)✅ Code formatted!$(COLOR_RESET)"

format-check:
	@echo "$(COLOR_YELLOW)Checking code formatting...$(COLOR_RESET)"
	black --check app/ tests/
	@echo "$(COLOR_GREEN)✅ Code formatting is correct!$(COLOR_RESET)"
