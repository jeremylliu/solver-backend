## Word Hunt Solver Backend

This is the source code of the backend API that is accessed by the <ins>frontend website</ins>(https://github.com/jliuu1/solver-frontend) designed in Python utilizing the Flask framework. To function, this API recieves an image as an x64 string and processed attempt to extract the 4x4 GamePigeon board from the picture taken from the front end.

Here is an example of a processable image

![https://imgur.com/a/M9AlFMp](https://imgur.com/a/M9AlFMp)

Then, this image is processed through a variety of methods before the letters are extracted using a combination of OpenCV2 for boundery detection and PyTesseract for letter detection. Finally, the board is then sorted before it is returned to the frontend for a user confirmation.

Once a user confirms the state of the board (or manually enters it), the backend then proceeds to proceed through a recursive, backtracking algorithm to determine all possible combinations of words that can be made before it is returned to the frontend to be displayed.

## Getting started

Once you have the backend downloaded, you must run
```
source venv/bin/activate
```
to enter the virtual enviroment and then run
```
flask run
```
to begin running the backend server.
