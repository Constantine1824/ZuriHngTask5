import random
import string
import re
import os
import fnmatch
from moviepy.editor import VideoClip, concatenate_videoclips

def generate_random_file_name():
    return ''.join(random.choices(string.ascii_lowercase, k=6))

def handle_file(create=True):
    if create:
        try:
            file = f'{generate_random_file_name()}.webm'
            return file
        except Exception as e:
            return e

def update_file(file_name, data):
    temp_file = f'{generate_random_file_name()}-{file_name}-temp.webm'
    with open (f'/media/temp/{temp_file}', 'wb') as file:
        file.write(data.encode('utf-8'))

def merge_files(file_name):
    path = '/media/temp'
    files = []
    for root, dir, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, f'*{file_name}*'):
                files.append(os.path.join(root, name))
    video_clips = [VideoClip(file) for file in files]
    merged_clip = concatenate_videoclips(video_clips)
    merged_clip.write_videofile(f'/media/{file_name}.webm')

    for file in files:
        os.remove(file)


        