import streamlit as st
from mutagen import File
import re


def check_format(timestamp):
    pattern = r"[0-9]+:[0-9]{2}"
    return re.fullmatch(pattern, timestamp)


def trim_audio():
    pass


def download_audio():
    pass


st.title("Audio Trimmer")
original_audio = st.file_uploader(label="Please upload audio file to edit:",
                                  type="audio",
                                  accept_multiple_files=False
                                  )
minutes = "0"
seconds = "00"
if original_audio:
    original_audio.seek(0)
    audio_info = File(original_audio)
    audio_length_seconds = 0
    if audio_info is not None:
        audio_length_seconds = audio_info.info.length
        minutes = int(audio_length_seconds // 60)
        seconds = int(audio_length_seconds % 60)
    track = st.audio(
        original_audio,
        format="audio/mpeg",
        loop=True,
        alt="Audio to edit",
    )
    st.write("Please select what you would like to trim:")
    new_start = st.text_input("Start time: ", value="0:00")
    new_end = st.text_input("End time: ", value=f"{minutes}:{seconds:02d}")
    new_end_time_seconds = (int(new_end.split(":")[0]) * 60) + int(new_end.split(":")[1])
    if check_format(new_start) and check_format(new_end) and audio_length_seconds >= new_end_time_seconds:
        st.button("Download trimmed Audio", disabled=False)
    else:
        st.button("Download trimmed Audio", disabled=True)
else:
    pass
