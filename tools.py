import subprocess
import webbrowser
import inspect
import pyautogui

tool_registry = []
tool_functions = {}

def tool(func):

    sig = inspect.signature(func)
    properties = {}
    required = []

    for name, param in sig.parameters.items():
        properties[name] = {
            "type": "string",
            "description": name
        }
        if param.default == inspect.Parameter.empty:
            required.append(name)

    tool_registry.append({
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,  # reads the docstring
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    })
    tool_functions[func.__name__] = func
    return func

@tool
def open_app(app: str):
    """Opens a desktop application by executable name. Use for apps like Spotify, Notepad, Calculator. NOT for websites or URLs."""
    subprocess.Popen([app])

@tool
def open_browser_window(url: str = "https://google.com"):
    """Opens a website URL in Chrome browser. Use for websites, news, online content. NOT for desktop applications."""
    webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(url)

# Not currently working too well, kinda inconsistent
@tool
def press_key_combination(keys: str):
    """Presses the keys on the keyboard"""
    keys_list = keys.replace(",", " ").split()
    pyautogui.hotkey(keys_list)
