#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
# import re as regular_expressions
import json
# from datetime import timedelta
from googleapiclient.discovery import build

class SortYoutube():
	def __init__(self):
		self.api_key = "" #insert your api key here
		self.youtube = build('youtube', 'v3', developerKey=self.api_key)

	def __get_channel_id(self):
		request = self.youtube.channels().list(
				part='snippet',
				forUsername='' # insert your username here.
				)
		response = request.execute()

		print(json.dumps(response, indent=4))
		return response['items'][0]['id']

	def __get_playlist_id(self):
		playlist_request = self.youtube.playlists().list(
				part='snippet',
				channelId=self.__get_channel_id(),
				maxResults=50,
				)
		playlist_response = playlist_request.execute()

		playlist_items = []
		while playlist_request is not None:
			playlist_items += playlist_response['items']
			playlist_response = playlist_request.execute()
			playlist_request = self.youtube.playlistItems().list_next(
					playlist_request,
					playlist_response
					)

		for item in playlist_items:
			if item['snippet']['title'] == 'Backlog':
				return item['id']

		return None

	def __get_backlog_playlist(self):
		playlist_id = self.__get_playlist_id()
		playlist_request = self.youtube.playlistItems().list(
				part='contentDetails',
				playlistId=playlist_id,
				maxResults=50
				)
		playlist_response = playlist_request.execute()

		playlist = []
		while playlist_request is not None:
			video_ids = []
			for item in playlist_response['items']:
				video_ids.append(item['contentDetails']['videoId'])

			video_request = self.youtube.videos().list(
					part="contentDetails, snippet",
					id=','.join(video_ids)
					)
			video_response = video_request.execute()

			for item in video_response['items']:
				video_id = item['id']
				youtube_link = f'https://youtu.be/{video_id}'
				title = item['snippet']['title']
				channel_title = item['snippet']['channelTitle']
				playlist.append({
						'id': video_id,
						'youtube_link': youtube_link,
						'title': title,
						'channel_title': channel_title
						})

			playlist_request = self.youtube.playlistItems().list_next(
					playlist_request,
					playlist_response
					)

		return playlist

	def sort_backlog(self):
		playlist = self.__get_backlog_playlist()

if __name__ == "__main__":
	sort_youtube = SortYoutube()
	sort_youtube.sort_backlog()
