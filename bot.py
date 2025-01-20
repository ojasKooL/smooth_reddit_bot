import praw
import requests
from groq import Groq
import re
import random
import schedule
import time  # Required to keep the script running for scheduling
from dotenv import load_dotenv
import os

# Load ENV
load_dotenv()

client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")
user_agent = os.getenv("REDDIT_USER_AGENT")
groq_api_key = os.getenv("GROQ_API_KEY")

if not all([client_id, client_secret, username, password, user_agent, groq_api_key]):
    raise ValueError("One or more Reddit credentials are missing in the environment variables.")

# Reddit Setup
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, username=username, password=password, user_agent=user_agent)

def find_top_posts(subreddit):
    try:
        response = requests.get(f'https://www.reddit.com/{subreddit}/hot.json', headers={'User-agent': '<console:smooth:1.0>'})
        response.raise_for_status()
        data = response.json()

        final = []
        for i in data['data']['children']:
            final.append("Title: " + i['data']['title'] + "     Self Text: " + i['data']['selftext'] + "   Flair:" + i['data']['link_flair_text'])
        return final[:3]
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return []

def make_post_content(subreddit, flair, posts):
    rules = ""
    i = 1
    for rule in reddit.subreddit(subreddit.split('/')[-1]).rules:
        rules += f"{i}. {rule} \n"
        i += 1

    client = Groq(
        api_key=groq_api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"Write a title and selftext for a Reddit post on the subreddit {subreddit} with the flair {flair}. "
                    "Use friendly and human-like language, incorporating Gen Z lingo if it fits naturally, but ensure the post remains respectful. "
                    "Avoid starting with generic or robotic phrases like 'Hey fellow Redditors' or 'Hello everyone.' "
                    "The post must comply with the following subreddit rules: \n"
                    f"{rules}\n"
                    "Additionally, here are some latest posts from the subreddit {subreddit} to give you a better understanding of its tone and context: \n"
                    f"{posts} "
                    "Your response should be unique and not a repost or a paraphrase of the provided examples. "
                    "The response should follow this exact format:\n"
                    "'TITLE: <title here>' \n'SELFTEXT: <selftext here>'. "
                    "Ensure you use these exact keywords: 'TITLE' and 'SELFTEXT' to distinguish the two parts clearly."
        }],
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    return chat_completion.choices[0].message.content

def extract_title_and_selftext(response_content):
    # Use regex to detect pattern
    pattern = r"TITLE:\s*(.*?)\nSELFTEXT:\s*(.*)"
    match = re.search(pattern, response_content, re.DOTALL)
    if match:
        title = match.group(1).strip()
        selftext = match.group(2).strip()
        return {"title": title, "selftext": selftext}
    else:
        return None

def choose_flair(chosen_subreddit):  # Choose flair randomly from available flairs else return None
    subreddit = reddit.subreddit(chosen_subreddit.split('/')[-1])
    try:
        flairs = list(subreddit.flair.link_templates)
        if not flairs:
            return None, None
        while True:
            chosen_flair = random.choice(flairs)
            if chosen_flair["text"] != "Poll":
                return chosen_flair["id"], chosen_flair["text"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def post_to_reddit():  # Post to reddit from given set of subreddits
    subreddits = [
        "r/testingground4bots"
    ]
    chosen_subreddit = random.choice(subreddits)
    print(f"Chosen subreddit: {chosen_subreddit}")
    posts = find_top_posts(chosen_subreddit)
    flair_id, flair_text = choose_flair(chosen_subreddit)
    if not posts:
        print("No posts found or failed to fetch posts.")
        return

    response_content = make_post_content(chosen_subreddit, flair_text, posts)
    post_data = extract_title_and_selftext(response_content)

    if flair_id is not None:
        print("Flair ID: ", flair_id)
        print("Flair Text: ", flair_text)
        submission = reddit.subreddit(chosen_subreddit.split('/')[-1]).submit(title=post_data['title'], selftext=post_data['selftext'], flair_id=flair_id)
        print(f"Post created successfully in {chosen_subreddit} with flair '{flair_text}': {submission.url}")
    else:
        print("No flairs available for the subreddit.")
        submission = reddit.subreddit(chosen_subreddit.split('/')[-1]).submit(title=post_data['title'], selftext=post_data['selftext'])
        print(f"Post created successfully in {chosen_subreddit} without a flair: {submission.url}")

def comment_on_top_post(subreddit_name):
    try:
        # Access the subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Fetch the top 5 posts
        top_posts = list(subreddit.new(limit=5))
        post_index = random.randint(0,4)
        # Choose the first post
        post_to_comment = top_posts[post_index]

        print(post_to_comment.title)
        print(post_to_comment.selftext)

        client = Groq(
            api_key="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",
        )

        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": f"Write a short, snappy, and respectful comment on the provided Reddit post. Post Title: {post_to_comment.title} Post SelfText: {post_to_comment.selftext}. The comment should sound human, casual, and genuinely engage with the post's content. Avoid robotic or generic replies—think of a real person contributing to the conversation. Add something that enhances the discussion, like asking a question, sharing a thought, or giving constructive feedback. Don't start with formal greetings or end with 'thanks'—just a natural flow that makes the comment feel like part of the discussion."
            }],
            model="llama-3.3-70b-versatile",
            stream=False,
        )

        comment_text = chat_completion.choices[0].message.content
        print(f"Comment: {comment_text}")
        # Add the comment
        post_to_comment.reply(comment_text)
        print(f"Commented on post: {post_to_comment.title}")
    except Exception as e:
        print(f"An error occurred: {e}")

import random
import schedule
import time
from datetime import datetime, timedelta

def random_time_daily():
    # Generate a random hour and minute
    hour = random.randint(0, 23)  # Hour in 24-hour format
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

def get_next_day_random_time():
    # Generate a random time for the next day that's greater than the current time
    now = datetime.now()
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    
    # If generated time is earlier than current time, adjust it to the next day
    if hour < now.hour or (hour == now.hour and minute <= now.minute):
        next_day = now + timedelta(days=1)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
    
    next_time = f"{hour:02d}:{minute:02d}"
    return next_time

def random_time_monday():
    # Generate a random hour and minute for Monday posting
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}:{minute:02d}"

random_time = get_next_day_random_time()
print(f"Scheduled daily commenting time: {random_time}")
schedule.every().day.at(random_time).do(comment_on_top_post, subreddit_name="AskReddit")

random_post_time = random_time_monday()
print(f"Scheduled posting time on Monday: {random_post_time}")
schedule.every().monday.at(random_post_time).do(post_to_reddit)

while True:
    schedule.run_pending()
    time.sleep(1)



