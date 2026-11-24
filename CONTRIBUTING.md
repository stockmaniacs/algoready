# Contributing to AlgoReady

Thank you for your interest in contributing to AlgoReady! This document provides guidelines and best practices for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Prerequisites

- Git
- Node.js 18+ (for web & extension)
- Python 3.10+ (for backend)
- PostgreSQL 16+
- Redis 7+

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/algoready.git
   cd algoready
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/stockmaniacs/algoready.git
   ```

4. **Install dependencies**

   **Backend:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

   **Frontend:**
   ```bash
   cd web
   npm install
   cp .env.example .env.local
   ```

   **Extension:**
   ```bash
   cd extension
   npm install
   ```

5. **Start development services**
   ```bash
   # Start PostgreSQL and Redis
   docker-compose up -d postgres redis

   # Run database migrations
   cd backend
   alembic upgrade head
   ```

6. **Start development servers**
   ```bash
   # Terminal 1: Backend
   cd backend
   uvicorn app.main:app --reload --port 8000

   # Terminal 2: Frontend
   cd web
   npm run dev

   # Terminal 3: Extension (optional)
   cd extension
   npm run dev
   ```

## 🔄 Development Workflow

### Branch Naming

- Feature: `feature/description-of-feature`
- Bug fix: `fix/description-of-bug`
- Documentation: `docs/description-of-changes`
- Refactor: `refactor/description-of-refactor`
- Test: `test/description-of-tests`

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
type(scope): short description

Longer description if needed

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add OAuth 2.0 support for Zerodha
fix(extension): resolve sidepanel width issue on small screens
docs(api): update broker connection endpoints
```

### Keeping Your Fork Updated

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 🎨 Code Style

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use type hints everywhere
- Maximum line length: 100 characters

```bash
# Format code
black .
isort .

# Lint
flake8 .
mypy .
```

### TypeScript/JavaScript (Frontend & Extension)

- Use [ESLint](https://eslint.org/) and [Prettier](https://prettier.io/)
- Follow [Airbnb Style Guide](https://github.com/airbnb/javascript) (modified)
- Use functional components with hooks
- Prefer TypeScript interfaces over types

```bash
# Format code
npm run format

# Lint
npm run lint
```

### General Guidelines

1. **Write self-documenting code** - Use clear variable and function names
2. **Add comments for complex logic** - Explain "why", not "what"
3. **Keep functions small** - Single responsibility principle
4. **Handle errors gracefully** - Never leave empty catch blocks
5. **Write tests for new features** - Aim for >80% coverage

## 🧪 Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

### Frontend Tests

```bash
cd web

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Extension Tests

```bash
cd extension

# Run tests
npm test
```

### Writing Tests

- Place tests in `__tests__` or `tests` directories
- Name test files with `.test.ts` or `_test.py` suffix
- Use descriptive test names: `should_return_user_when_valid_token_provided`
- Test edge cases and error conditions
- Mock external dependencies

## 📥 Pull Request Process

### Before Submitting

1. **Update your branch** with latest main
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all tests** and ensure they pass
   ```bash
   # Backend
   cd backend && pytest
   
   # Frontend
   cd web && npm test
   
   # Extension
   cd extension && npm test
   ```

3. **Run linters** and fix any issues
   ```bash
   # Backend
   cd backend && black . && isort . && flake8 . && mypy .
   
   # Frontend/Extension
   cd web && npm run lint
   ```

4. **Update documentation** if needed

### Submitting the PR

1. Push your branch to your fork
   ```bash
   git push origin feature/your-feature
   ```

2. Open a Pull Request against `stockmaniacs/algoready:main`

3. Fill out the PR template:
   - Description of changes
   - Related issue number
   - Screenshots (for UI changes)
   - Testing steps

### PR Requirements

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Meaningful commit messages
- [ ] Descriptive PR title and description

### Review Process

1. At least one maintainer must approve
2. All CI checks must pass
3. No unresolved conversations
4. Branch must be up to date with main

## 🐛 Issue Reporting

### Bug Reports

Use the bug report template and include:

- **Environment**: OS, browser, Node/Python versions
- **Steps to reproduce**: Clear, numbered steps
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Screenshots**: If applicable
- **Logs**: Relevant error messages

### Good Bug Report Example

> **Title**: [Bug] Sidepanel doesn't load positions on Upstox
>
> **Environment**: Chrome 125, macOS 14.5
>
> **Steps**:
> 1. Connect Upstox account
> 2. Open sidepanel
> 3. Navigate to Positions tab
>
> **Expected**: Positions list displayed
> **Actual**: Empty state shown, console shows 401 error
>
> **Logs**: `GET https://api.upstox.com/v2/portfolio/positions 401`

## 💡 Feature Requests

Use the feature request template and include:

- **Problem**: What problem does this solve?
- **Solution**: Proposed implementation
- **Alternatives**: Other approaches considered
- **Impact**: Who benefits from this?
- **Priority**: Low/Medium/High

## 🏷️ Labels

We use the following labels:

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or improvement |
| `documentation` | Documentation updates |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `priority: high` | Critical priority |
| `priority: medium` | Normal priority |
| `priority: low` | Low priority |
| `status: needs triage` | Not yet reviewed |
| `status: in progress` | Being worked on |
| `status: blocked` | Blocked by external factor |

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [Chrome Extension Docs](https://developer.chrome.com/docs/extensions/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

Thank you for contributing to AlgoReady! 🚀