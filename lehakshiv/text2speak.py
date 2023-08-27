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

import pathlib
import logging
import os
import pyttsx3
import pdf2txt
import textcleaner


class TTS:
    """ pyttsx class to solve the hangs in runAndWait problem"""
    def __init__(self):
        """init TTS
        """
        self.engine = pyttsx3.init()

    def text2mp3(self,text_, out_audio):
        """text 2 mp3 converter function"""
        # self.engine.say(text_)
        self.engine.save_to_file(text_ ,
                                 out_audio)
        self.engine.runAndWait()

    def set_voice(self, num):
        """Set voice"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[num].id)


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
    def __init__(self,
                 in_work_dir,
                 out_work_dir) -> None:
        """
        Initialize the LText2Speak instance.

        Initializes the text-to-speech engine using the 'pyttsx3' library.
        """
        self.tts = TTS()
        self.in_work_dir = in_work_dir
        self.out_work_dir = out_work_dir

    def get_audio_file(self, file_name : str) -> str:
        """
        Convert text to speech and save as a txt file.

        This method processes the input by converting him into a txt files

        Args:
            file (str): The input file name

        Returns:
            str: The name of the output txt converted file
        """
        ext = pathlib.Path(f'{self.in_work_dir}/{file_name}').suffix[1:].lower()
        in_file = f'{self.in_work_dir}/{file_name}'
        out_file = f'{self.in_work_dir}/{file_name.replace(".pdf", ".txt")}'
        if ext == "pdf":
            pdf2txt.pdf2txt(in_file, out_file)
        elif ext == "txt":
            textcleaner.cleantext(in_file, out_file)
        else:
            logging.error("unable to covert the following extension %s", (ext))
            return -1
        chunks = []
        with open(out_file, "r", encoding="utf-8") as f_txt:
            text = ""
            i = 0
            for line in f_txt:
                if len(text.split(" ")) < 4096:
                    text += line
                else:
                    chunks.append(f'{self.in_work_dir}/{6:i}.mp3')
                    self.tts.text2mp3(text, chunks[-1])
                    text = line
                    i += 1
        return 0

    def merge_audio_files(self, chunks : list, out_name : str):
        """
        Convert text to speech and save as an audio file.
        """
        cat_str = "cat "+" ".join(chunks)+" > "+f'{out_name}'
        os.system(cat_str)
