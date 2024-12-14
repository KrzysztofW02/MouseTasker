# MouseTasker

MouseTasker is an application designed to automate mouse tasks. It allows users to record, save, and replay sequences of mouse actions.


![MouseTasker Screenshot](https://drive.google.com/uc?export=view&id=1C6CAHBLAO72aun3AdOTlvFBJtqV0u5LI)

## Installation

Clone this repository and install the required packages:

```sh
git clone https://github.com/KrzysztofW02/MouseTasker.git
cd MouseTasker
python3 -m venv venv
```
For Unix and MacOS systems: 
```sh
source venv/bin/activate
```
For Windows systems:
```sh
venv\Scripts\activate
```
Then
```sh
pip install -r requirements.txt
```
## Usage

To start MouseTasker, navigate to the project directory and run:

python main.py

## Mouse Recording

The Mouse Recording feature allows you to record complex mouse movements and play them back with precise timing. 

![Demo](https://s6.ezgif.com/tmp/ezgif-6-947300915b.gif)
1. Click the Record Mouse Actions button or "F10" to start recording.
2. Perform the desired mouse actions (moving, clicking).
3. Click the button again or "F10" to stop the recording.
4. The recorded actions will appear in the actions list, including paths.
5. Use the Save and Load options to export or import recorded sequences.

## AI CHAT 

If you're unsure how to use the app, you can click on button "Open Chat" and ask a question in the chat, which will guide you on how to do something.

![MouseTasker Screenshot](https://drive.google.com/uc?export=view&id=18NzD1Ab1vXUfIFHD3TuEJAztLugErZGe)

To use the chat, you'll need to obtain a free API key from [https://console.groq.com/keys](https://console.groq.com/keys) and set it as the environment variable `GROQ_API_KEY`.


## Viewing Shortcuts

To view available shortcuts within MouseTasker:

- Press `F5` on your keyboard, or
- Navigate through the menu by selecting `Help` followed by `Shortcuts`.

This will display a list of shortcuts you can use to enhance your experience with MouseTasker.

