import os
import tempfile
from datetime import datetime

import pyperclip
import win32api
import win32print

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def open_file():
    """Opens a file dialog to select a text file and displays its content in the text field."""
    global open_flag
    global filepath

    filepath = askopenfilename(filetypes=[('text file', '*.txt')])
    name = os.path.basename(filepath)

    if not filepath:
        return

    text_field.delete('1.0', 'end-1c')

    with open(filepath, 'r', encoding='utf8') as f:
        content = f.read()
        text_field.insert('end-1c', content)

    root.title(f'{name} | Notepad')
    open_flag = True
    return filepath


def save():
    """Saves the current content to the existing file or prompts for a new file if it hasn't been saved before."""
    global open_flag
    global filepath

    if open_flag:
        with open(filepath, 'w', encoding='utf8') as f:
            content = text_field.get('1.0', 'end-1c')
            f.write(content)
    else:
        filepath = asksaveasfilename(filetypes=[('text file', '*.txt')], )
        name = os.path.basename(filepath)

        if not filepath:
            return

        with open(filepath, 'w', encoding='utf8') as f:
            content = text_field.get('1.0', 'end-1c')
            f.write(content)
        root.title(f'{name} | Notepad')


def save_file_as():
    """Prompts the user to save the current content to a new file."""
    global filepath

    filepath = asksaveasfilename(filetypes=[('text file', '*.txt')])
    name = os.path.basename(filepath)

    if not filepath:
        return

    with open(filepath, 'w', encoding='utf8') as f:
        content = text_field.get('1.0', 'end-1c')
        f.write(content)

    root.title(f'{name} | Notepad')


def printer():
    """Opens a print dialog to allow the user to select a printer and print the current content."""
    installed_printers = list(win32print.EnumPrinters(2))
    installed_printers_list = [printer[2] for printer in installed_printers]  # Extract printer names

    # Setup printer selection window
    printers_window = tk.Tk()
    printers_window.title('Select printer')
    printers_window.geometry('300x150')
    printers_window.resizable(False, False)
    title = tk.Label(printers_window, text='Select printer:', font=('Arial', 12))
    title.pack(pady=(15, 0))

    # Combobox to select printer
    selected_printer_var = tk.StringVar(printers_window)
    printers_combobox = ttk.Combobox(
        printers_window, width=40, state='readonly', values=installed_printers_list, textvariable=selected_printer_var
    )
    printers_combobox.pack(pady=(15, 0))
    printers_combobox.set(installed_printers_list[-1])  # Set default printer

    def print_in_selected():
        """Sets the selected printer as default and sends the current content to print."""
        selected_printer = selected_printer_var.get()
        win32print.SetDefaultPrinter(selected_printer)
        content = text_field.get('1.0', 'end-1c')
        filename = tempfile.mktemp(".txt")
        open(filename, "w").write(content)
        win32api.ShellExecute(0, 'printto', filename, '"%s"' % win32print.GetDefaultPrinter(), '.', 0)
        printers_window.destroy()

    print_button = tk.Button(printers_window, text='Print', command=print_in_selected)
    print_button.pack(pady=(30, 0))


def exit_program():
    """Opens a confirmation dialog to ask the user if they want to exit the application."""
    exit_window = tk.Toplevel()
    exit_window.title('Exit')
    exit_window.geometry('200x150')
    exit_window.resizable(False, False)
    statement = tk.Label(exit_window, text='Are you sure?', font=('Arial', 12))
    statement.pack(pady=(30, 0))
    yes_button = tk.Button(exit_window, text='Yes', width=5, font=('Arial', 12), command=root.quit)
    yes_button.pack(side='left', padx=(30, 0))
    no_button = tk.Button(exit_window, text='No', width=5, font=('Arial', 12), command=exit_window.destroy)
    no_button.pack(side='right', padx=(0, 30))


def font_type(*args):
    """Applies the selected font type and size to the text field."""
    global size

    type_font = font_combobox.get()
    size = font_size_combobox.get()
    size = int(size)
    text_field.configure(font=(type_font, size))


def hide():
    """Toggles visibility of the option bar and status bar based on user selection."""
    hide_option_checked = hide_option_var.get()
    hide_status_checked = hide_status_var.get()

    # Hide/show the top option bar
    if hide_option_checked == 0:
        option_bar.pack_forget()
    elif hide_option_checked == 1:
        text_field.pack_forget()
        vertical_scroll.pack_forget()
        option_bar.pack(fill='x', anchor='n')
        vertical_scroll.pack(fill='y', side='right')
        text_field.pack(fill='both', expand=True)

    # Hide/show the bottom status bar
    if hide_status_checked == 0:
        bottom_bar.pack_forget()
    elif hide_status_checked == 1:
        text_field.pack_forget()
        vertical_scroll.pack_forget()
        horizontal_scroll.pack_forget()
        bottom_bar.pack(fill='x', side='bottom')
        vertical_scroll.pack(fill='y', side='right')
        horizontal_scroll.pack(fill='x', side='bottom')
        text_field.pack(fill='both', expand=True)


def show_menu_mouse(event):
    """Displays the context menu when the user right-clicks within the text field."""
    edit_menu_mouse.post(event.x_root, event.y_root)


def wrap():
    """Toggles text wrapping mode in the text field."""
    wrap_checked = wrap_var.get()

    if wrap_checked == 0:
        text_field.configure(wrap='none')
    elif wrap_checked == 1:
        text_field.configure(wrap='word')


def undo_command():
    """Undoes the last action in the text field."""
    text_field.edit_undo()


def redo_command():
    """Redoes the previously undone action in the text field."""
    text_field.edit_redo()


def cut_command():
    """Cuts the selected text and copies it to the clipboard."""
    sel_start, sel_end = text_field.tag_ranges('sel')
    cut = text_field.get(sel_start, sel_end)
    pyperclip.copy(cut)
    text_field.delete(sel_start, sel_end)


def copy_command():
    """Copies the selected text to the clipboard."""
    sel_start, sel_end = text_field.tag_ranges('sel')
    cut = text_field.get(sel_start, sel_end)
    pyperclip.copy(cut)


def paste_command():
    """Pastes the clipboard content at the current cursor position in the text field."""
    text_field.insert(tk.INSERT, root.clipboard_get())


def delete_command():
    """Deletes the selected text from the text field."""
    sel_start, sel_end = text_field.tag_ranges('sel')
    text_field.delete(sel_start, sel_end)


def select_command():
    """Selects all the text in the text field."""
    text_field.tag_add('sel', '1.0', 'end-1c')


def time_and_date():
    """Inserts the current date and time at the cursor position."""
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y %H:%M:%S")
    text_field.insert(tk.INSERT, date_string)


def about():
    """Displays information about the application."""
    about_window = tk.Toplevel()
    about_window.title('About')
    about_window.geometry('200x180')
    about_window.resizable(False, False)
    about_info = tk.Label(about_window, text='Notepad\n'
                                             'Version: 0.2 beta\n\n'
                                             'Made by:\n'
                                             'Kamil Seternus\n'
                                             '2024',
                          font=('Arial', 12))
    about_info.pack(pady=(30, 0))


def get_font_type(font):
    """Sets the font type in the font selection combobox."""
    font_combobox.set(font)


def get_font_size(size):
    """Sets the font size in the font selection combobox."""
    font_size_combobox.set(size)


def count_characters_func(event):
    """Updates character and line count in the status bar."""
    count_char = len(text_field.get('1.0', 'end'))
    lines = text_field.get('1.0', 'end').count('\n')
    count_characters.configure(text=f'{count_char - 1} characters | {lines} lines')
    utf_label.configure(text='UTF-8')


def find_replace():
    """Opens a window to find and replace text within the text field."""
    # Create window
    find_window = tk.Toplevel()
    find_window.title('Find and Replace')
    find_window.geometry('400x250')
    find_window.resizable(False, False)

    # Frame for the entries and buttons
    frame = tk.Frame(find_window)
    frame.pack(padx=10, pady=10)

    # Variable to hold the found indices and the current index
    found_indices = []
    current_index = -1  # Start at -1 for the first "Find Next" call
    last_search_text = ""

    # Create a tag for highlighting found text
    text_field.tag_configure('highlight', foreground='blue', background='light blue')  # Example style

    def update_count_label():
        """Updates the count of found occurrences."""
        count_label.config(text=f'Occurrences: {len(found_indices)}')

    def clear_highlights():
        """Removes all current highlights."""
        text_field.tag_remove('highlight', '1.0', 'end')

    def highlight_next_occurrence():
        """Selects the next occurrence of the found text in the main text field."""
        nonlocal current_index, last_search_text
        search_text = find_entry.get()

        # Reset if new search text is different from the last search
        if search_text != last_search_text:
            clear_highlights()  # Clear previous highlights
            found_indices.clear()
            current_index = -1
            last_search_text = search_text

        # Clear previous highlights if no search text is provided
        if not search_text:
            update_count_label()
            return

        # Remove previous selection if one exists
        if found_indices and current_index >= 0:
            start, end = found_indices[current_index]
            text_field.tag_remove('highlight', start, end)  # Remove previous highlight

        # Search for occurrences if the list is empty
        if not found_indices:
            start_index = '1.0'
            while True:
                start_index = text_field.search(search_text, start_index, stopindex='end')
                if not start_index:
                    break
                end_index = f"{start_index}+{len(search_text)}c"
                found_indices.append((start_index, end_index))
                start_index = end_index

            update_count_label()  # Update count after search

        # Update index to highlight the next occurrence
        if found_indices:
            current_index = (current_index + 1) % len(found_indices)  # Wrap around
            start, end = found_indices[current_index]
            text_field.tag_add('highlight', start, end)  # Highlight the found occurrence
            text_field.mark_set('insert', start)  # Set cursor to start of found text
            text_field.see(start)  # Scroll to the highlighted occurrence

            # Optionally create a selection-like effect
            text_field.tag_add('sel', start, end)  # This creates a selection

    def replace_selection():
        """Replaces the currently selected text with the input from the replace entry."""
        try:
            sel_start = text_field.index(tk.SEL_FIRST)  # Get the start of the selection
            sel_end = text_field.index(tk.SEL_LAST)  # Get the end of the selection
            text_field.delete(sel_start, sel_end)  # Delete the selected text
            text_field.insert(sel_start, replace_entry.get())  # Insert the new text

            # Reset found indices and current index
            found_indices.clear()
            current_index = -1
            clear_highlights()  # Clear highlights after replacement
            highlight_next_occurrence()  # Update highlights after replacement
        except tk.TclError:
            print("No text selected for replacement.")  # Log message if nothing is selected

    def replace_all():
        """Replaces all occurrences of the searched text with the replacement text."""
        search_text = find_entry.get()
        replace_text = replace_entry.get()

        content = text_field.get('1.0', 'end-1c')
        new_content = content.replace(search_text, replace_text)
        text_field.delete('1.0', 'end-1c')
        text_field.insert('end-1c', new_content)

        # Reset found indices and current index
        found_indices.clear()
        current_index = -1
        clear_highlights()  # Clear highlights after replacement
        update_count_label()  # Update count after replacement

    # Create buttons and entries
    # Entry for text to find
    find_label = tk.Label(frame, text='Find:')
    find_label.grid(row=0, column=0, pady=(10, 0), sticky='w')
    find_entry = tk.Entry(frame, width=40)
    find_entry.grid(row=1, column=0, pady=(5, 10))

    # Entry for text to replace with
    replace_label = tk.Label(frame, text='Replace with:')
    replace_label.grid(row=2, column=0, pady=(10, 0), sticky='w')
    replace_entry = tk.Entry(frame, width=40)
    replace_entry.grid(row=3, column=0, pady=(5, 10))

    # Button for finding next occurrence
    find_next_button = tk.Button(frame, text='Find Next', command=highlight_next_occurrence, width=15)
    find_next_button.grid(row=1, column=1, padx=(10, 0), pady=(5, 10), sticky='nsew')

    # Button for replacing selected text
    replace_selected_button = tk.Button(frame, text='Replace Selected', command=replace_selection, width=15)
    replace_selected_button.grid(row=2, column=1, padx=(10, 0), pady=(5, 10), sticky='nsew')

    # Button for replacing all text
    replace_all_button = tk.Button(frame, text='Replace All', command=replace_all, width=15)
    replace_all_button.grid(row=3, column=1, padx=(10, 0), pady=(5, 10), sticky='nsew')

    # Label to show occurrence count
    count_label = tk.Label(frame, text='Occurrences: 0')
    count_label.grid(row=4, column=0, pady=(5, 10), sticky='w')


# Font and size lists used for font selection in menus and comboboxes
fonts = ['Arial', 'Times New Roman', 'Comic Sans MS', 'Courier New', 'Impact']
sizes = ['8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '56', '64']

# Global variables to manage file state
open_flag = False  # Tracks if a file is currently open
filepath = ''  # Stores the path of the currently opened or saved file

# Set up the main application window
root = tk.Tk()
root.title('New text file | Notepad')
root.geometry('1200x600')
root.minsize(600, 300)

# Main menu bar setup
main_menu = tk.Menu(root)

# File menu: contains options for file management
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save as...', command=save_file_as)
file_menu.add_command(label='Print', command=printer)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_program)

# Edit menu: contains options for text editing actions
edit_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Undo', command=undo_command)
edit_menu.add_command(label='Redo', command=redo_command)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', command=cut_command)
edit_menu.add_command(label='Copy', command=copy_command)
edit_menu.add_command(label='Paste', command=paste_command)
edit_menu.add_command(label='Delete', command=delete_command)
edit_menu.add_command(label='Select All', command=select_command)
edit_menu.add_command(label='Find & Replace', command=find_replace)
edit_menu.add_separator()
edit_menu.add_command(label='Time and date', command=time_and_date)

# Right-click context menu for editing (bound to right mouse button)
main_menu_mouse = tk.Menu(root)
edit_menu_mouse = tk.Menu(main_menu_mouse, tearoff=0)
main_menu_mouse.add_cascade(label='Edit', menu=edit_menu_mouse)
edit_menu_mouse.add_command(label='Undo', command=undo_command)
edit_menu_mouse.add_command(label='Redo', command=redo_command)
edit_menu_mouse.add_separator()
edit_menu_mouse.add_command(label='Cut', command=cut_command)
edit_menu_mouse.add_command(label='Copy', command=copy_command)
edit_menu_mouse.add_command(label='Paste', command=paste_command)
edit_menu_mouse.add_command(label='Delete', command=delete_command)
edit_menu_mouse.add_command(label='Select All', command=select_command)
edit_menu_mouse.add_separator()
edit_menu_mouse.add_command(label='Time and date', command=time_and_date)

# View menu: controls display settings like font, wrapping, and status bar visibility
view_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='View', menu=view_menu)

# Font submenu for selecting font type and size
font_menu = tk.Menu(view_menu, tearoff=0)
view_menu.add_cascade(label='Font', menu=font_menu)

# Submenu for selecting font type
font_menu_type = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label='Font type', menu=font_menu_type)

# Populate font type submenu with font options
for font in fonts:
    font_menu_type.add_command(label=font, command=lambda font=font: get_font_type(font))

# Submenu for selecting font size
font_menu_size = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label='Size', menu=font_menu_size)

# Populate font size submenu with size options
for size in sizes:
    font_menu_size.add_command(label=size, command=lambda size=size: get_font_size(size))

# About menu with application information
about_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About', command=about)

# Additional view options for option and status bars, and text wrapping
view_menu.add_separator()
hide_option_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Option bar', onvalue=1, offvalue=0, command=hide, variable=hide_option_var)
hide_status_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Status bar', onvalue=1, offvalue=0, command=hide, variable=hide_status_var)
wrap_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Text wrapping', onvalue=1, offvalue=0, command=wrap, variable=wrap_var)

# Apply main menu to the application window
root.config(menu=main_menu)

# Option bar with buttons for quick access to file and edit actions
option_bar = tk.Frame(root, height=50)
option_bar.pack(fill='both', anchor='n')

open_button = tk.Button(option_bar, text='📂', command=open_file)
open_button.pack(side='left', padx=5, pady=2, anchor='center')

save_button = tk.Button(option_bar, text='💾', command=save)
save_button.pack(side='left', pady=2, anchor='center')

printer_button = tk.Button(option_bar, text='🖨', command=printer)
printer_button.pack(side='left', padx=5, pady=2, anchor='center')

printer_button = tk.Button(option_bar, text='🔍', command=find_replace)
printer_button.pack(side='left', padx=5, pady=2, anchor='center')

undo_button = tk.Button(option_bar, text=' ↩', command=undo_command)
undo_button.pack(side='left', pady=2, anchor='center')

redo_button = tk.Button(option_bar, text='↪ ', command=redo_command)
redo_button.pack(side='left', padx=5, pady=2, anchor='center')

# Font selection combobox for font type
font_combobox_var = tk.StringVar()
font_combobox = ttk.Combobox(option_bar, width=20, state='readonly', textvariable=font_combobox_var, values=fonts)
font_combobox.set('Arial')  # Set default font
font_combobox.pack(side='left', padx=5, pady=2, anchor='center')
font_combobox_var.trace('w', font_type)

# Font size combobox for font size
font_size_combobox_var = tk.StringVar()
font_size_combobox = ttk.Combobox(option_bar, width=5, state='readonly', textvariable=font_size_combobox_var, values=sizes)
font_size_combobox.set('12')  # Set default size
font_size_combobox.pack(side='left', padx=5, pady=2, anchor='center')
font_size_combobox_var.trace('w', font_type)

# Status bar at the bottom to display character and line count
bottom_bar = tk.Label(root, height=50)
bottom_bar.pack(fill='both', anchor='s', side='bottom')

# Vertical and horizontal scrollbars for text area
vertical_scroll = ttk.Scrollbar(root, orient='vertical')
vertical_scroll.pack(fill='y', side='right')
horizontal_scroll = ttk.Scrollbar(root, orient='horizontal')
horizontal_scroll.pack(fill='x', side='bottom')

# Main text field setup
text_field = tk.Text(root, wrap='word', font=('Arial', 12), yscrollcommand=vertical_scroll.set, xscrollcommand=horizontal_scroll.set, undo=True)
text_field.pack(fill='both', expand=True)
vertical_scroll.config(command=text_field.yview)
horizontal_scroll.config(command=text_field.xview)
# Highlight tag configuration
text_field.tag_config('highlight', background='lightblue')  # Use light blue for selection highlight

# Key bindings for real-time character and line count updates and context menu display
text_field.bind('<KeyPress>', count_characters_func)
text_field.bind('<KeyRelease>', count_characters_func)
root.bind('<Button-3>', show_menu_mouse)

# Display for character count and encoding
count_characters = tk.Label(bottom_bar, text='0 characters | 1 lines')
count_characters.pack(side='left', padx=10, anchor='center')
utf_label = tk.Label(bottom_bar, text='UTF-8')
utf_label.pack(side='right', padx=10)

# Start the Tkinter main loop
root.mainloop()
