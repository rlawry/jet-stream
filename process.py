import os
from pydub import AudioSegment

def normalize_folder(input_folder, target_lufs=-14.0):
    """
    Scans a folder for MP3s, calculates average loudness, 
    and normalizes all files to the target LUFS.
    """
    # 1. Setup paths
    output_folder = os.path.join(input_folder, "normalized_output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    audio_files = [f for f in os.listdir(input_folder) if f.endswith('.mp3')]
    
    if not audio_files:
        print("No MP3 files found in the directory.")
        return

    print(f"Found {len(audio_files)} files. Processing...")

    for filename in audio_files:
        file_path = os.path.join(input_folder, filename)
        
        # Load audio
        audio = AudioSegment.from_file(file_path, format="mp3")
        
        # 2. Comparative Assessment
        # pydub's .dBFS is a close approximation for loudness assessment
        current_loudness = audio.dBFS
        change_in_gain = target_lufs - current_loudness
        
        print(f"Processing: {filename} | Current: {current_loudness:.2f} dBFS | Adjusting: {change_in_gain:+.2f} dB")
        
        # 3. Apply Gain
        normalized_audio = audio.apply_gain(change_in_gain)
        
        # 4. Export
        output_path = os.path.join(output_folder, filename)
        normalized_audio.export(output_path, format="mp3")

    print(f"\nSuccess! Normalized files are in: {output_folder}")

if __name__ == "__main__":
    # Change '.' to your specific folder path if needed
    folder_to_process = "." 
    normalize_folder(folder_to_process)