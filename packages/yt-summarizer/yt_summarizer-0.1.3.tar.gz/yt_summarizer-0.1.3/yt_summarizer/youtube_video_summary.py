import os
import re
import time
import logging

import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound,TranscriptsDisabled

import openai
from tqdm import tqdm
from langdetect import detect
from gtts import gTTS 
import nltk
nltk.download('punkt')

logging.basicConfig(level=logging.INFO)


class YouTubeVideoSummarizer:
    
    
    
    def __init__(self, youtube_api_key=None, openai_api_key=None,  model="gpt-3.5-turbo"):
        
        self.api_service_name = "youtube"
        self.model = model
        self.api_version = "v3"
        self.openai_api_key = openai_api_key or os.environ['OPENAI_API_KEY']
        self.youtube_api_key = youtube_api_key or os.environ['YOUTUBE_API_KEY']
        self.youtube = googleapiclient.discovery.build(self.api_service_name, self.api_version, developerKey=self.youtube_api_key)

    def get_video_ids_from_playlist(self, playlist_id):
        
        """
        Retrieve video IDs from a YouTube playlist.

        Parameters:
        - playlist_id (str): The ID of the YouTube playlist.

        Returns:
        - videos (list): A list of video IDs.
        """
        videos = []
        next_page_token = None

        while True:
            request = self.youtube.playlistItems().list(part="contentDetails", playlistId=playlist_id, maxResults=50, pageToken=next_page_token)
            response = request.execute()

            for item in response["items"]:
                videos.append(item["contentDetails"]["videoId"])

            next_page_token = response.get("nextPageToken")

            if not next_page_token:
                break

        return videos
    
    def extract_language_code(self, input_string):
        """
        Extract a two-character language code from a string.

        Parameters:
        - input_string (str): The input string containing the language code.

        Returns:
        - language_code (str): The extracted two-character language code.
        """
        # Use regular expressions to search for the language code pattern
        pattern = r"(?<=- )[a-z]{2}(?= \()"
        match = re.search(pattern, input_string)

        if match:
            # Extract the matched language code
            language_code = match.group(0)

            return language_code

        else:
            return None
        
    def get_video_title(self, video_id):
        """
        Get the title of a YouTube video.

        Parameters:
        - video_id (str): The ID of the YouTube video.

        Returns:
        - title (str): The title of the video.
        """
        
        try:
            request = self.youtube.videos().list(part="snippet", id=video_id)
            response = request.execute()

            title = response["items"][0]["snippet"]["title"]
            return title

        except Exception as e:
            raise Exception("Error retrieving video title:", e)
            
    def video_lang(self,video_id):
        """
        Detect the language of a YouTube video.

        Parameters:
        - video_id (str): The ID of the YouTube video.

        Returns:
        - language (str): The detected language of the video.
        """
        
        title = self.get_video_title(video_id)
        
        language =detect(title)

        return language
       
        
    def get_transcript(self, video_id, language = 'en'):
        """
        Get the transcript of a YouTube video.

        Parameters:
        - video_id (str): The ID of the YouTube video.

        Returns:
        - video language(str): the language of title
        - transcript (str): The transcript of the video.
        """
        
        langs = list(set([language, self.video_lang(video_id)] ))
        
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            video_lang = self.extract_language_code(str(transcript_list))
            if video_lang is not None:
                langs = list(set([language, video_lang, self.video_lang(video_id)] ))
            logging.warning(langs)
            for lang in langs:
                try:
                    transcript = transcript_list.find_manually_created_transcript([lang])
                    return self.video_lang(video_id), '.'.join(section['text'] for section in transcript.fetch())
                
                except NoTranscriptFound as e:
                    
                    try:
                        transcript = transcript_list.find_generated_transcript([lang])
                        logging.info(f'Auto-generiert transcript.')
                        return self.video_lang(video_id),'.'.join(section['text'] for section in transcript.fetch())  
                    except NoTranscriptFound as e:
                        
                        logging.warning(f'failed to retrieve transcript in {lang}. Try to retrieve transcript in {set(langs).difference(set(lang))}')
                        continue
                except Exception as e:
        
                    logging.warning(f"Error retrieving transcript for video: {video_id}. {e}")
                    continue
        
        except TranscriptsDisabled as e:
            logging.warning(f"Transcripts are disabled for video: {video_id}")
            
            
    def download_playlist_transcripts(self, playlist_id):
        """
        Download transcripts for all videos in a YouTube playlist.

        Parameters:
        - playlist_id (str): The ID of the YouTube playlist.
        """
        videos = self.get_video_ids_from_playlist(playlist_id)

        for video in tqdm(videos[:]):
            try:
                title = self.get_video_title(video)
            except:
                title = video
            try:
                transcript = self.get_transcript(video)
                if transcript:
                    transcript_list = transcript.fetch()
                    transcript_text = '\n'.join(line['text'] for line in transcript_list)
                    if not os.path.exists("transcripts"):
                        os.makedirs("transcripts")
                    with open(f'transcripts/{video}_{title}.txt','w') as file:
                        file.write(transcript_text)
                    logging.info(f"Transcript downloaded for video: {video}")

                # Pause to avoid exceeding API rate limits
                time.sleep(2)

            except Exception as e:
                logging.warning(f"Error downloading transcript for video: {video}. {e}")
    
 

    def divide_document_into_chunks(self,document,token_lim=2000):
        """
        Divide a document into chunks of specified token limit.

        Parameters:
        - document (str): The document to divide into chunks.
        - token_lim (int): The maximum number of tokens per chunk (default: 2000).

        Returns:
        - chunks (list): A list of document chunks.
        """
        tokens = nltk.word_tokenize(document)
        chunks = []

        # Iterate over the tokens and divide them into chunks
        for i in range(0, len(tokens),token_lim):
            chunk = tokens[i: i+token_lim]  
            section = ' '.join(chunk)
            chunks.append(section) 
            
        return chunks

    
    def summarize_text(self, text,lang, max_tokens = 200):
        """
        Summarize text using OpenAI's GPT model.

        Parameters:
        - text (str): The text to summarize.
        - video_id (str): The ID of the associated video.
        - max_tokens (int): The maximum number of tokens in the summary (default: 200).

        Returns:
        - summary (str): The summarized text.
        """
        
        openai.api_key = self.openai_api_key
    
        content = "Du bist ein hilfreicher Assistent, der Texte zusammenfasst" if lang =="de" \
                else "You are a helpful assistant that summarizes text."
        
        # reduce number of tokens when reaching token limit 
        for token_lim in range(2000,0,-500):
            
            summarizes = []
            chunks = self.divide_document_into_chunks(text,token_lim)
            for chunk in tqdm(chunks):    
                
                try:
                    response = openai.ChatCompletion.create(
                        model=self.model,

                        messages=[
                                {"role": "system", "content": content},
                                {"role": "user", "content":'summarize '+ chunk}
                                ],

                        max_tokens=max_tokens,
                        n=1,
                        stop=None,
                        temperature=0.5,
                    )
                    
                    logging.info("summarizing...")
                    summarize = response.choices[0].message.content.strip()
                    summarizes.append(summarize)
                   
                except Exception as e:
                    logging.warning(e)
                    break
                    
                
            else:
                logging.info("SUMMARIZING FINISHED")
                return ' '.join(summarizes)
                    
    def convert_to_audio(self,text):
        
        if not os.path.exists("audios"):
            os.makedirs("audios")    
        au = gTTS(text ,lang = 'en') 
        au.save(f"audios/summary.mp3")
    
    def write_to_textfile(self,video_id,text):
        """
        Write text to a file.

        Parameters:
        - video_id (str): The ID of the associated video.
        - text (str): The text to write to a file.
        """
        title = self.get_video_title(video_id)
        if not os.path.exists("summaries"):
            os.makedirs("summaries")
        with open(f"summaries/{title}.txt","w") as file:
            file.write(text)
            logging.info("writing to file")
        


if __name__ == "__main__":
    
    
    video_id = input("Youtube Video ID: ") # video_id is the characters after v= inside the link such as https://www.youtube.com/watch?v=cupU_lyNY2w
    downloader = YouTubeVideoSummarizer()
    lang, text = downloader.get_transcript(video_id)
    if text:
        summarized_text = downloader.summarize_text(text,lang, max_tokens = 200)
        print(summarized_text)
        # you can also write the summarized transcript to file :
        # downloader.write_to_textfile(video_id,summarized_text)
        # or as mp3 file downloader.convert_to_audio(summarized_text)
    else:
        print("problem retrieving transcript")
    
        
        