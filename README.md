# Shape API

API de exemplo com um único domínio (User), apenas para uma breve demonstração.

## Pré-requisitos

- Docker
- Python 3.9
- PostgreSQL


## Desenvolvimento Local

```bash
# Instalar dependências
make install

# Copiar Env
make env

# Inicializar o Postgres
make db-start

# Rodar localmente
make run
```


## Tests

```bash
# Rodar testes
make test

# Testes com cobertura
make test-cov
```

**Cobertura atual: 89%** ✅

## Code Quality

```bash
# Formatar código
make format

# Verificar formatação
make format-check

# Linting
make lint
```

## CI/CD

Pipeline automatizado com GitHub Actions:
- Linting (Black + Flake8)
- Testes
- Build & Deploy Simulation

**Trigger:** Pull Requests e merges na `main`

## API Docs
- **Swagger UI**: http://localhost:8000/docs




## Tracing

```bash
# Iniciar o Jaeger
make jaeger-start
```

## Jaeger Endpoint

http://localhost:16686
