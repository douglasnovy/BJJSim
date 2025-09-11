# BJJSim - Brazilian Jiu-Jitsu Simulation

## Project Overview
BJJSim is a Python FastAPI web application that provides a simulation framework for Brazilian Jiu-Jitsu multi-agent self-play scenarios. The project is currently in the UI skeleton phase with a working web interface and API endpoints.

## Current Status
- **Phase**: UI skeleton implementation complete
- **Version**: 0.0.4
- **Framework**: FastAPI with Uvicorn server
- **Frontend**: HTML templates with Jinja2
- **Physics**: Deterministic counter adapter (placeholder for future PyBullet integration)

## Project Structure
```
├── src/bjjsim/
│   ├── web/
│   │   ├── app.py           # Main FastAPI application
│   │   └── templates/       # HTML templates
│   └── physics/
│       ├── adapter.py       # Physics adapter interface and implementation
│       └── __init__.py
├── tests/                   # Test suite
├── docs/                    # Sphinx documentation
├── scripts/                 # PowerShell setup scripts
├── main.py                  # Replit entry point
└── pyproject.toml          # Project configuration
```

## Replit Configuration
- **Host**: 0.0.0.0 (configured for Replit proxy)
- **Port**: 5000 (required for Replit)
- **Workflow**: "BJJSim Web Server" - runs `python main.py`
- **Deployment**: Configured for autoscale deployment target

## Available Endpoints
- `GET /` - Main dashboard page
- `POST /api/sim/reset` - Reset simulation with optional seed
- `POST /api/sim/start` - Start episode
- `POST /api/sim/stop` - Stop episode  
- `POST /api/sim/step` - Advance simulation by steps
- `GET /api/sim/state` - Current simulation state
- `GET /api/frames/current` - Current frame (PNG placeholder)
- `GET /api/metrics` - Server metrics
- `WS /ws/events` - WebSocket events stream
- `GET /healthz` - Health check
- `GET /readyz` - Readiness check
- `GET /api/config` - Runtime configuration
- `POST /api/config` - Update configuration

## Development Setup
The project uses Python 3.12 with strict type checking (mypy) and modern formatting (ruff). All dependencies are managed through pyproject.toml.

### Key Dependencies
- FastAPI >= 0.111.0 - Web framework
- Uvicorn >= 0.30.0 - ASGI server
- Pydantic >= 2.7.0 - Data validation
- Jinja2 >= 3.1.4 - Template engine
- Pillow >= 10.3.0 - Image processing
- Playwright >= 1.46.0 - E2E testing

## Testing
The project includes a comprehensive test suite with both API and end-to-end testing:

### Test Coverage
- **API Tests**: Complete coverage of all FastAPI endpoints (10 tests)
  - Simulation control (reset, start, stop, step)
  - State management and metrics
  - Frame generation (PNG encoding)
  - WebSocket event streaming
  - Configuration management
  - Health and readiness checks

- **E2E Tests**: Playwright browser-based testing (1 test)
  - Dashboard UI interaction testing
  - Control button functionality verification
  - Automatically skipped in Replit environment (browsers not available)

### Running Tests
```bash
# Run all tests (E2E test will be skipped locally)
pytest tests/ -v

# Run only API tests
pytest tests/test_web_app.py -v

# Run physics adapter tests
pytest tests/test_physics_adapter.py -v
```

**Note**: E2E tests require Playwright browsers and are designed to run in CI environments. In local development (including Replit), these tests are automatically skipped.

## Recent Changes
- **2025-09-11**: Imported to Replit environment
  - Created main.py entry point configured for Replit (0.0.0.0:5000)
  - Fixed physics adapter protocol compliance issues
  - Set up workflow for web server
  - Configured autoscale deployment
  - All dependencies installed and working
  - Validated comprehensive test suite (10/11 tests passing, 1 E2E skipped as expected)

## Future Milestones
The project roadmap includes:
1. PyBullet physics integration
2. Multi-agent Gymnasium environment
3. Hierarchical reward system
4. RLlib PPO self-play training
5. GUI debugging interface

## Architecture Notes
The application uses a clean architecture with:
- Protocol-based physics adapter interface (future PyBullet support)
- FastAPI with dependency injection pattern
- Type-safe Pydantic models for all API contracts
- Template-based frontend with WebSocket real-time updates
- Comprehensive test suite with Playwright E2E tests

The current deterministic counter adapter serves as a placeholder while the actual physics simulation is developed in future phases.