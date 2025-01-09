# PollMatrixBot

[![simplematrixbotlib][simplematrixbotlib]][simplematrixbotlib-url]

A handy bot for creating and managing polls in Matrix rooms.

## Features

* **!create title:** Create a new poll with the specified title.
* **!close:** Close the current poll.
* **!remove <item>:** Remove the given item from the poll.
* **!list:** List all items currently in the poll.
* **!add <item>:** Add a new item to the poll (if enabled in the configuration).
* **!help:** Display the help message with available commands.

## Installation

### Prerequisites

* A Matrix account (Sign up at [Matrix.org](https://matrix.org))
* Python 3.x

### Using Docker Compose (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/bennocrafter/pollmatrixbot.git
   cd PollMatrixBot
   ```

2. (Recommended) Build the Docker image:

```bash
docker-compose build
```

3. Start the bot in detached mode:
```bash
docker-compose up -d
```

### Running without Docker (Not Recommended)

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Run the main script:

```bash
python main.py
```

## Commands
The Matrix Poll Bot supports the following commands:

- **!create title**: Creates a new poll with the specified title.
- **!close**: Closes the current poll and displays a status report.
- **!remove <item>**: Removes the given item from the current poll (if enabled).
- **!list**: Lists all options currently available in the poll.
- **!add <item>**: Adds a new option to the current poll (if enabled, configurable).
- **!help**: Displays the help message with available commands.

## Configuration
Create a ```.env``` file in the project's root directory with the following environment variables:

```makefile
USERNAME=your-matrix-username
PASSWORD=your-matrix-password
HOMESERVER=your-matrix-homeserver
```

Configure other things in ```assets/config.yaml```


[simplematrixbotlib]: https://img.shields.io/badge/Framework-simplematrixbotlib-blue
[simplematrixbotlib-url]: https://codeberg.org/imbev/simplematrixbotlib
