# Base Image: Lightweight Python
FROM python:3.9-slim

# Security: Create non-root user
RUN useradd -m -s /bin/bash subject

# Environment Setup
WORKDIR /app

# Sterility: No internet access by default (Enforced by Docker network=none at runtime)
# Clean slate
RUN rm -rf /tmp/*

# Switch to low-privilege user
USER subject

# Entry point (can be overridden by controller)
CMD ["python", "--version"]
