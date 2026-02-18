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
```


## Tracing

```bash
# Iniciar o Jaeger
make jaeger-start
```

## Tracing Endpoint

http://localhost:16686
