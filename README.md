<p align="center">
  <img src="assets/RoundedIcon.png" width="150" height="150" alt="Posterfy Logo">
</p>

<div align="center">
    <h1>Poll Matrixbot 📊</h1>
  
    **A handy bot for creating and managing polls in Matrix rooms.**

  
   [![Stars](https://img.shields.io/github/stars/BennoCrafter/TrackStar?style=social)](https://github.com/BennoCrafter/TrackStar)
   [![Forks](https://img.shields.io/github/forks/BennoCrafter/TrackStar?style=social)](https://github.com/BennoCrafter/TrackStar)
   [![Open Issues](https://img.shields.io/github/issues/BennoCrafter/TrackStar)](https://github.com/BennoCrafter/TrackStar/issues)
   [![Last Updated](https://img.shields.io/github/last-commit/BennoCrafter/TrackStar)](https://github.com/BennoCrafter/TrackStar/commits/main)
   [![simplematrixbotlib][simplematrixbotlib]][simplematrixbotlib-url]
</div>

## Features

* **!create <title>:** Create a new poll with the specified title.
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

## Configuration
Create a ```.env``` file in the project's root directory with the following environment variables:
Use password or access token to authenticate

```makefile
HOMESERVER=your-matrix-homeserver
USERNAME=your-matrix-username
PASSWORD=your-matrix-password
ACCESS_TOKEN=your-matrix-access-token
```

Configure other things in ```assets/config.yaml```


[simplematrixbotlib]: https://img.shields.io/badge/Framework-simplematrixbotlib-blue
[simplematrixbotlib-url]: https://codeberg.org/imbev/simplematrixbotlib
