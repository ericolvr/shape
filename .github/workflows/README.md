# CI/CD Pipeline

Este projeto utiliza GitHub Actions para automação de CI/CD.

## 🔄 Workflow: CI Pipeline

**Trigger:**
- Pull Requests para `main`
- Push direto na branch `main`

### Jobs

#### 1. 🔍 Lint (Code Quality)
- **Black**: Verifica formatação do código
- **Flake8**: Análise estática de código

#### 2. 🧪 Test (Testes)
- Executa todos os testes unitários
- Gera relatório de cobertura
- Upload para Codecov (opcional)
- **Threshold mínimo**: 80% de cobertura

#### 3. 🚀 Build & Deploy Simulation
- Inicia PostgreSQL em container
- Executa migrações do Alembic
- Smoke test da aplicação
- Simula deploy

## 📊 Status Badges

Adicione ao README principal:

```markdown
![CI Pipeline](https://github.com/seu-usuario/shape/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/seu-usuario/shape/branch/main/graph/badge.svg)](https://codecov.io/gh/seu-usuario/shape)
```

## 🛠️ Comandos Locais

Antes de fazer commit, rode localmente:

```bash
# Formatar código
make format

# Verificar formatação
make format-check

# Linting
make lint

# Testes com cobertura
make test-cov
```

## 🔐 Secrets Necessários

Configure no GitHub (Settings > Secrets):

- `CODECOV_TOKEN` (opcional): Token do Codecov para upload de cobertura

## ✅ Checklist de PR

Antes de abrir um Pull Request:

- [ ] Código formatado com Black
- [ ] Linting passou (Flake8)
- [ ] Todos os testes passando
- [ ] Cobertura >= 80%
- [ ] Migrações criadas (se necessário)
