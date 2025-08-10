# ADR-0005: FastAPI response models and typed handlers

Status: Accepted

## Context

We enforce strict type hints and want clear API contracts. Returning JSONResponse everywhere makes it easier to diverge from the schema and complicates type checking.

## Decision

- Route handlers return Pydantic models directly; FastAPI handles serialization and response validation.
- All routes declare `response_model` where applicable.
- Keep request/response DTOs in the same module initially; split if/when the surface grows.

## Consequences

- Clearer, self-documenting contracts and better editor/type-checker support.
- Tests assert on plain JSON without coupling to JSONResponse.
- Refactor completed in `src/bjjsim/web/app.py` to return models and annotate response models.

## Alternatives considered

- Continue returning JSONResponse explicitly. Rejected for weaker contracts and extra boilerplate.
