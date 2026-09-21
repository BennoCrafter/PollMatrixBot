<p align="center">
  <img src="assets/icon/icon_round.png" width="150" height="150" alt="Lunchy Logo">
</p>

<div align="center">
  <h1>Poll Matrixbot</h1>

  **A handy bot for creating and managing polls in Matrix rooms.**

  [![Stars](https://img.shields.io/github/stars/BennoCrafter/PollMatrixBot?style=social)](https://github.com/BennoCrafter/PollMatrixBot)
  [![Forks](https://img.shields.io/github/forks/BennoCrafter/PollMatrixBot?style=social)](https://github.com/BennoCrafter/PollMatrixBot)
  [![Open Issues](https://img.shields.io/github/issues/BennoCrafter/PollMatrixBot)](https://github.com/BennoCrafter/PollMatrixBot/issues)
  [![Last Updated](https://img.shields.io/github/last-commit/BennoCrafter/PollMatrixBot)](https://github.com/BennoCrafter/PollMatrixBot/commits/main)
  [![simplematrixbotlib][simplematrixbotlib]][simplematrixbotlib-url]
</div>

---

## Overview

Poll Matrixbot (a.k.a. *Lunchy*) is your perfect Matrix bot for running polls with friends or teams — perfect for deciding lunch spots or anything else that needs a quick team decision.

---

## Commands

| Command | Description | Example |
|----------|--------------|----------|
| `!lunchy <name>` | Start a new poll | `!lunchy Pizza Day` |
| `!add <quantity>x <item>` | Add an item to the poll | `!add 2x Pepperoni Pizza` |
| `!remove <quantity>x <item>` | Remove an item from the poll | `!remove 1x Garlic Bread` |
| `!status` | Show all items currently in the poll | `!status` |
| `!nothing` | Mark that you’re not joining the poll | `!nothing` |
| `!noblame` | Disable blame message for the pay reminder | `!noblame` |
| `!close` | Close the active poll | `!close` |
| `!reopen` | Reopen the most recently closed poll | `!reopen` |
| `!releasenotes` | View the bot’s latest release notes | `!releasenotes` |
| `!help` | Display all available commands | `!help` |

---

## Installation

### Prerequisites

* A Matrix account (Sign up at [Matrix.org](https://matrix.org))
* Python 3.x

### Using Docker Compose

1. Clone the repository:

   ```bash
   git clone https://github.com/bennocrafter/pollmatrixbot.git
   cd PollMatrixBot
   ```

2. Build the Docker image:

```bash
docker-compose build
```

3. Start the bot in detached mode:
```bash
docker-compose up -d
```

### Running without Docker

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

```makefile
HOMESERVER="" # required
# use username and password for auth
USERNAME=""
PASSWORD=""
# or using an acess token
ACCESS_TOKEN=""

# optional openai intergration for ai features
OPENAI_BASE_URL=""
OPENAI_API_KEY=""

```

or have a look at ```.env.example```

Use password or access token to authenticate

Configure other things in ```assets/config.yaml```


[simplematrixbotlib]: https://img.shields.io/badge/Framework-simplematrixbotlib-blue
[simplematrixbotlib-url]: https://codeberg.org/imbev/simplematrixbotlib
