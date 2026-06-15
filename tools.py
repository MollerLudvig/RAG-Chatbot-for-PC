import subprocess
import webbrowser

tool_registry = []
tool_functions = {}

def tool(func):
    tool_registry.append({
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,  # reads the docstring
            "parameters": {}  # simple version, no parameters
        }
    })
    tool_functions[func.__name__] = func
    return func

@tool
def open_spotify():
    """Opens Spotify"""
    subprocess.Popen(["spotify.exe"])

@tool
def open_notepad():
    """Opens Notepad"""
    subprocess.Popen(["notepad.exe"])