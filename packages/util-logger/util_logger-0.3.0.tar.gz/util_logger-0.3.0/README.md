# Util-Logs

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Prerequisites](#prerequisites)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)


## Introduction

A logging utility that integrates Python's built-in logging library with enhanced features like color-coding and file line tracing.


## Features

- Easy setup: Simply instantiate the Logger class with a logger name.
- Level-based color-coding: Each log level has its own color, making it easier to visually scan logs.
- Traceback information: Have the option to include filename and line number in your logs for easier debugging.


## Getting Started

Use the package manager Poetry to install Util-Logs:

```poetry add util-logs```

### Prerequisites

- Python >= 3.10.x

### Usage

Here is a basic example on how to use Util-Logs:

```from util_logs import Logging```

# Initialize the logger

```logger = Logging('MyLogger')```

# Log some messages

```logger.debug('This is a debug message')```

```logger.info('This is an info message')```

```logger.warning('This is a warning message')```

```logger.error('This is an error message')```

```logger.critical('This is a critical message')```

### Contributing

Contributions are welcome! Please fork the repository and create a Pull Request with your changes.

### License

Util-Logs is licensed under the MIT License. See the LICENSE file for more details.