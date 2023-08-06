# Configonaut

Configonaut is a Python library for handling JSON configuration files. It provides an intuitive and simple way to access, modify, and save configurations stored in JSON format.

## Installation

Install Configonaut with pip:

```bash
pip install configonaut
```

## Usage

```python
from configonaut import Configonaut

# Create a new configuration
config = Configonaut('config.json')

# Access configuration
db_config = config['database']

# Modify configuration
db_config['host'] = 'localhost'
db_config['port'] = 5432

# Save configuration
db_config.save()
```

## Features

- Simple and intuitive access to configuration items.
- Automatic saving of modifications.
- Ability to navigate through the configuration hierarchy.

## License

Configonaut is licensed under the MIT License. See [LICENSE](LICENSE) for more details.