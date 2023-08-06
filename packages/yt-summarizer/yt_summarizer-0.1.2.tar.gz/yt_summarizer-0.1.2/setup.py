from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='yt_summarizer',
    version='0.1.2',
    author='Isaac Duong',
    author_email='isaaacduong@gmail.com',
    license='MIT',    
    url='https://github.com/isaacduong/youtube_summarizer',
    description=("Python script to extract video transcripts " 
                 "based on the video id, and summarize the " 
                 "text content using the GPT-3.5 Turbo model."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['yt_summarizer'],
    install_requires=[            # I get to this in a second
          'google-api-python-client',
          'youtube_transcript_api',
          'openai',
          'tqdm',
          'nltk',
          'gtts',
          'langdetect',
      ],
   
)
