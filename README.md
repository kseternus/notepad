# Notepad

A simple Python-based text editor with basic functionality. This lightweight application is designed to demonstrate text handling, file operations, and UI creation using Python's `tkinter` library.

## Features

- **Open, Save, Save As**  
  - Allows the user to open an existing file, save the current file (if new, works as "Save As"), or save as a new file.
- **Print**  
  - Sends the file to a printer.
- **Undo, Redo**  
  - Allows unlimited undo and redo actions.
- **Cut, Copy, Paste, Delete, Select All**  
  - Standard text editing functionality.
- **Find & Replace**  
  - Opens a new window to find a symbol or word, replace selected occurrences or all occurrences, and displays the number of matches.
- **Time and Date**  
  - Inserts the current time and date at the text cursor position.
- **Font**  
  - Allows changing the font type and size.
- **Option Bar and Status Bar**  
  - Toggle the option bar, which has shortcuts for `Open`, `Save As`, `Print`, `Find & Replace`, `Undo`, `Redo`, and font type and size selection.
  - Toggle the status bar to display character and line counts and the document's character encoding.
- **Text Wrapping**  
  - Toggle text wrapping on or off.

## Installation

- **Installation**
  - `pip install pyperclip`
  - `pip install pywin32`

- **Clone this repository:**
   ```bash
   git clone https://github.com/kseternus/notepad.git
   cd notepad