## Autonomous Language Interpreter
A.L.I. was developed as a tool for use in hospitals to help bridge the gap between language barriers in the medical environment. It is designed to work in place of a live interpreter who would normally be present for the conversation. A.L.I. is able to not only translate both text and speech as desired, but also provides additional functionality to allow the user to store notes parts of a conversation for up to 24 hours. Additionally, the user is able to access these notes regardless of location, so long as they are connected to the internet.

## Installation
A.L.I requires several installations before it is accessable to the user. The easiest way to do this is to install pip which can be done by running the command:
```python3 -m pip install --user --upgrade pip```

The user must then setup and navigate to a folder the project to be cloned to. You can then setup a local environment to install the proper packages which can be done by running:
```
python3 -m pip install --user virtualenv
python3 -m venv env
```
Following this, the user must then activate the virtual environment by running the following command in the env folder:
```env\Scripts\activate```

Finally the user must run the following pip commands:
```
pip install lxml
pip install Flask
pip install pandas
pip install pipwin 
pip install keyboard
pip install playsound
pip install google-cloud-speech
pip install google-cloud-translate 
pip install google-cloud-texttospeech
pipwin install pyaudio 
```

So long as the user has activated their environment and installed all the required packages, the user can then navigate to the location of the 'env' folder, clone the repository, and run the following command to launch the application.
```python3 server.py```

## Usage
Now the user should be directed to a login page. The user must click on signup and create an account using a company key stored in the 'companies' mysql database. The user can then sign into the app and gain full access to the software.

#### Homepage
To translate speech, navigate to the homepage, select an input and an output language and click on the mic icon. A.L.I will then listen to your speech and output the speech in the output language the user selected. You can stop translating by pressing the spacebar or by saying 'exit'. You can then view the input and the output by selecting the 'view text' button at the bottom. You can highlight particular sections from the category and click the highlighter icon in the middle to transfer this to the notes section. You can access the notes section click on the tab on the left side of the screen and then you can input a paitent, any relevant information, and whatever you highlighted after the translation occured, which the user can then access up to 24 hours later.

#### Translator Page
To translate text, click the Translator link on the navbar, you can then select an output language and any text entered on the left text area will be translated and displayed in the right textarea tag after clicking the 'go; button. 

#### Previous Entries
To view previously stored instruction or translations, click on the 'Previous Entries' tab from the navbar. The user can then see any entries saved from the interpreter from the last 24 hours.

## Credits
None of this could have been done without help from:
- @IAmDylanDennison
- @JarrettWoo
- @MatthewSherlin
- @SamH7798
- @SulfuricGoose
