# pyenvtools

> Simple tool for environment variables

### Features

- Dumping environments
- Joining .env files to one string
- Generating environment activation scripts from .env files

### Installation

```bash
pip install pyenvtools
```

### Usage

```bash
# Dump environment
python -m pyenvtools dump

# Dump environment to file
python -m pyenvtools dump .env

# Join .env file
python -m pyenvtools join .env

# Generate script
python -m pyenvtools script .env
```