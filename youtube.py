from selenium_youtube_uploader import YouTubeUploader

tags = ["reddit", "funny", "askreddit", "best", "montage", "compilation"]
description = """Reddit funny moments compilation from r/askreddit! 
Be sure to subscribe for daily funny reddit posts. Check out my
channel for more hilarious reddit clips!
"""

def uploadVideo(filePath, title):
  if len(title + "#shorts") < 100:
    title = title + "#shorts"
  uploader = YouTubeUploader(filePath, title, description, tags, "C:\\Users\\lukas\\AppData\\Local\\Google\\Chrome\\User Data")
  uploader.upload()
