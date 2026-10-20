import streamlit as st


st.title("Audio Trimmer")
original_audio = st.file_uploader(label="Please upload audio file to edit:",
                                  type="audio",
                                  accept_multiple_files=False
                                  )
if original_audio:
    track = st.audio(
        original_audio,
        format="audio/mpeg",
        loop=True,
        alt="Audio to edit",
    )
    st.write("Please select what you would like to trim:")
else:
    pass
