import music_tag
import os
import glob
import itertools
import eyed3

class album_meta:
    def __init__(self):
        self.artist = ''
        self.album = ''
        self.album_artist = ''
        self.date = 1
        self.tracknumber = 1
        self.genre = 'Hip Hop'
        self.artwork = 'img'


dir = 'C:/Users/Minwoo/Music/Take One/Takeone for the team'


def getFilenames(dir : str, exts : list):
       fnames = [glob.glob(dir + ext) for ext in exts]
       fnames = list(itertools.chain.from_iterable(fnames))
       return fnames

file_list = glob.glob(dir)

audio_list = getFilenames(dir, ['/*.mp3'])
cover = getFilenames(dir, ['/*.jpg', '/*.jpeg', '/*.png'])[0]



if __name__ == "__main__":

    meta = album_meta()
    
    for file in file_list:

        
        audiofile = eyed3.load("test.mp3")
        audiofile.initTag()
        audiofile.tag.artist = meta.artist
        audiofile.tag.album = meta.album
        audiofile.tag.album_artist = meta.album_artist
        audiofile.tag.recording_date = meta.date
        audiofile.tag.images.set(3, open(cover,'rb').read(), 'image/jpeg')
        audiofile.tag.save()
#"AttributeError : 'NoneType'object has no attribute 'artist'"
#TypeError: Missing filename or fileobj argument