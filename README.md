# Internal Developer Platform 🚀

Started this to learn FastAPI and K8s client libraries. Tired of waiting for ops to create namespaces every time I need to test something.

## What it does

Basic internal platform for dev teams:
- Self-service namespace creation in K8s
- JWT auth for users (still needs work)
- Basic CRUD for resources
- Integrates with Vault for secrets (WIP)
- Terraform for some infra bits

## Quick Start ⚡

```bash
# Setup (might need to fix the venv path)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on windows

# Install deps
pip install -r requirements.txt

# Run it
python -m uvicorn app.main:app --reload
```

Then go to `localhost:8000/docs` for the API docs.

## Features

- User auth with JWT (kinda works)
- Multi-tenant namespace isolation
- K8s namespace provisioning
- Basic secret management 🔒
- API rate limiting (needs tuning)
- Docker & docker-compose setup

## Architecture

It's a FastAPI app with:
- PostgreSQL for users/namespaces (SQLAlchemy)
- Redis for caching (optional)
- K8s client for namespace ops
- Vault integration for secrets

```
Frontend (basic) -> FastAPI -> [PostgreSQL, Redis, K8s, Vault]
```

## TODO

Lots of stuff missing:
- [ ] Proper error handling
- [ ] More tests (coverage is like 40%)
- [ ] Frontend UI (just API for now)
- [ ] Better logging
- [ ] CI/CD pipeline
- [ ] Documentation (this README is most of it)

## Known Issues

- Auth middleware sometimes breaks
- K8s client timeout needs adjustment
- Database migrations are manual (alembic setup but not automated)
- No proper monitoring yet

## Notes

The K8s client integration was trickier than expected. Had to mess with service accounts and RBAC for a while before it worked. Not sure if this is the best approach but it's functional.

Based on some blog posts and the FastAPI docs, but adapted for our use case. The JWT implementation is basic - should probably use proper OAuth2 flows but this works for now.

Started in Nov 2023, been adding bits when I have time between work projects. The terraform part is experimental, might remove it if it becomes too complex.

---

*Last updated: April 2024* (still needs work but it runs)# Test
