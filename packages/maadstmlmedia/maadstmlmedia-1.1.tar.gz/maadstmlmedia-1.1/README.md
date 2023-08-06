**Multi-Agent Accelerator for Data Science Using Transactional Machine Learning (MAADSTMLMEDIA)**

*Revolutionizing Data Stream Science with Transactional Machine Learning*

**Overview**

*MAADSTMLMEDIA allows users to extract text from images, audio and video.*  

**Compatibility**
    - Python 3.7 or greater
    - Minimal Python skills needed

**Copyright**
   - Author: Sebastian Maurice, PhD
   
**Installation**
   - At the command prompt write:
     **pip install maadstmlmedia**
     - This assumes you have [Downloaded Python](https://www.python.org/downloads/) and installed it on your computer.  


- **viperimagetotext**
  - Extracts text from images like PNG, JPG, etc., which can then be streamed to kafka.

- **viperaudiototext**
  - Extracts text from audio files like WAV, etc., which can then be streamed to kafka.

- **vipervideototext**
  - Extracts text from video files like MP4, etc., which can then be streamed to kafka.


**First import the Python library.**

**import maadstmlmedia**


**1. maadstmlmedia.viperimagetotext(imagefilename)**

**Parameters:**	Extract text from images.

*imagefilename* : string, required

- Image filename like PNG, JPG etc.

RETURNS: Text in image.

**2. maadstmlmedia.vipervideototext(videofilename)**

**Parameters:**	Extract text from video.

*videofilename* : string, required

- Video filename like MP4 etc.

RETURNS: Text in video.

**3. maadstmlmedia.viperaudiototext(audiofilename)**

**Parameters:**	Extract text from audio

*audiofilename* : string, required

- Audio filename like WAV etc.

RETURNS: Text in audio.
