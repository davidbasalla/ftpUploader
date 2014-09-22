ftpUploader
===========

This tool is a light weight application for uploading files to a web host via FTP. It's written in Python, using the ftputil module, and PyQT.
It's intended to speed up the process of uploading files to a web host, by reducing the number of manual selection of files.

Features to add:
- mirror file structure, so that a whole directory can be uploaded and updated in one go
- fix the callback for reporting back to the user - callback only prints to the QtConsole at the end of the file upload
