import pyperclip

def copy_to_user_keyboard(text: str) -> str:
    """Use this to copy some text to the user keyboard. Before using it make sure that user want's it, if unsure - ask.
  
    Args:
      text: Text that will be pasted into the user's keyboard.

    Returns:
      String with status of tool usage(Succes or error)
    """
    try:
        pyperclip.copy(text)
        return "Successfuly copied text to user keyboard"
    except:
        return "There was some problem with tool, haven't copied text to user keyboard."

def paste_from_user_keyboard() -> str:
    """Use this to get text copied in user keyboard. Use it if you sure user want's it.
  
    Args:
      None

    Returns:
      Text that currently coppied in the user's keyboard.
    """

    try:
        text = pyperclip.paste()
        return text.strip()
    except:
        return "There was some problem with tool, haven't pasted text from user keyboard."
    
