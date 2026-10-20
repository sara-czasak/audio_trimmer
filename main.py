import streamlit as st
from mutagen import File
import re
from pydub import AudioSegment
from io import BytesIO
import time


def check_format(timestamp):
    pattern = r"[0-9]+:[0-5][0-9]"
    return re.fullmatch(pattern, timestamp)


def trim_audio(audio, start, end):
    audio.seek(0)
    audio_segment = AudioSegment.from_file(audio)
    new_track = audio_segment[(start * 1000):(end * 1000)]
    st.write(f"Start: {start} End: {end} Length: {len(new_track)}")
    st.session_state["to_download"] = new_track
    return new_track


def download_audio(track_to_download):
    time.sleep(4)
    buffer = BytesIO()
    track_to_download.export(buffer, format="mp3")
    buffer.seek(0)
    info = File(buffer)
    st.write(info.info.length)
    return buffer


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
    if check_format(new_start) and check_format(new_end):
        new_start_time_seconds = (int(new_start.split(":")[0]) * 60) + int(
            new_start.split(":")[1])
        new_end_time_seconds = (int(new_end.split(":")[0]) * 60) + int(
            new_end.split(":")[1])
        if audio_length_seconds >= new_end_time_seconds > new_start_time_seconds:
            st.button(label="Trim Audio",
                      disabled=False,
                      on_click=lambda: trim_audio(original_audio,
                                                  new_start_time_seconds,
                                                  new_end_time_seconds))
            if "to_download" in st.session_state:
                st.download_button(label="Download Audio",
                                   data=download_audio(
                                       st.session_state.to_download
                                   ),
                                   file_name=f"{original_audio.name.split('.')[0]}_trimmed.mp3")
        else:
            st.button(label="Trim Audio",
                      disabled=True)
    else:
        st.button(label="Trim Audio",
                  disabled=True)
else:
    pass
