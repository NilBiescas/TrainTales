import os
from TTS.utils.synthesizer import Synthesizer
from TTS.utils.manage import ModelManager
from pydub import AudioSegment

def text_to_mp3(text, output_file='output.mp3'):
    # Define model names
    tts_model_name = "tts_models/en/ljspeech/tacotron2-DDC"
    vocoder_model_name = "vocoder_models/en/ljspeech/hifigan_v2"
    
    # Download models
    model_manager = ModelManager()
    tts_model_path, tts_config_path, tts_model_item = model_manager.download_model(tts_model_name)
    vocoder_model_path, vocoder_config_path, vocoder_model_item = model_manager.download_model(vocoder_model_name)
    
    # Initialize the synthesizer
    synthesizer = Synthesizer(
        tts_model_path, 
        tts_config_path, 
        None, 
        None, 
        vocoder_model_path, 
        vocoder_config_path, 
        None, 
        False
    )
    
    # Synthesize speech
    wav = synthesizer.tts(text)
    
    # Save the output to a temporary WAV file
    temp_wav_file = "temp_output.wav"
    synthesizer.save_wav(wav, temp_wav_file)
    
    # Convert WAV to MP3
    sound = AudioSegment.from_wav(temp_wav_file)
    sound.export(output_file, format="mp3")
    
    # Remove the temporary WAV file
    os.remove(temp_wav_file)
    print(f"MP3 file saved as {output_file}")

# Example usage
text = "Once upon a time, in a faraway land, there was a little princess who loved adventures."
text_to_mp3(text, "story.mp3")
