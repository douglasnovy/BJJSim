# BJJSim - Brazilian Jiu-Jitsu Simulation

## Project Overview

BJJSim is a Python FastAPI web application that provides a simulation framework for Brazilian Jiu-Jitsu multi-agent self-play scenarios. The project now includes a fully functional multi-agent Gymnasium environment with hierarchical reward system and physics adapter integration.

## Current Status

- **Phase**: **Phase 2 Complete** ✅ - Environment and Rewards implemented
- **Version**: 0.1.0  
- **Framework**: FastAPI with Uvicorn server
- **Frontend**: HTML templates with Jinja2 + real-time WebSocket updates
- **Environment**: Multi-agent Gymnasium environment with hierarchical rewards
- **Physics**: Deterministic counter adapter (validated, ready for Phase 3 PyBullet integration)

## Project Structure

```text
├── src/bjjsim/
│   ├── web/
│   │   ├── app.py           # Main FastAPI application
│   │   └── templates/       # HTML templates
│   ├── env/
│   │   ├── bjj_env.py       # Multi-agent Gymnasium environment
│   │   └── __init__.py      # Environment module exports
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
- Gymnasium >= 0.29.0 - Multi-agent environment framework
- NumPy >= 1.26.0 - Numerical computing for observations and actions

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

- **2025-09-11**: **Phase 2 Complete** ✅ - Environment and Rewards implemented
  - **Multi-agent Gymnasium Environment**: Two-agent BJJ simulation with proper observation/action spaces
  - **Hierarchical Reward System**: Choke submissions (+30), hyperextension (+20), top control (+10), contact control (+5), energy penalty (-0.1)
  - **Physics Integration**: DeterministicCounterAdapter working, ready for PyBullet integration
  - **Dependency Resolution**: Successfully installed numpy and gymnasium with proper system library support
  - **Comprehensive Testing**: Environment lifecycle, reward tracking, and multi-step execution validated
  - **Type Safety**: Full mypy compliance with proper conditional imports and error handling
  - **Web Server Integration**: All API endpoints responding correctly with environment metrics
  - **Ready for Phase 3**: Multi-agent training and policy development

- **2025-09-11**: Initial import to Replit environment
  - Created main.py entry point configured for Replit (0.0.0.0:5000)
  - Fixed physics adapter protocol compliance issues
  - Set up workflow for web server
  - Configured autoscale deployment
  - All dependencies installed and working
  - Validated comprehensive test suite (10/11 tests passing, 1 E2E skipped as expected)
  - **Added comprehensive formatting prevention system**:
    - Created `.editorconfig` for consistent editor settings
    - Created `.gitattributes` for line ending normalization
    - Updated `.gitignore` to exclude ephemeral `attached_assets/` files
    - Updated pre-commit config to exclude problematic files and latest hook versions
    - Enhanced CONTRIBUTING.md with detailed formatting guidelines

## Future Milestones (Phase 3+)

The project roadmap includes:

1. **Phase 3**: PyBullet physics integration
2. **Phase 4**: RLlib PPO self-play training
3. **Phase 5**: Advanced policy architectures
4. **Phase 6**: GUI debugging interface
5. **Phase 7**: Performance optimization and scaling

## Architecture Notes

The application uses a clean architecture with:

- Protocol-based physics adapter interface (future PyBullet support)
- FastAPI with dependency injection pattern
- Type-safe Pydantic models for all API contracts
- Template-based frontend with WebSocket real-time updates
- Comprehensive test suite with Playwright E2E tests

The current deterministic counter adapter serves as a placeholder while the actual physics simulation is developed in future phases.
