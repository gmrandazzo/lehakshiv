"""lbackend.py lehakshiv backend

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

import tempfile
import pathlib
import shutil
from flask import (Flask,
                   jsonify,
                   make_response,
                   send_from_directory,
)

def convert_bytes(size):
    """Convert bytes to an useful size
    """
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f'{size:3.1f} {unit}'
        size /= 1024.0
    return size

class LBackend:
    """
    This module defines a Flask-based backend class, 'LBackend', 
    designed to manage file operations such as upload, download, removal, 
    and conversion. The class provides routes for various functionalities.

    Class: LBackend
    ----------------
    This class represents the backend service, equipped with methods for 
    handling file operations.

    Attributes:
        app (Flask): The Flask application instance.
        work_dir (TemporaryDirectory): 
            Temporary directory to store uploaded and converted files.

    Methods:
        __init__(self, name)
            Initializes the LBackend instance with the given name, 
            creates a Flask app, sets up the work directory, and defines
            routes for different operations.

        prepare(self)
            Prepares the backend's data structure by creating 'uploads' 
            and 'converted' directories within the work directory.

        index(self)
            Returns an HTML response displaying the backend's index page.

        upload(self, _request)
            Handles file upload. Accepts a file from the incoming request, 
            saves it to the 'uploads' directory, and returns a response
            indicating success or failure.

        download(self, filename)
            Handles file download. Attempts to send the specified file from
            the 'downloads' directory as an attachment in the response.

        remove(self, filename)
            Handles file removal. Deletes the specified file from both the
            'uploads' and 'downloads' directories and returns a response
            indicating success or failure.

        convert(self, filename)
            Converts the specified file into audio format. Returns a JSON
            response indicating the filename to be converted.

        run(self, host, port)
            Starts the backend server and listens for incoming requests on
            the specified host and port.

    Routes:
        /: Returns the backend's index page.
        /upload: Handles file uploads.
        /download/<filename>: Handles file downloads.
        /remove/<filename>: Handles file removal.
        /convert/<filename>: Handles file conversion.

    Example Usage:
    --------------
    backend = LBackend("my_backend")
    backend.run(host="0.0.0.0", port=8080)
    """
    # pylint: disable=unused-private-member
    def __init__(self, name) -> None:
        """
        Initialize the LBackend instance.

        Parameters:
            name (str): Name of the backend.
        """
        self.app = Flask(name)
        self.work_dir = tempfile.mkdtemp()
        print(self.work_dir)
        self.prepare()

        @self.app.route('/')
        def __index():
            """Backend index
            """
            return self.index()

        @self.app.route('/upload/', methods=['POST'])
        def __upload(_request):
            """upload method
            """
            return self.upload(_request)

        @self.app.route('/download/<filename>', methods=['GET'])
        def __download(filename):
            """download method
            """
            return self.download(filename)

        @self.app.route('/remove/<filename>', methods=['GET'])
        def __remove(filename):
            """remove method
            """
            return self.remove(filename)

        @self.app.route('/lsdir/', methods=['GET'])
        def __list_downloads():
            """download method
            """
            return self.list_downloads()

        @self.app.route('/convert/<filename>', methods=['GET'])
        def __convert(filename):
            """convert method
            """
            return self.convert(filename)

    def close(self):
        """Cleanup"""
        if pathlib.Path(self.work_dir).exists():
            shutil.rmtree(self.work_dir)

    def prepare(self):
        """Prepare backend data structure"""
        pathlib.Path(f'{self.work_dir}/uploads').mkdir(exist_ok=True)
        pathlib.Path(f'{self.work_dir}/converted').mkdir(exist_ok=True)

    def index(self):
        """Return index backend
        """
        return "<h1 style='color:blue'>lehakshiv backend</h1>"

    def upload(self, _request):
        """
        Upload a file inside the 'uploads' directory.

        Parameters:
            _request (Request): Incoming HTTP request containing the uploaded file.

        Returns:
            Response: JSON response indicating the success or failure of the upload.
        """
        try:
            fup = _request.files['file']
            fup.save(f'{self.work_dir}/uploads')
            return make_response(jsonify({"message": "upload ok",
                                          "severity": "INFO"}), 200)
        except FileNotFoundError as error_msg:
            return make_response(jsonify({"message": error_msg,
                                          "severity": "ERROR"}),
                                 404)

    def download(self, filename):
        """
        Download a file from the 'downloads' directory.

        Parameters:
            filename (str): Name of the file to be downloaded.

        Returns:
            Response: Response containing the specified file as an attachment, 
            or an error response if the file is not found.
        """
        try:
            send_from_directory(f'{self.work_dir}',
                                f'{filename}',
                                as_attachment=True)
            return make_response(jsonify({"message": "download ok.",
                                          "severity": "INFO"}),
                                 200)
        except FileNotFoundError as error_msg:
            return make_response(jsonify({"message": error_msg,
                                          "severity": "ERROR"}),
                                 404)

    def remove(self, filename):
        """
        Remove a file from both 'uploads' and 'downloads' directories.

        Parameters:
            filename (str): Name of the file to be removed.

        Returns:
            Response: JSON response indicating the success or failure of the removal.
        """
        try:
            pathlib.Path(f'{self.work_dir}/uploads/{filename}').unlink()
            pathlib.Path(f'{self.work_dir}/converted/{filename}').unlink()
            return make_response(jsonify({"message": f"file {filename} removed.",
                                          "severity": "INFO"}),
                                          200)
        except FileNotFoundError as error_msg:
            return make_response(jsonify({"message": error_msg,
                                          "severity": "ERROR"}),
                                 404)

    def list_downloads(self,):
        """
        List the contents of the 'downloads' folder.

        This function scans the 'downloads' folder specified by the 'work_dir'
        attribute, retrieves information about its contents, and returns a JSON
        response containing a list of files along with their sizes.

        Returns:
            Flask Response: JSON response containing folder contents or an error message.
        """
        full_path = pathlib.Path(f'{self.work_dir}/converted')
        print(full_path)
        if full_path.exists() is False:
            return make_response(jsonify({"message": "folder not found!",
                                          "severity": "ERROR"}),
                                          404)
        folder_contents = []
        for f_found in full_path.glob('**/*'):
            print(f_found)
            if f_found.is_file():
                folder_contents.append(
                    {"file": str(f_found.name),
                     "size": convert_bytes(f_found.stat().st_size)})
            else:
                continue
        print(folder_contents)
        return make_response(jsonify(folder_contents), 200)

    def convert(self, filename):
        """
        Convert the specified file into audio format.

        Parameters:
            filename (str): Name of the file to be converted.

        Returns:
            Response: JSON response indicating the filename to be converted.
        """
        return make_response(jsonify(filename))

    def run(self, host, port):
        """Run the backend"""
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    server = LBackend(__name__)
    server.run(host='0.0.0.0', port=7777)
