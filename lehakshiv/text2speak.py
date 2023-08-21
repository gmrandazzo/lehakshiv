"""text2speak.py lehakshiv text conversion method

Copyright (C) <2023>  Giuseppe Marco Randazzo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pyttsx3


class LText2Speak:
    """
    LText2Speak

    This class provides methods to convert text to speech and save it as an audio file.
    It uses the 'pyttsx3' library for text-to-speech conversion.

    Attributes:
        engine (pyttsx3.init()): An instance of the pyttsx3 text-to-speech engine.

    Methods:
        text2mp3(text, outname):
            Converts the provided text to speech and saves it as an audio file.

        convert(text, outname):
            Converts the provided text to speech and saves it as an audio file.
            This method is a higher-level wrapper that uses 'text2mp3' internally.
            It's designed to process text in sequential chunks and merge 
            them into a single audio file.
    """
    def __init__(self) -> None:
        """
        Initialize the LText2Speak instance.

        Initializes the text-to-speech engine using the 'pyttsx3' library.
        """
        self.engine = pyttsx3.init()

    def text2mp3(self, text : str, outname : str):
        """
        Convert text to speech and save as an audio file.

        Args:
            text (str): The input text to convert to speech.
            outname (str): The name of the output audio file (e.g., "output.mp3").
        """
        self.engine.save_to_file(text, outname)
        self.engine.runAndWait()

    def convert(self, text : str, outname : str):
        """
        Convert text to speech and save as an audio file.

        This method processes the input text by splitting it into sequential chunks,
        converting each chunk to speech, and then merging the chunks into a single audio file.

        Args:
            text (str): The input text to convert to speech.
            outname (str): The name of the output audio file (e.g., "output.mp3").

        Returns:
            int: Always returns 0.
        """
        # 1) Take a txt
        # 2) Split into sequential chunck
        # 3) Convert each chunk
        # 4) Merge the final mp3 with the senquential chunck
        self.text2mp3(text, outname)
        return 0
