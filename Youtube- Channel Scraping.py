#!/usr/bin/env python
# coding: utf-8

# In[3]:


def get_channel_id_from_url(channel_url):
    if channel_url.startswith("https://www.youtube.com/channel/"):
        channel_id = channel_url.split("/channel/", 1)[1]
    elif channel_url.startswith("https://www.youtube.com/user/"):
        channel_id = channel_url.split("/user/", 1)[1]
    else:
        channel_id = None
        print("Invalid YouTube channel URL")
    return channel_id

# Replace the placeholder URL with your own YouTube channel URL
your_channel_url = "https://www.youtube.com/your-channel"

# Call the function with your channel URL
channel_id = get_channel_id_from_url(your_channel_url)
print("Channel ID:", channel_id)


# In[18]:


import csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up your API credentials and create a YouTube Data API client
api_key = "PUT YOUR API KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

# Specify the channel ID
channel_id = "CHECK CHANNEL ID USING INSPECT OR PAGE SOURCES"

# Set the maximum number of results per page and initialize variables
max_results = 500
videos = []

try:
    # Fetch the video details from the channel
    next_page_token = None
    while True:
        playlist_items = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=max_results,
            pageToken=next_page_token
        ).execute()

        video_ids = []
        for item in playlist_items['items']:
            if 'videoId' in item['id']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_views = "N/A"  # Views not available in the search results
                video_date = item['snippet']['publishedAt']

                # Fetch the duration of each video using the video ID
                video_response = youtube.videos().list(
                    part='contentDetails',
                    id=video_id
                ).execute()

                duration = video_response['items'][0]['contentDetails']['duration']

                # Fetch the comments for each video using the video ID
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText'
                ).execute()

                comments = [comment['snippet']['topLevelComment']['snippet']['textDisplay'] for comment in comments_response['items']]

                videos.append({
                    'Video ID': video_id,
                    'Title': video_title,
                    'Views': video_views,
                    'Duration': duration,
                    'Date': video_date,
                    'Comments': comments
                    # Add other desired metrics here
                })

                video_ids.append(video_id)

        next_page_token = playlist_items.get('nextPageToken')

        if not next_page_token:
            break

    # Save the video details to a CSV file
    csv_file = 'youtube_videos.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Video ID', 'Title', 'Views', 'Duration', 'Date', 'Comments']  # Add other desired metric fieldnames
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(videos)

    print(f"Video details have been scraped and saved to '{csv_file}'.")

except HttpError as e:
    print("An HTTP error occurred:")
    print(e)


# In[21]:


##Analyze youtube channel dimension like engagement metrics

import pandas as pd

csv_file = 'youtube_videos.csv'

# Load video details from CSV file into a pandas DataFrame
videos_df = pd.read_csv(csv_file)

# Convert the 'Comments' column to numeric type, ignoring errors for non-numeric values
videos_df['Comments'] = pd.to_numeric(videos_df['Comments'], errors='coerce')

# Sort videos by number of comments in descending order
videos_sorted = videos_df.sort_values('Comments', ascending=False)

# Display top 20 videos with highest number of comments in a table
top_20 = videos_sorted.head(20)[['Title', 'Comments']]
top_20.index = top_20.index + 1  # Start index at 1 instead of 0
top_20.columns = ['Video Title', 'Number of Comments']
print(top_20.to_string(index=False))


# In[22]:


# Sort video based on view

# Read the CSV file into a DataFrame
df = pd.read_csv('youtube_videos.csv')

# Sort the DataFrame by 'Views' column in descending order
top_30_highest_views = df.sort_values('Views', ascending=False).head(30)

# Display the top 30 highest views
print(top_30_highest_views)


# In[15]:


import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('youtube_videos.csv')

# Sort the DataFrame by 'Views' column in ascending order
least_10_views = df.sort_values('Views').head(10)

# Display the least 10 views
print(least_10_views)


# In[23]:


#Analyze videos upload by years


# Read the CSV file into a DataFrame
df = pd.read_csv('youtube_videos.csv')

# Extract the year from the 'Date' column
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Group the DataFrame by 'Year' and count the number of videos in each year
videos_per_year = df.groupby('Year').size()

# Display the videos per year
print(videos_per_year)


# In[ ]:




