import cv2, sys, os
import os.path
from pymediainfo import MediaInfo
from os import path

def main():
    vid = get_video()
    split_frames(vid)

def get_video():
    print("Hi! Enter the path to a video you would like to analyze:")
    vid_path = input()
    validFile = False
    while (not validFile):
        try:
            file = open(vid_path, "r")
            media_info = MediaInfo.parse(vid_path)
            for track in media_info.tracks:
                if track.track_type == "Video": print('Video selected: ' + vid_path)
            validFile = True
            return vid_path
        except:
            print('Not a valid path. Please try again (press q to quit)')
            vid_path = input()
            if(vid_path == 'q'): sys.exit(0)

def split_frames(path):
    vid = cv2.VideoCapture(path)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    print("Frame count: ", length)
    try: os.rmdir('frames')
    finally: os.mkdir('frames')
    count = 0
    while vid.isOpened():
        ret, frame = vid.read()
        cv2.imwrite("%s/frame%d.jpg" % ('frames', count), frame)
        print("%s/frames/frame%d.jpg" % (os.getcwd(), count));
        count += 1
        if (count > (length-1)):
            vid.release()
            print ("Done extracting %d frames!" % count)
            break

if (__name__ == "__main__"):
    main()