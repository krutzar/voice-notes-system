# voice-notes-system
System for taking voice notes and transcribing them, organizing notes into themes, and ultimately organizing them into a usable notes system.

## Intro & Context
With this, the main issue I wanted to try and tackle is combatting the difficulty of capturing an idea. Often when you have an idea, being able to quickly get the idea from your brain into some form of note is key to trying to capture the idea in it's "purist" form. 

For more abstract or more complex ideas, writing it down isn't always the most seamless medium, particularly if you're in a situation where you don't have access to something you can write with or use your phone to take notes on.

It's like when you end up having ideas when you're showering, driving, doing dishes, etc. Rarely do you sit down to solve something and have those ideas just come rushing it it seems. 

If you ever have an idea and think to yourself "I'll remember that," odds are you won't. 
### Solution
This is why I aimed to create a system that ultimately tries to make capturing and re-analyzing those spur-of-the-moment ideas at a later date as seamless and frictionless as possible. 

For me it begins at the point of capturing the idea. Voice notes ultimately are the most seamless so I've devised a system to easily capture voice notes, compile them in google drive, transcribe, and organize them for storage and later use. 

Being able to immediately store these ideas not only helps in capturing ideas for later use, but also can simply get ideas out of your own head so you stop thinking about them in circles. 
### Process Outline
1. Voice Notes Capture: Capture the idea via voice notes app. I use and app called "easy voice recorder" because of it's simplicity and ability to do step 2 automatically
2. Sync To Google Drive: Done automatically via Easy Voice Recorder app. 
3. Compile Separate Notes: Via python I combine my files into one file for transcription. As a bonus on this step I count the total number of files, time duration, and word count of the voice notes to add to a CSV for analytics later if I ever feel like it. 
4. Transcription: I use OpenAI's whisper to transcribe my voice notes all within Google Colab
5. Chunking: I chunk the transcription into 6000 word chunks. Not strictly necessary but depending on LLM you're using for the next step. Longer strings of text can cause details of the notes to get left out, which is strictly what I'm trying to avoid. 
6. Delete Old Files: Delete your old transcripts so you don't re-transcribe old notes. I do this manually just to make sure you don't automatically delete files and run into an error elsewhere that causes you to use.
7. Organize Notes: Using ChatGPT, Claude, or your open source LLM of choice, organize the notes into themes using an agent I outlined below. 
8. Organize into your own notes: At this point you probably need your own note taking system but you can then take all this info and put it into your own notes based on the theme. 
## Full Process Walkthrough

### Voice Notes For Capturing Ideas
As I mentioned, voice notes seem to be the most frictionless idea for me. The ability to simply dictate something on the fly, thinking through the idea out loud and as "in the moment" as possible with minimal reflection tends to be the most seamless. There's almost a fluidity to it, helping capture the idea or thought in it's most "pure" state so to speak. 

It's also just easy to pull up a recording and speak...

To accomplish this I used an app called Easy Voice Recorder. For $5 it automatically syncs to google drive, making any sort of file transfer a non-issue. 

Whenever I need to jot down an idea or thought, I can simply pull the app out and start recording within a few seconds. Super fast, frictionless, etc. 
### Google Colab Script
Once I want to compile my ideas, I move to the google colab script I put together to automate this process. 

It begins by setting up the appropriate libraries needed, mounts to your google drive, and sets some functions up. Simply put what the script ends up doing is concatenating all the different audio files and passing them into OpenAI's Whisper for transcription. 

Whisper is really great at transcribing my notes, even getting some of the weird words and phrases I use correct. It runs entirely in google colab as well, so ultimately it's entirely free to use this way and fairly straightforward once set up. I run it on medium, but you could probably run the small or tiny model if you really wanted to. Ultimately though the time to run even larger batches of voice notes isn't all that long even with larger models. 

At the end this script spits out the text transcript as well as a chunked version that is broken into 6000 character segments into a new sub-folder in your Easy Voice Recorder drive folder. This chunking isn't needed, but depending on the LLM you're using, it's context, and ability to follow instructions through larger batches of text, it can be useful for avoiding information loss in larger batches of notes. 

As a bonus, it also logs the file count, runtime in seconds, and character count of the transcribed notes to a CSV so you can look back at usage if you ever want to.
### Transcript & Information Organization
Once you have the transcript you need to organize it so that you can organize it into your own notes system. 

I do the first layer of organization via an LLM Agent (using either GPT4, or claude3 as of late). Simply put this agent aims to reorganize the notes verbatim and into themes. I made a point to have it not reword or summarize anything at all, but if you wanted this could be a pretty easy tweak to make. I would just rather make my own summaries rather than trust an LLM to potentially omit key information. 

This is also where potentially chunking the transcript can come in handy. If you notice the LLM you're using is skipping parts of the transcript, you could just be at the limit of the model's ability to organize information at scale. 

From here you've got an organized version of your transcript grouped by theme. It's not always perfect, but often it's a far better starting point. From here you can organize it into your own notes system, or remove information that either isn't relevant or no longer feels worth storing. 

While you'll need your own system at this point for organizing these notes, I'm planning to put together another article on my own process using Obsidian. That being said if you're reading this, I haven't done that yet - sorry about that. 
### Results and Insights
I've included an example output from the full process below. 

#### Glossary / Appendix
- [Python Script for Google Colab](https://github.com/krutzar/voice-notes-system/blob/main/whisper-notes-transcription.py)
- [Easy Voice Recorder App](https://play.google.com/store/apps/details?id=com.coffeebeanventures.easyvoicerecorder&hl=en_US&gl=US)
- Notes Organizer Agent
- [OpenAI Whisper](https://github.com/openai/whisper)
- Example of notes organized
- [Obsidian](https://obsidian.md/)


[Follow My Work](https://rkseo.xyz/)
