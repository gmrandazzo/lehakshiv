"""textcleaner.py lehakshiv text cleaner method

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

def cleantext(in_txt : str, out_txt : str):
    """
    Clean txt file removing unwanted worlds
    """
    with open(in_txt, "r", encoding="utf-8") as f_inp:
        with open(out_txt, "w", encoding="utf-8") as f_out:
            for line in f_inp:
                f_out.write(line)
