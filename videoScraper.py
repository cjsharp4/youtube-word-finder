from youtube_transcript_api import YouTubeTranscriptApi #pip install youtube_transcript_api
import requests #pip install requests
from pytube import YouTube #pip install pytube
from moviepy.editor import * #pip install moviepy
import cv2 #pip install opencv-python
import os 
import pathlib #pip install pathlib
from csv import reader
import time
import shutil


"""
def csvLinks():
    # open file in read mode
    with open('links.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        video_id_list = []
        video_link_list = []
        for row in csv_reader:
            #iterate through first row 
            for i in range(0,len(row)):
                #check if row is empty 
                if row[i]:
                    #get video link 
                    video_link_list.append(row[i])
                    #get video id
                    video_id_list.append(row[i].split("v=",1)[1]) 
"""

def getLinks():
    with open('random_youtube_database.txt') as text_file:
        video_id_list = []
        video_link_list = []
        for line in text_file:
            stripped_line = line.strip()
            video_id_list.append(stripped_line)
            new_link = 'https://www.youtube.com/watch?v=' + stripped_line
            video_link_list.append(new_link)
        
    return video_link_list , video_id_list


##TODO require coords to be certain size so that face is big enough to see in video
##TODO OPTIMIZE CLIP LENGTH SO ONLY TARGET WORD IS IN CLIP (HARDER TODO)
def faceDetect(clip_name):
    #Load the cascade  
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')  #open face classifier from opencv github
  
    # To capture video from existing video.   
    cap = cv2.VideoCapture(clip_name)  

    faces_array = []
    count = 0

    while True:
        #read frame (img variable)
        _, img = cap.read()  
    

        #stop at end of frames in video
        if(img is None):
            break

        #Convert to grayscale  
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
  
        #Detect the faces  
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)  #increase last two argument (scaleFactor and minNeighbors) for stricter classification

        faces_array.append(faces)
        count = count + 1

    #remove empty tuples or frames with no face detection
    faces_array = [t for t in faces_array if t != ()]
    print('frames with face: ' + str(len(faces_array)))
    print('total frames: ' + str(count))
    print(len(faces_array)/count)
    print('-----------------------')

    #Release VideoCapture object  
    cap.release()

    if( (len(faces_array)/count) > 0.80 ):
        return True
    
    return False


def saveClip(clip_name,folder_name,phoneme):
    cwd = os.getcwd()

    current_filepath = cwd + '/' + clip_name

    #gets directory for proper folder based on word's phoneme

    phoneme_folder = cwd + '/'

    print("Phoneme: " , phoneme, " || " , phoneme_folder)

    if(phoneme == "(EE)"):
        phoneme_folder += "EE_Videos"
    else:
        phoneme_folder += "UH_Videos"

    destination_folder = phoneme_folder + '/' + folder_name
    destination_filepath = destination_folder + '/' + clip_name

    pathlib.Path(destination_folder).mkdir(parents=True, exist_ok=True)

    shutil.move(current_filepath, destination_filepath)
    #os.rename(current_filepath, destination_filepath)


def scrape(words):

    """
    example video link:
    https://www.youtube.com/watch?v=7iONU9LxeV8
    this is the video id:
    7iONU9LxeV8
    """

    #video_link = 'https://www.youtube.com/watch?v=7iONU9LxeV8'  
    #root = YouTubeTranscriptApi.get_transcript('7iONU9LxeV8') 

    #for key in root:
    #   print(key['text'])

    video_link_list , video_id_list = getLinks()
    
    #list of words that we are looking to find in the video 
    target_words = words

    #get list of target_words without the phoneme as a tuple
    ee_uh = [x[0] for x in target_words]
    ee_uh = [x.lower() for x in ee_uh]


    #print(ee_uh)
    #GET https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=surfing&key=[YOUR_API_KEY] HTTP/1.1

    test_counter = 0
    
    for link in range(0,len(video_link_list)):
        
        test_counter += 1

        video_link = video_link_list[link]  
        
        try:
            root = YouTubeTranscriptApi.get_transcript(video_id_list[link])
        except:
            root = "fail"

        if(root != "fail"):
            word_found = False
            which_word = "###"
            clip_number = 1
            for child in root:  
                transcript_section = child['text'].lower().split()

                #begin downloading and clipping a video if a word from the list is found in the video's transcript
                if(any(word in transcript_section for word in ee_uh)):
                    
                    print("target word found")

                    print("Video Link Array Index: " + str(link))

                    #get which word and phoneme was said in the clip
                    phoneme = ""
                    word_index = 0
                    for word in ee_uh:
                        if(word in transcript_section):
                            phoneme = target_words[word_index][1]
                            which_word = word
                        word_index += 1

                    #for the first instance of a word being found, download the current video
                    if(word_found == False):
                        yt = YouTube(video_link)
                        video_title = yt.title
                        #video_title = "".join( x for x in video_title if (x.isalnum() or x in "._- "))
                        video_title = "".join( x for x in video_title if (x.isalnum())) #remove illegal characters from filename
                        video_filename = video_title + ".mp4"
                        #yt.streams.first().download()
                        download_video = yt.streams.filter(progressive = True, file_extension = "mp4").first().download(filename=video_filename)
                        word_found = True

                    #find the start and ending times of each transcript portion with a target word
                    start = int(float(child['start']))
                    end = int(float(child['duration'])) + start

                    print("Initial start and end: " + str(start) + " | " + str(end))
                    

                    clip = VideoFileClip(video_filename)

                    #case where clip is at the end of the video and the duration is rounded up when converting to an int
                    duration = clip.duration
                    print("duration: " + str(duration))
                    if(duration < end):
                        print("test")
                        end = end-2
                        print("test2")
                        start = start - 4
                    if(start == end):
                        start = start -1

                    print("After comparison start and end: " + str(start) + " | " + str(end))

                    clip = clip.subclip(start, end)

                    #name file with video's title, the target word found, and number of clip within an individual video 
                    clip_name = phoneme + "-(" + which_word + ")_" + video_title + "_clip" + str(clip_number) + ".mp4"
                    clip_number += 1
                    folder_name = video_title

                    #write file that will contain video and audio
                    
                    clip.write_videofile(clip_name, temp_audiofile='temp-audio.m4a', remove_temp=True, codec="libx264", audio_codec="aac")
                    #print(unescape(child.text), int(float(child.attrib['start'])), "\n")

                    clip.close()

                    #if a face is detected for at least 80% of the video
                    if(faceDetect(clip_name)):

                        #save clip in folder with video's title
                        saveClip(clip_name,folder_name,phoneme)

                        #remove full length downloaded video
                        try:
                            removeFile = os.getcwd() + '/' + video_filename
                        except:
                            print("video did not contain any of the target words")
                            video_filename = None
                        else:
                            if(os.path.isfile(removeFile)):
                                os.remove(removeFile)

                        #stop scraping once one video is saved
                        print("Number of videos analyzed: ")
                        print(test_counter)
                        return
                        

                    else:
                        removeFile = os.getcwd() + '/' + clip_name
                        if(os.path.isfile(removeFile)):
                            os.remove(removeFile)


            
            #remove full length downloaded video
            try:
                removeFile = os.getcwd() + '/' + video_filename
            except:
                print("video did not contain any of the target words")
                video_filename = None
            else:
                if(os.path.isfile(removeFile)):
                    os.remove(removeFile)


def main():
    start = time.time()

    words = [ ["street","(EE)"] ]
    scrape(words)

    #Print number of links analyzed and total elapsed time of script
    end = time.time()
    print("Elapsed Time:")
    print(end - start)


if __name__ == "__main__":
    main()
