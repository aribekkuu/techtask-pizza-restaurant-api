FROM python:3.10-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --no-dev

# Copy project files
COPY .. /techtask

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

COPY . .
