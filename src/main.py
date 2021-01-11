from pytube import Playlist, YouTube
from googleapiclient.discovery import build
import requests
import subprocess
import os
import time
import json
import re
import threading

lock = threading.Lock()
sema = threading.Semaphore(10)

WORKDIR = os.path.dirname(os.path.realpath(__file__)) + '/tmp5/'

JSON_NAME = 'video_stats.json'
JSON_PATH = WORKDIR + JSON_NAME

json_template = {
    "name": "crwal_youtube",
    "platform": "youtube",
    "title": "default",
    "len": 0,
    "models": [
    ]}

def get_id(url: str):

    pattern = r'((?<=(v|V|e)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)'
    return re.search(pattern, url).group()

class result:
    def __init__(self):
        self.text = ''
        self.file_path = ''

class _json:

    def __init__(self, title : str = None):

        global JSON_PATH

        _json.json_data = json_template

        if title:
            _json.json_data['title'] = title
            JSON_PATH = './' + title + '/' + JSON_NAME

        if not os.path.isfile(JSON_PATH):
            os.mkdir(os.path.dirname(JSON_PATH))
            with open(JSON_PATH, 'w') as json_file:
                json.dump(_json.json_data, json_file, indent=4)

        else :
            with open(JSON_PATH, 'r') as json_file:
                _json.json_data = json.load(json_file)

    def sub_model(self, yt : YouTube, status: int, path : str = None, track : int = None):

        json_data = {}
        json_data['id'] = yt.video_id
        json_data['status'] = status
        if status > 0:
            
            if not track : 
                track = _json.json_data['len'] + 1

            json_data['meta'] = []
            json_data['meta'].append({
                'title': yt.title,
                'author': yt.author,
                'track': track,
                'len': yt.length,
                'file_size': os.path.getsize(path),
                'uploaded': False
            })
            
        _json.json_data['len'] += 1
        _json.json_data['models'].append(json_data)

        with open(JSON_PATH, 'w') as outfile:
            json.dump(_json.json_data, outfile, indent=4)

def _YouTube(url: str):

    try:
        yt = YouTube(url)

    except Exception as err:
        if 'unavailable' in str(err):
            return 'blocked_error'
        if 'regex_search' in str(err):
            return 'worng_url_error'

    return yt


def download_video(url, yt):

    _result = result()
   
    file_id = yt.video_id
    file_name = yt.title

    video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by(
        'resolution').desc().first().download(WORKDIR, file_id + 'video')
    audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by(
        'abr').desc().first().download(WORKDIR, file_id + 'audio')

    lock.acquire()

    process = subprocess.Popen(['ffmpeg', '-y', '-i', WORKDIR + '/' + file_id + 'video.mp4', '-i', WORKDIR
                               + '/' + file_id + 'audio.mp4', WORKDIR + '/' + file_name.replace('/', '-') + '.mp4'], 
                               shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    exitcode = process.returncode

    lock.release()

    file_path = WORKDIR + '/' + file_name.replace('/', '-') + '.mp4'

    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
        _result.text = 'download_failed'
    else:
        _result.text = 'completed'
        _result.file_path = file_path

    if(os.path.isfile(video_stream)):
        os.remove(video_stream)
    if(os.path.isfile(audio_stream)):
        os.remove(audio_stream)

    return _result


def try_download(yt, i = None):

    print(yt.title)

    if yt == 'worng_url_error':
        print('Worng url ㅗ')

    elif yt == 'blocked_error':
        print('막혔음 ㅅㄱ')
        j.sub_model(url, -1)

    else :
        result = download_video(url, yt) 
        
        if result.text == 'completed':
            j.sub_model(yt, 1, result.file_path, i)
        elif result.text == 'download_failed':
            j.sub_model(yt, 0, i)


if __name__ == '__main__':

    j = _json()
    
    t1 = time.time()
    url = input('url : ')
    file_ext = input('extension : ')
    
    if('list=' in url):
        
        p = Playlist(url)
        j = _json(p.title)
        WORKDIR = './' + p.title
        i = 1

        def 이름짓기싫다(uyl,i):
            sema.acquire()
            yt = _YouTube(url)
            try_download(yt, i)
            sema.release()

        threads = []

        for url in p.video_urls:
            th = threading.Thread(target=이름짓기싫다,args=(url, i))
            th.start()
            threads.append(th)
            i+=1

        for th in threads:
            th.join()

    else:
        yt = _YouTube(url)
        try_download(yt)


    print(time.time()-t1)
