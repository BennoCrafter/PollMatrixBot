  # PollMatrixBot
  [![simplematrixbotlib][simplematrixbotlib]][Simplematrixbotlib-url]

  A handy bot for creating and managing polls in Matrix rooms.

  ## Features

  - !create title: Create a new poll with the specified title.
  - !close: Close the current poll.
  - !remove <item>: Remove the given item from the poll.
  - !list: List all items currently in the poll.
  - !add <item>: Add a new item to the poll (if enabled in the configuration).
  - !help: Display the help message with available commands.

  ## Setup

  Follow these steps to set up your Matrix Poll Bot:

  ### Note
  Make sure you invite the user first when the bot is running. Otherwise the Bot will not join the given room.

  ### 1. Create a New Matrix Account

  1. Go to [Matrix.org](https://matrix.org) and sign up for a new account.
  2. Note down your username and password. You will need these for the bot configuration.

  ### 2. Clone the Repository

  ```bash
  git clone https://github.com/bennocrafter/pollmatrixbot.git
  cd PollMatrixBot
  ```

  ### 4. Configure Environment Variables
  Create a .env file in the root of your project directory and add the following credentials:

  ```makefile
  USERNAME=your-matrix-username
  PASSWORD=your-matrix-password
  HOMESERVER=your-matrix-homeserver

  ```

  ### 5. Build and Start the Bot Using Docker Compose
  To build and start the bot using Docker Compose, run the following command from the root of your project directory:

  ```bash
  docker-compose up -d
  ```
  This will build the Docker image (if it hasn't been built yet) and start the container in detached mode.

    ### Commands

  The Matrix Poll Bot supports the following commands:

  #### !create title
  Create a new poll with the specified title.

  #### !close
  Close a poll and get a status report sent.

  #### !remove <item>
  Remove the given item from the poll.

  [simplematrixbotlib]: https://img.shields.io/badge/Framework-simplematrixbotlib-blue
  [Simplematrixbotlib-url]: https://codeberg.org/imbev/simplematrixbotlib

  ### Run without Docker

  ###  Install Dependencies
  Make sure you have Python and pip installed. Then, install the required packages:

  ```bash
  pip install -r requirements.txt
  ```

  ### Run main.py
  Just run the `main.py` file.
  ```bash
  python main.py
  ```
