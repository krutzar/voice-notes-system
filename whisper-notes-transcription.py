# For Use In Google Colab
# WARNING - I'm no dev. My code is probably a mess. 

# Importing necessary libraries
import os
import subprocess
import shutil
import csv
from datetime import datetime
from IPython.display import Javascript
from google.colab import drive

# Installing required packages and updating system packages
!pip install git+https://github.com/openai/whisper.git
!sudo apt update && sudo apt install ffmpeg

# Mount Google Drive
drive.mount('/content/drive')

################

# Functions
def get_file_duration(file_path):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    duration = result.stdout.strip()  # Get the duration as a string
    return float(duration)  # Convert to float for further calculations

def append_to_csv(file_path, count, duration, word_count):
    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        current_date = datetime.now().strftime('%Y-%m-%d')
        writer.writerow([current_date, count, duration, word_count])

# Step 1: Setup and file preparation
def prepare_environment(folder_path):
    combined_folder_path = os.path.join(folder_path, 'combined')
    # Create the 'combined' subfolder if it doesn't exist
    if not os.path.exists(combined_folder_path):
        os.makedirs(combined_folder_path)
    return combined_folder_path

# Step 2: Listing MP3 files
def list_mp3_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.mp3')]

# Step 3: Creating a file list for ffmpeg concatenation
def create_file_list(files, folder_path):
    with open('file_list.txt', 'w') as file_list:
        for file in files:
            file_list.write(f"file '{os.path.join(folder_path, file)}'\n")

# Step 4: Concatenating MP3 files
def concatenate_files(input_file_list, output_file):
    subprocess.run(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', input_file_list, '-c', 'copy', output_file])

# Step 5: Updating the summary CSV
def update_summary(csv_file_path, file_count, total_duration, word_count):
    append_to_csv(csv_file_path, file_count, total_duration, word_count)

def split_file(input_file, chunk_size=6000):
    # Open the input file and read the text
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Calculate the number of chunks
    num_chunks = len(text) // chunk_size + (1 if len(text) % chunk_size else 0)

    # Split the text into chunks and write to separate files
    for i in range(num_chunks):
        chunk = text[i*chunk_size:(i+1)*chunk_size]
        with open(f'output_{i+1}.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(chunk)
        print(f'Chunk {i+1} written to output_{i+1}.txt')

# Transcribe Audio and Move Transcript
def transcribe_and_move_transcript(audio_file_path, transcript_destination_path):
    # Constructing Whisper command
    whisper_command = f'whisper "{audio_file_path}" --model medium --language en'
    try:
        # Executing Whisper command for transcription
        subprocess.run(whisper_command, shell=True, check=True)

        # Assuming Whisper outputs a .txt file in the same directory as the audio file, with the same base name
        source_transcript_path = audio_file_path.rsplit('.', 1)[0] + '.txt'

        # Moving the transcript to the desired location
        shutil.copy(source_transcript_path, transcript_destination_path)
        print(f"Transcript file copied to: {transcript_destination_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during transcription: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def count_words_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        transcript = file.read()
        word_count = len(transcript.split())
    return word_count


def main():
    folder_path = '/content/drive/My Drive/Easy Voice Recorder/'
    combined_folder_path = prepare_environment(folder_path)

    # Check for and delete combined_file.mp3 if it exists
    combined_mp3_path = os.path.join(combined_folder_path, 'combined_file.mp3')
    if os.path.exists(combined_mp3_path):
        os.remove(combined_mp3_path)
        print(f"Deleted existing file: {combined_mp3_path}")

    # Check for and delete combined_file.txt if it exists
    combined_txt_path = os.path.join(combined_folder_path, 'combined_file.txt')  # Adjust this path if necessary
    if os.path.exists(combined_txt_path):
        os.remove(combined_txt_path)
        print(f"Deleted existing file: {combined_txt_path}")

    files = list_mp3_files(folder_path)
    create_file_list(files, folder_path)
    output_file = os.path.join(combined_folder_path, 'combined_file.mp3')
    concatenate_files('file_list.txt', output_file)
    print(f"Concatenation complete. The combined file is located at: {output_file}")
    total_duration = get_file_duration(output_file)  # Calculate total duration of the combined file

    # Transcription moved here after concatenation
    combined_audio_path = os.path.join(combined_folder_path, 'combined_file.mp3')
    transcript_destination_path = os.path.join(combined_folder_path, 'combined_file.txt')
    transcribe_and_move_transcript(combined_audio_path, transcript_destination_path)
    print(f"Transcription complete. The transcript file is located at: {transcript_destination_path}")

    # Counting words in the transcript
    word_count = count_words_in_file('combined_file.txt')

    csv_file_path = os.path.join(combined_folder_path, 'summary.csv')
    update_summary(csv_file_path, len(files), total_duration, word_count)
    print(f"Updated CSV with Date: {datetime.now().strftime('%Y-%m-%d')}, Count: {len(files)}, Total Duration: {total_duration} seconds, Word Count: {word_count}.")

###############

# Run Main Function
if __name__ == "__main__":
    main()


###################

# Word Count And Data
    word_count = count_words_in_file('combined_file.txt')

    csv_file_path = os.path.join(combined_folder_path, 'summary.csv')
    update_summary(csv_file_path, len(files), total_duration, word_count)
    print(f"Updated CSV with Date: {datetime.now().strftime('%Y-%m-%d')}, Count: {len(files)}, Total Duration: {total_duration} seconds, Word Count: {word_count}.")



