{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ubuntu@sandbox:~ $ python3 << 'EOF'\
import urllib.request\
import json\
\
# Flickr API endpoint for user's public photos\
user_id = "201908381@N02"\
api_key = "YOUR_API_KEY"  # Note: Flickr API requires authentication\
\
# Alternative: Use Flickr's public photo URL pattern\
# Format: https://live.staticflickr.com/\{server-id\}/\{id\}_\{secret\}_b.jpg\
\
# Let's construct URLs from the photo IDs we saw on the page\
# Photo IDs from the Flickr page: IMG_4715, IMG_4754, IMG_4758, IMG_4820, IMG_4824, IMG_4794, IMG_4864, IMG_4863, IMG_4831, IMG_4845, IMG_4832, IMG_4857, IMG_4854\
\
# Since we don't have API key, let's use direct Flickr photo page URLs\
# which can be embedded as image sources\
\
photos = [\
    "55018540576",  # IMG_4715\
    "55018540596",  # IMG_4754\
    "55018540606",  # IMG_4758\
    "55018540666",  # IMG_4820\
    "55018540686",  # IMG_4824\
]\
\
for photo_id in photos:\
    url = f"https://flickr.com/photos/loganfinney/\{photo_id\}/"\
    print(url)\
\
EOF\
\
https://flickr.com/photos/loganfinney/55018540576/\
https://flickr.com/photos/loganfinney/55018540596/\
https://flickr.com/photos/loganfinney/55018540606/\
https://flickr.com/photos/loganfinney/55018540666/\
https://flickr.com/photos/loganfinney/55018540686/\
ubuntu@sandbox:~\
[CMD_END][CMD_BEGIN]\
ubuntu@e29ea14a11bb:~ $}