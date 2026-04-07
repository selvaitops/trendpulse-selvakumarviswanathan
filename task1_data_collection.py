import requests
import time
import json
import os
from datetime import datetime

categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

main_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
headers = {"User-Agent": "TrendPulse/1.0"}

collected_data = []

try:
    # First get top story data
    response = requests.get(main_url, headers=headers)
    story_ids = response.json()[:500]

    # Per category loop
    for category in categories:
        
        count = 0
        print(category)

        for story_id in story_ids:
            print(story_id)

            if count >= 25:
                break

            item_url = "https://hacker-news.firebaseio.com/v0/item/" + str(story_id) + ".json"

            try:
                story_response = requests.get(item_url, headers=headers)
                story = story_response.json()

                # skipping no data and no title word exist in response data
                if not story or 'title' not in story:
                    continue

                
                title = story['title'].lower()

                # keyword find check
                match = False
                for keyword in categories[category]:
                    if keyword in title:
                        match = True
                        break

                if not match:
                    continue

                # Fetching required fields  mentioned in task
                content = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(content)
                count += 1

                print(f"Fetched {count} stories for {category}")

            except Exception as e:
                print(f"Error in fetching {story_id} story: {e}")

        

        # Sleep once per category
        time.sleep(2)

    #Saving data under data/trends_*
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected: {len(collected_data)} stories. Saved to {filename}")

except Exception as e:
    print("Error fetching top stories:", e)