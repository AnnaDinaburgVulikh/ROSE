# Managing a Class in Classroom

## Setup

1. Create a credentials.json file by using [google quickstart](https://developers.google.com/classroom/quickstart/python) (step 1)  
   Choose your app name, desktop app, and download client configuration(using button) to classroom directory.

2. Make sure that the following packages are installed: (step 2 in google guide, also included in ROSE pipfile for developers)
   - google-api-python-client
   - google-auth-httplib2
   - google-auth-oauthlib

3. In first run, an app authentication window will pop. Authorization for classroom.courses and classroom.rosters, allow both (creates token.pickle file).

## Functionality

First, make sure you are running the commands from the **classroom** directory.

For creating a course use:  

        `python rose_class.py -c "className"`

For retrieving existing classes and their IDs use:  

        `python rose_class.py -p`

For addressing a specific class use class ID:

        `python rose_class.py -i classID`

For adding students using a list  
(requires class ID and a file with mail addresses, accepts csv files):  

        `python rose_class.py -i classID -s file_path`

For adding teachers using a list  
(requires class ID and a file with mail addresses, accepts csv files):  

        `python rose_class.py -i classID -t file_path`

## Notice

- A mail can be added to teacher list or student list, not both.
- Only one invitation can exist for each mail. Before sending a new invitation the old one must be canceled.