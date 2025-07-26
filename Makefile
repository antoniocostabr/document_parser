# Document Parser Platform Makefile
# ===================================

.PHONY: help install dev clean test build run stop logs shell health parse-test docker-build docker-run docker-stop docker-clean compose-up compose-down compose-logs compose-restart

# Default target
help: ## Show this help message
	@echo "Document Parser Platform - Available Commands:"
	@echo "=============================================="
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Setup
install: ## Install dependencies and setup virtual environment
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

dev: ## Start development server
	.venv/bin/python app.py

dev-cli: ## Test CLI with sample invoice
	.venv/bin/python parse.py test_files/sample_invoice.pdf

# Testing
test: ## Run tests
	.venv/bin/python -m pytest tests/ -v

test-api: ## Test API endpoints (requires running server)
	@echo "Testing health endpoint..."
	curl -s http://localhost:8000/health | jq
	@echo "\nTesting parse endpoint with sample invoice..."
	curl -s -X POST -F "file=@test_files/sample_invoice.pdf" http://localhost:8000/parse | jq '.confidence_score'

parse-test: ## Quick parse test with sample files
	@echo "Testing invoice parsing..."
	curl -s -X POST -F "file=@test_files/sample_invoice.pdf" http://localhost:8000/parse | jq '.configurable_fields.document_type, .confidence_score'
	@echo "\nTesting resume parsing..."
	curl -s -X POST -F "file=@test_files/sample_resume.pdf" http://localhost:8000/parse | jq '.configurable_fields.document_type, .confidence_score'

health: ## Check API health
	curl -s http://localhost:8000/health | jq

# Docker Commands
docker-build: ## Build Docker image
	docker build -t document-parser .

docker-run: ## Run Docker container with env file
	docker run -d -p 8000:8000 --env-file .env --name document-parser-container document-parser

docker-stop: ## Stop and remove Docker container
	docker stop document-parser-container || true
	docker rm document-parser-container || true

docker-logs: ## Show Docker container logs
	docker logs document-parser-container

docker-shell: ## Open shell in running Docker container
	docker exec -it document-parser-container /bin/bash

docker-clean: ## Remove Docker image and containers
	docker stop document-parser-container || true
	docker rm document-parser-container || true
	docker rmi document-parser || true

# Docker Compose Commands
compose-up: ## Start services with Docker Compose
	docker-compose up -d

compose-down: ## Stop services with Docker Compose
	docker-compose down

compose-logs: ## Show Docker Compose logs
	docker-compose logs -f

compose-restart: ## Restart services with Docker Compose
	docker-compose restart

compose-build: ## Build services with Docker Compose
	docker-compose build

compose-ps: ## Show Docker Compose service status
	docker-compose ps

# Utility Commands
clean: ## Clean up temporary files and cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf dist/
	rm -rf build/

generate-samples: ## Generate sample PDF files for testing
	.venv/bin/python scripts/generate_sample_pdfs.py

logs: ## Show development server logs (for background processes)
	tail -f app.log 2>/dev/null || echo "No log file found"

shell: ## Start Python shell with project context
	.venv/bin/python -c "from document_parser import DocumentParser; from document_parser.models import *; print('Document Parser shell ready')"

# Package Management
install-dev: ## Install package in development mode
	.venv/bin/pip install -e .

requirements: ## Generate requirements.txt from current environment
	.venv/bin/pip freeze > requirements.txt

# Environment
env-check: ## Check environment variables
	@echo "Environment Variables:"
	@echo "OPENAI_API_KEY: $${OPENAI_API_KEY:+SET}"
	@echo "OPENAI_MODEL: $${OPENAI_MODEL:-gpt-4o-mini}"
	@echo "MAX_FILE_SIZE_MB: $${MAX_FILE_SIZE_MB:-10}"

# Complete workflows
setup: install generate-samples ## Complete setup: install dependencies and generate test files
	@echo "Setup complete! Ready to run 'make dev' or 'make compose-up'"

full-test: compose-up test-api compose-down ## Full test: start compose, test API, stop compose
	@echo "Full test completed successfully!"

deploy: docker-build compose-up ## Build and deploy with Docker Compose
	@echo "Deployment complete! API available at http://localhost:8000"
