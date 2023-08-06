## Project description

This is the speech client python package built by Abax.AI

It allows use to use speech to text services in both manners: offline and online

Online streaming will take audio stream in realtime, and return the transcripts on the fly

Offline transcribing will read your audio file, transcribe and return the transcripts in different formats.


## Examples

### Stream your audio file with python3

    import io
    from abaxai_sdk import streaming

    accessToken = 'YOUR_ACCESS_TOKEN'


    def get_wav_data(wavfile):
        for block in iter(lambda: wavfile.read(1280), b""):
            yield generate_block(block)

    def generate_block(block):
        return block

    def abaxai_streaming(stream_file):
        """Streams transcription of the given audio file."""

        client = streaming.SpeechClient()

        config = streaming.RecognitionConfig(
            encoding=streaming.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="basic_english",
        )

        streaming_config = streaming.StreamingRecognitionConfig(config, accessToken)

        # In practice, stream should be a generator yielding chunks of audio data.
        with io.open(stream_file, 'rb') as audiostream:
            data = get_wav_data(audiostream)
            requests = (
                streaming.StreamingRecognizeRequest(audio_content=chunk) for chunk in data
            )

            responses = client.streaming_recognize(
                            config=streaming_config,
                            requests=requests,
                    )
            
            print("\n\nFinal transcripts: \n")
            for response in responses:
                print(response)


    audio_file = "your_audio_file.wav"

    print("Streaming the audio file")
    abaxai_streaming(audio_file)

### Transcribe your audio file with python3

    from abaxai_sdk import transcribing

    accessToken = 'YOUR_ACCESS_TOKEN'

    def abaxai_transcribe(audio_filepath):
        """Streams transcription of the given audio file."""

        client = transcribing.SpeechClient()

        config = transcribing.RecognitionConfig(
            encoding=transcribing.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            model="wenet-english",
        )
        
        transcribing_config = transcribing.TranscribeConfig(config, accessToken)

        client.recognize(config=transcribing_config,
                            audiofilepath=audio_filepath,)
        
        # speechid = "<your_speech_id>"
        # client.get_transcription(speechid, accessToken)

        print("Done.")


    audio_file = "your_audio_file.wav"

    print("Transcribe the audio file")
    abaxai_transcribe(audio_file)


## Resources

Homepage: https://abax.ai/
