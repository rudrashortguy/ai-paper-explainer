# Contributing

## Development Setup

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Running Locally

```bash
./run.sh
```

## Code Quality

```bash
# Backend
ruff check backend/ --fix
mypy backend/
pytest backend/ --cov=backend/ --cov-report=term-missing
bandit -r backend/

# Frontend
cd frontend && npm run lint && npm run format
```

## Commit Guidelines

Use Conventional Commits:

- `feat:` new feature
- `fix:` bug fix
- `refactor:` code change without feature/fix
- `docs:` documentation only
- `test:` adding or fixing tests
- `chore:` maintenance, deps

## Pull Request Process

1. All checks must pass (lint, typecheck, test, coverage >85%)
2. Update `AGENTS.md` if architecture changes
3. Update `DEPLOYMENT.md` if deployment steps change
