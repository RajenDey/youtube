# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from oauth2client import client # Added
from oauth2client import tools # Added
from oauth2client.file import Storage # Added

import pandas as pd
import numpy as np


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"


    credential_path = os.path.join('./', 'credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
        credentials = tools.run_flow(flow, store)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return request(youtube)



def request(youtube):
    allVideos = []

    def getRelated(videoId, depth):
        if (depth == 6):
            return
                    
        nonlocal allVideos
        try:
            # 50 -> maybe some later ones irrelevant, but gets more videos total without exceeding quota
            req = youtube.search().list(part="snippet", relatedToVideoId=videoId, type="video", maxResults=50)
            response = req.execute()
        except:
            export(allVideos)

        videos = []
        for video in response["items"]:
            try:
                id = video["id"]["videoId"]
                title = video["snippet"]["title"][:200]
                desc = video["snippet"]["description"][:200]
                stats = getStats(youtube, id)

                features = [depth, id, title, desc] + stats
                videos.append(features)
            except:
                print("failed")
        
        allVideos += videos

        for video in videos:
            id = video[1]
            getRelated(id, depth + 1)

    def getStats(youtube, videoId):
        try:
            req = youtube.videos().list(part="statistics", id=videoId)
            response = req.execute()

            stats = response["items"][0]["statistics"]
        except:
            export(allVideos)
        return [stats["viewCount"], stats["likeCount"], stats["dislikeCount"], stats["favoriteCount"], stats["commentCount"]]


    start_video = "G7RgN9ijwE4"
    getRelated(start_video, 0)
    return allVideos




def export(videos):
    df = pd.DataFrame(videos, columns=["depth", "id", "title", "description", "views", "likes", "dislikes", "favorites", "comments"])
    df.to_csv("videos.csv")
    print(df)


if __name__ == "__main__":
    videos = main()
    export(videos)