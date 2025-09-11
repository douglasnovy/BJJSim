#!/usr/bin/env python3
"""
Main entry point for BJJSim web application.
Configured for Replit environment.
"""

import os

import uvicorn

from bjjsim.web.app import create_app

if __name__ == "__main__":
    app = create_app()
    # Configure for Replit environment: bind to all interfaces, use PORT env var if available
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True,
    )