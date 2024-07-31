# PollMatrixBot
[![simplematrixbotlib][simplematrixbotlib]][Simplematrixbotlib-url]

A handy bot for creating and managing polls in Matrix rooms.

## Features

- **!create title**: Create a new poll with the specified title.
- **!close**: Close the current poll.

## Setup

Follow these steps to set up your Matrix Poll Bot:

### 1. Create a New Matrix Account

1. Go to [Matrix.org](https://matrix.org) and sign up for a new account.
2. Note down your username and password. You will need these for the bot configuration.

### 2. Clone the Repository

```bash
git clone https://github.com/bennocrafter/pollmatrixbot.git
cd PollMatrixBot
```

### 3. Install Dependencies
Make sure you have Python and pip installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root of your project directory and add the following credentials:

```makefile
USERNAME=your-matrix-username
PASSWORD=your-matrix-password
HOMESERVER=your-matrix-homeservet

```

### Note
Make sure you invite the user first when the bot is running. Otherwise the Bot will not join the given room.

### 5. Run main.py
Just run the `main.py` file.
```bash
python main.py
```

### Commands

The Matrix Poll Bot supports the following commands:

#### !create title
Create a new poll with the specified title.
 
#### !close
Close a poll and get a status report sent.

 
Made for denkbares

[simplematrixbotlib]: https://img.shields.io/badge/Framework-simplematrixbotlib-blue
[Simplematrixbotlib-url]: https://codeberg.org/imbev/simplematrixbotlib
