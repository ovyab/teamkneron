import cv2, sys, os, csv, shutil
import os.path
from pymediainfo import MediaInfo
from os import path
# import torchvision
from PIL import Image, ImageFont, ImageDraw 

def main():
    vid = get_video()
    # get_frames(vid)
    split_frames(vid)
    imgnames, imgs = generate_results()
    generate_video(imgnames, imgs)

def get_video():
    print("Hi! Enter the path to a video you would like to analyze:")
    vid_path = input()
    validFile = False
    while (not validFile):
        try:
            file = open(vid_path, "r")
            media_info = MediaInfo.parse(vid_path)
            for track in media_info.tracks:
                if track.track_type == "Video": print('Selected video: ' + vid_path)
            validFile = True
            return vid_path
        except:
            print('Not a valid path. Please try again (press q to quit)')
            vid_path = input()
            if(vid_path == 'q'): sys.exit(0)

# def get_frames(video):
#     frames = torchvision.io.read_video(video, pts_unit="sec") # returns each video frame as a Tensor[T, H, W, C]
#     count = 1
#     for f in frames[1]:
#         print()
#         # cv2.imwrite("%s/frame%d.jpg" % ('frames', count), f)
#         count += 1
#     print('hi')

def split_frames(path):
    vid = cv2.VideoCapture(path)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    if os.path.exists('frames'):
        shutil.rmtree('frames')
    os.mkdir('frames')
    count = 0
    with open('results.csv', mode='w') as file:
        fieldnames = ['img', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        while vid.isOpened():
            ret, frame = vid.read()
            cv2.imwrite("%s/frame%d.jpg" % ('frames', count), frame)
            # print("%s/frames/frame%d.jpg" % (os.getcwd(), count));
            writer.writerow({'img': 'frame%d.jpg' % (count),
                            'c0':.1,
                            'c1':.1,
                            'c2':.98,
                            'c3':.3,
                            'c4':.1,
                            'c5':.7,
                            'c6':.14,
                            'c7':.1,
                            'c8':.02,
                            'c9':.18})
            count += 1

            if (count > (length-1)):
                vid.release()
                print ("Done extracting %d frames!" % count)
                break

def generate_results():
    print('Classifying frames...')
    images = []
    imgnames = []
    with open('results.csv', mode='r') as file:
        csv_reader = csv.DictReader(file)
        os.chdir('frames')
        for row in csv_reader:
            # get name of img and open it
            img_name = row['img']
            img = Image.open("%s" % (img_name))

            # get classifications for img text
            text = ""
            maxNum = 0.0
            for col in row:
                if (col !='img' and float(row[col]) > maxNum):
                    maxNum = float(row[col])
                    text = col

            # put classifications on image + save
            img_editable = ImageDraw.Draw(img)
            img_editable.text(xy=(15,15), text=text, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0,0,0))
            # os.chdir('frames')
            img.save("%s" % (img_name))
            images.append(img)
            imgnames.append(img_name)
    return imgnames, images
    
def generate_video(imgnames, images):
    video_name = 'resultvideo.mp4'
    print('Generating results video...')
     
    # dict of {image_name, JpegImageFile} 
    frame = cv2.imread('frame0.jpg') 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape

    video = cv2.VideoWriter("../" + video_name, 0x7634706d, 20.0, (width, height))  
  
    # appending images to the video one by one 
    for image in imgnames:  
        video.write(cv2.imread(image))  
      
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 

    # remove frames folder
    os.chdir('..')
    shutil.rmtree('frames')
    print('Done! Open %s for the result video, and results.csv for the CSV output.' % video_name)

if (__name__ == "__main__"):
    main()