DICOM PACS Client
=========
# About
Project on the subject of _Medical Information Systems_. 


The application is used to manage medical images in the PACS server service.
 It allows you to connect to the server using any user parameters and archive. 
Changing the user and the archive is done through the window called from the menu bar.

Tested: 

+PACS server - dcmqrscp 

+Operating system - Win10

+Python version: 3.7 (don't try on Python 2.x)

#### Author 
Kamil Kozieł

email: kkoziel@outlook.com

## Prepare virtual environment

First step to run application is create new python virtual environment

``` python
python3 -m venv venv
```
Next you have to active your environment
``` bash
 venv\Scripts\activate.bat
``` 
## Install requirements packages
``` bash
(venv) (...)> pip install (path_to_PACSClient)\requirements.txt
```
## Add gdcm dll to you Python directory

Copy files from res\dlls to C:\Users\(username)\AppData\Local\Programs\Python\Python37\DLLs

## Running app
To run app you should run you command prompt from StepToBum directory and then type:
``` bash
(venv) (path_to_PACSClient) > python PACSClient.py
```
