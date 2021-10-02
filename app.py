import flask
import ctypes
import time
import base64
from PIL import ImageGrab


SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
UP = 0xC8
LEFT = 0xCB
RIGHT = 0xCD
DOWN = 0xD0
ENTER = 0x1C
ESC = 0x01
TWO = 0x03

KEYEVENTF_SCANCODE = 0x8
KEYEVENTF_UNICODE = 0x4
KEYEVENTF_KEYUP = 0x2
SPACE = 0x39
INPUT_KEYBOARD = 1

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_UNICODE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, KEYEVENTF_UNICODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ScancodeDown(hex):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ScancodeUp(hex):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# directx scan codes
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html


def MoveMouse(x, y):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    #0x4000 - entire desktop
    #0x8000 - absolute coordinate
    #0x0001 - mouse move
    ii_.mi = MouseInput(x, y, 0, 0x0001 | 0x8000 | 0x4000, 0, ctypes.pointer(extra))
    mouse_event = ctypes.c_ulong(0)
    x = Input(mouse_event, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def LeftPress():
    extra = ctypes.c_ulong(0)
    mouse_event = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input(mouse_event, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def LeftRelease():
    extra = ctypes.c_ulong(0)
    mouse_event = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input(mouse_event, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def RightPress():
    extra = ctypes.c_ulong(0)
    mouse_event = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0008, 0, ctypes.pointer(extra))
    x = Input(mouse_event, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def RightRelease():
    extra = ctypes.c_ulong(0)
    mouse_event = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, 0x0010, 0, ctypes.pointer(extra))
    x = Input(mouse_event, ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def LeftClick():
    LeftPress()
    time.sleep(0.05)
    LeftRelease()

def RightClick():
    RightPress()
    time.sleep(0.05)
    RightRelease()

def process_mouse(args):
    action = args["action"]
    if action == "move":
        x, y = args["x"], args["y"]
        MoveMouse(x, y)
    elif action == "left":
        LeftClick()
    elif action == "right":
        RightClick()

def key_string(message):
    keys = [ord(ch) for ch in message]
    for key in keys:
        PressKey(key)
        ReleaseKey(key)

def process_key(args):
    input = args["input"]
    key_string(input)


screen_image = r"C:\Workspaces\Eclipse\eclipse-2019-03\hello\local_programs\Python\screen.jpg"
screen_image = r"C:\Programs\Programs\Python\screenshot.jpg"
vwidth = 65536
vheight = 65536

app = flask.Flask(__name__)

def screenshot():
    im = ImageGrab.grab(bbox = None)
    size = im.size
    im.save(screen_image, "JPEG")
    with open(screen_image, "rb") as fd:
        im = fd.read()
    im_encoded = base64.b64encode(im).decode("utf-8")
    return size, im_encoded

@app.route("/init", methods=['GET', 'POST'])
def init():
    args = flask.request.json
    for item in args.items(): print(item)
    (width, height), im_encoded = screenshot()
    response = {"status": True, "image": im_encoded, "width": width, "height": height}
    return flask.jsonify(response)

@app.route("/move", methods=['GET', 'POST'])
def move():
    args = flask.request.json
    for item in args.items(): print(item)
    x = int(args["x"] / args["width"] * vwidth)
    y = int(args["y"] / args["height"] * vheight)
    print(x, y)
    MoveMouse(x, y)
    return ""

@app.route("/left", methods=['GET', 'POST'])
def left_click():
    args = flask.request.json
    for item in args.items(): print(item)
    LeftClick()
    time.sleep(1)
    _, im_encoded = screenshot()
    response = {"status": True, "image": im_encoded}
    return flask.jsonify(response)

@app.route("/right", methods=['GET', 'POST'])
def right_click():
    args = flask.request.json
    for item in args.items(): print(item)
    RightClick()
    time.sleep(1)
    _, im_encoded = screenshot()
    response = {"status": True, "image": im_encoded}
    return flask.jsonify(response)

@app.route("/input", methods=['GET', 'POST'])
def input():
    args = flask.request.json
    for item in args.items(): print(item)
    input = args["input"]
    key_string(input)
    time.sleep(1)
    _, im_encoded = screenshot()
    response = {"status": True, "image": im_encoded}
    return flask.jsonify(response)

@app.route("/")
def hello():
    return """
<html>

<head>
    <title>Remote Control</title>
<style rel="stylesheet">
#scrImage {
    border: 2px solid black;
}

button {
    width: 10em;
    height: 2em;
}

#textInput {
    width: 25em;
    height: 2em;
}
</style>
</head>

<body>
    <img id="scrImage" />
    <br />
    <table>
        <tr>
            <td>
                <button id="leftButton">Left</button>
            </td>
            <td>
                <button id="rightButton">Right</button>
            </td>
            <td>
                <div style="width: 3em; height: 2em;"></div>
            </td>
            <td><input id="textInput" type="text"></td>
            <td>
                <button id="inputButton">Input</button>
            </td>
        </tr>
    </table>
    
<script type="text/javascript">
//var url = "http://192.168.29.198:50000";
//var url = "http://192.168.29.202:50000";
var url = "http://localhost:50000";

var scrWidth, scrHeight;
var imgWidth = 800;
var imgHeight;

var scrImage = document.getElementById("scrImage");
var leftButton = document.getElementById("leftButton");
var rightButton = document.getElementById("rightButton");
var textInput = document.getElementById("textInput");
var inputButton = document.getElementById("inputButton");

document.body.onload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url+"/init");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
       if (xhr.readyState === XMLHttpRequest.DONE) {
          data = JSON.parse(xhr.responseText);
          scrWidth = data.width;
          scrHeight = data.height;
          imgHeight = parseInt(imgWidth / scrWidth * scrHeight);
          scrImage.style.width = ""+imgWidth+"px";
          scrImage.style.height = ""+imgHeight+"px";
          scrImage.src = "data:image/jpg;base64," + data.image;
       }};
    
    var data = {};
    data.type = "screen";

    xhr.send(JSON.stringify(data));    
}

scrImage.onclick = function(ev) {
    console.log(ev);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url+"/move");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    
    var data = {};
    data.x = ev.offsetX;
    data.y = ev.offsetY;
    data.width = imgWidth;
    data.height = imgHeight;

    xhr.send(JSON.stringify(data));    
}

leftButton.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url+"/left");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
       if (xhr.readyState === XMLHttpRequest.DONE) {
          data = JSON.parse(xhr.responseText);
          scrImage.src = "data:image/jpg;base64," + data.image;
       }};
    
    var data = {};
    data.type = "screen";

    xhr.send(JSON.stringify(data));    
    
}

rightButton.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url+"/right");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
       if (xhr.readyState === XMLHttpRequest.DONE) {
          data = JSON.parse(xhr.responseText);
          scrImage.src = "data:image/jpg;base64," + data.image;
       }};
    
    var data = {};
    data.type = "screen";

    xhr.send(JSON.stringify(data));    
    
}

inputButton.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url+"/input");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function() {
       if (xhr.readyState === XMLHttpRequest.DONE) {
          data = JSON.parse(xhr.responseText);
          scrImage.src = "data:image/jpg;base64," + data.image;
       }};
    
    var data = {};
    data.input = textInput.value;

    xhr.send(JSON.stringify(data));    
    
}

</script>    
</body>

</html>    
"""    

if __name__ == "__main__":
    app.run("0.0.0.0", 50000)