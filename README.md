# Smooth - Reddit Bot
This Reddit bot is designed to post content, comment on top posts, and interact with Reddit communities using Groq for natural language generation. It includes scheduling functionality to make random posts and comments at set intervals.

## Features

- **Post to Subreddit**: Creates posts on a chosen subreddit.
- **Comment on Top Posts**: Generates and posts random comments on top posts from a specific subreddit.
- **Scheduling**: Posts and comments are scheduled at random times, including weekly posts on Mondays.
- **Groq Integration**: Uses Groq API to generate content for posts and comments.

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine.

```bash
git clone https://github.com/ojasKooL/smooth_reddit_bot.git
cd smooth_reddit_bot
```

### 2. Install Dependencies

Make sure you have Python 3.6+ installed. You will need to install the required Python libraries. Use `pip` to install them:

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the root directory of the project. This file will store your sensitive API keys and credentials. Here's an example `.env` file:

```plaintext
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=python:smoothposterbot:v1.0 (by u/RecipeNo4290)
GROQ_API_KEY=your_groq_api_key
```

Make sure to replace the placeholders with your actual credentials.

### 4. Create a `requirements.txt`

The required libraries for the project:

```plaintext
praw
requests
groq
schedule
python-dotenv
```

### 5. Run the Bot

After setting up your environment and `.env` file, you can run the bot:

```bash
python bot.py
```

The bot will now:
- Post to a random subreddit at a randomly chosen time.
- Comment on top posts of a chosen subreddit at a randomly chosen time.
- Follow the defined schedule.

### 6. Scheduling

The bot is set up to run tasks at random times:
- **Daily Commenting**: A random time each day.
- **Monday Posting**: A random time on Monday.

The bot uses the `schedule` library to manage task scheduling.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
