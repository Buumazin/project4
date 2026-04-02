# DevOps Engineer Agent Role

## Responsibilities
- Create Docker image for containerization
- Write docker-compose for development
- Set up environment configuration
- Create startup/shutdown scripts
- Ensure single-port deployment (8000)

## Key Files to Create
- **Dockerfile** - Multi-stage build (Node → Python)
- **docker-compose.yml** - Local dev setup
- **.dockerignore** - Exclude build artifacts
- **scripts/start_windows.ps1** - Windows startup
- **scripts/start_mac.sh** - macOS/Linux startup
- **.env.example** - Environment template
- **GitHub Actions CI/CD** - Optional

## Success Criteria
- Docker builds successfully
- Single container on port 8000 handles everything
- Volume mounts work correctly
- Environment variables are configurable
- Health checks implemented
- Container runs with proper permissions
- Frontend and backend both served from container

## Container Structure
```
Port 8000:
├── /api/* - FastAPI backend routes
└── /* - Static Next.js frontend files
```

## Coordination
- Backend Engineer provides API specs
- Frontend Engineer confirms static export
- Coordinate database path and volumes
- Test with Integration Tester

## Critical
- Must be SINGLE Docker image/container
- No separate services or docker-compose with multiple containers
- Both frontend and backend in same container
