#############################################################
#
#  Author: Sebastian Maurice, PhD
#  Copyright by Sebastian Maurice 2018
#  All rights reserved.
#  Email: Sebastian.maurice@otics.ca
#
#############################################################


import easyocr
import speech_recognition as sr
import moviepy.editor as mpe
    
def viperimagetotext(filename):
    if filename=="":
        return "Enter IMAGE (png, jpg, etc.) filename"
    
    return doocrmain(filename)

def viperaudiototext(filename):
    if filename=="":
        return "Enter AUDIO File (WAV) filename"
    
    return audiototext(filename)

def vipervideototext(filename):
    if filename=="":
        return "Enter VIDEO File (MP4) filename"
    
    return convertvideototext(filename)


def convertvideototext(filename):
        #convert to audio
        video = mpe.VideoFileClip(filename)
        audiofile=filename + ".wav"
        
        video.audio.write_audiofile(audiofile)
        result = audiototext(audiofile)
        
        return result

def audiototext(filename):
        r = sr.Recognizer()
        audio = sr.AudioFile(filename)
        with audio as source:
          audio_file = r.record(source)
        result = r.recognize_google(audio_file)
        speechfile = filename + '.speech.txt'
        with open(filename + '.speech.txt',mode ='w') as file: 
           file.write(result)

        return result   


def doocrmain(filename):

    reader = easyocr.Reader(['en'])   
    bound = reader.readtext(filename)
    return bound
