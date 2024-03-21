# Recruitment Service Python

This is a recruitment service implemented in Python.

## Getting Started

### Prerequisites

- Python 3.9.0
- Docker

### Install dependencies

For Linux and macOS:

```bash
# Change directory
cd recruitment-service-python

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

For Windows:

```bash
# Change directory
cd recruitment-service-python

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Set environment variables

Copy the .env.example file to .env and set the environment variables.

## Run tests

```bash
pytest
```

## Start the application

```bash
docker compose up -d
```
