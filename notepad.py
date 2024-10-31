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
    installed_printers = list(win32print.EnumPrinters(2))
    installed_printers_list = []

    for i in installed_printers:
        installed_printers_list.append(i[2])

    printers_window = tk.Tk()
    printers_window.title('Select printer')
    printers_window.geometry('300x150')
    printers_window.resizable(False, False)
    title = tk.Label(printers_window, text='Select printer:', font=('Arial', 12))
    title.pack(pady=(15, 0))
    selected_printer_var = tk.StringVar(printers_window)
    printers_combobox = ttk.Combobox(printers_window, width=40, state='readonly', values=installed_printers_list,
                                     textvariable=selected_printer_var)
    printers_combobox.pack(pady=(15, 0))
    printers_combobox.set(installed_printers_list[-1])

    def print_in_selected():
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
    global size

    type_font = font_combobox.get()
    size = font_size_combobox.get()
    size = int(size)
    text_field.configure(font=(type_font, size))


def hide():
    hide_option_checked = hide_option_var.get()
    hide_status_checked = hide_status_var.get()

    # hide top option bar
    if hide_option_checked == 0:
        option_bar.pack_forget()
    # show option bar again, need to forget text field and vertical scroll to pack it again in correct order
    # to prevent messing up layout of windows
    elif hide_option_checked == 1:
        text_field.pack_forget()
        vertical_scroll.pack_forget()
        option_bar.pack(fill='x', anchor='n')
        vertical_scroll.pack(fill='y', side='right')
        text_field.pack(fill='both', expand=True)

    # hide bottom bar
    if hide_status_checked == 0:
        bottom_bar.pack_forget()
    # show bottom bar again, need to forget text field and vertical with horizontal scroll to pack it again in correct
    # order to prevent messing up layout of windows
    elif hide_status_checked == 1:
        text_field.pack_forget()
        vertical_scroll.pack_forget()
        horizontal_scroll.pack_forget()
        bottom_bar.pack(fill='x', side='bottom')
        vertical_scroll.pack(fill='y', side='right')
        horizontal_scroll.pack(fill='x', side='bottom')
        text_field.pack(fill='both', expand=True)


def show_menu_mouse(event):
    edit_menu_mouse.post(event.x_root, event.y_root)


def wrap():
    wrap_checked = wrap_var.get()

    if wrap_checked == 0:
        text_field.configure(wrap='none')
    elif wrap_checked == 1:
        text_field.configure(wrap='word')


def undo_command():
    text_field.edit_undo()


def redo_command():
    text_field.edit_redo()


def cut_command():
    sel_start, sel_end = text_field.tag_ranges('sel')
    cut = text_field.get(sel_start, sel_end)
    pyperclip.copy(cut)
    text_field.delete(sel_start, sel_end)


def copy_command():
    sel_start, sel_end = text_field.tag_ranges('sel')
    cut = text_field.get(sel_start, sel_end)
    pyperclip.copy(cut)


def paste_command():
    text_field.insert(tk.INSERT, root.clipboard_get())


def delete_command():
    sel_start, sel_end = text_field.tag_ranges('sel')
    text_field.delete(sel_start, sel_end)


def select_command():
    text_field.tag_add('sel', '1.0', 'end-1c')


def time_and_date():
    now = datetime.now()
    date_string = now.strftime("%d/%m/%Y %H:%M:%S")
    text_field.insert(tk.INSERT, date_string)


def about():
    about_window = tk.Toplevel()
    about_window.title('About')
    about_window.geometry('200x180')
    about_window.resizable(False, False)
    about_info = tk.Label(about_window, text='Notepad\n'
                                             'Version: 0.3 beta\n\n'
                                             'Made by:\n'
                                             'Kamil Seternus\n'
                                             '2024',
                          font=('Arial', 12))
    about_info.pack(pady=(30, 0))


def get_font_type(font):
    font_combobox.set(font)


def get_font_size(size):
    font_size_combobox.set(size)


def count_characters_func(event):
    count_char = len(text_field.get('1.0', 'end'))
    lines = text_field.get('1.0', 'end')
    lines = lines.count('\n')
    count_characters.configure(text=f'{count_char - 1} characters | {lines} lines')
    utf_label.configure(text='UTF-8')


# this function is placeholder for testing new functionalities
def do_nothing():
    pass


# lists of fonts and font sizes used by submenus and combobox, different variables
fonts = ['Arial', 'Times New Roman', 'Comic Sans MS', 'Courier New', 'Impact']
sizes = ['8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '36', '48', '56', '64']
open_flag = False
filepath = ''


# make main window
root = tk.Tk()
root.title(f'New text file | Notepad')
root.geometry('1200x600')
root.minsize(600, 300)

# making main menu bar
main_menu = tk.Menu(root)
# menu save, open, edit etc
file_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save as...', command=save_file_as)
file_menu.add_command(label='Print', command=printer)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_program)

# menu with all functions to edit text
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
edit_menu.add_separator()
edit_menu.add_command(label='Time and date', command=time_and_date)

# edit menu bound to RMB
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

# view menu with font type, size selection, text wrapping and status bar
view_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='View', menu=view_menu)

# make submenu font
font_menu = tk.Menu(main_menu, tearoff=0)
view_menu.add_cascade(label='Font', menu=font_menu)

# make submenu to font with font types
font_menu_type = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label='Font type', menu=font_menu_type)

# make loop to make submenu in submenu font types with all font types from list
for font in fonts:
    font_menu_type.add_command(label=font, command=lambda font='font': get_font_type(font))

# make submenu to font with font sizes
font_menu_size = tk.Menu(font_menu, tearoff=0)
font_menu.add_cascade(label='Size', menu=font_menu_size)

# make loop to make submenu in submenu font sizes with all font sizes from list
for size in sizes:
    font_menu_size.add_command(label=size, command=lambda size='size': get_font_size(size))

about_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About', command=about)

# rest of menu
view_menu.add_separator()
hide_option_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Option bar', onvalue=1, offvalue=0, command=hide, variable=hide_option_var)
hide_status_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Status bar', onvalue=1, offvalue=0, command=hide, variable=hide_status_var)
wrap_var = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Text wrapping', onvalue=1, offvalue=0, command=wrap, variable=wrap_var)

# create main menus
root.config(menu=main_menu)

option_bar = tk.Frame(root, height=50)
option_bar.pack(fill='both', anchor='n')

open_button = tk.Button(option_bar, text='📂', command=open_file)
open_button.pack(side='left', padx=5, pady=2, anchor='center')

save_button = tk.Button(option_bar, text='💾', command=save)
save_button.pack(side='left', pady=2, anchor='center')

printer_button = tk.Button(option_bar, text='🖨', command=printer)
printer_button.pack(side='left', padx=5, pady=2, anchor='center')

undo_button = tk.Button(option_bar, text='↩', command=undo_command)
undo_button.pack(side='left', pady=2, anchor='center')

redo_button = tk.Button(option_bar, text='↪', command=redo_command)
redo_button.pack(side='left', padx=5, pady=2, anchor='center')

font_combobox_var = tk.StringVar()
font_combobox = ttk.Combobox(option_bar, width=20, state='readonly', textvariable=font_combobox_var,
                             values=fonts)
font_combobox.set('Arial')
font_combobox.pack(side='left', padx=5, pady=2, anchor='center')
font_combobox_var.trace('w', font_type)

font_size_combobox_var = tk.StringVar()
font_size_combobox = ttk.Combobox(option_bar, width=5, state='readonly', textvariable=font_size_combobox_var,
                                  values=sizes)
font_size_combobox.set('16')
font_size_combobox.pack(side='left', padx=5, pady=2, anchor='center')
font_size_combobox_var.trace('w', font_type)

bottom_bar = tk.Label(root, height=50)
bottom_bar.pack(fill='both', anchor='s', side='bottom')

vertical_scroll = ttk.Scrollbar(root, orient='vertical')
vertical_scroll.pack(fill='y', side='right')
horizontal_scroll = ttk.Scrollbar(root, orient='horizontal')
horizontal_scroll.pack(fill='x', side='bottom')

# main window where you work on your PhD
text_field = tk.Text(root, wrap='word', height=5, font=('Arial', 24), yscrollcommand=vertical_scroll.set,
                     xscrollcommand=horizontal_scroll.set, undo=True)
text_field.pack(fill='both', expand=True)
vertical_scroll.config(command=text_field.yview)
horizontal_scroll.config(command=text_field.xview)

# key bindings
text_field.bind('<KeyPress>', count_characters_func)
text_field.bind('<KeyRelease>', count_characters_func)
root.bind('<Button-3>', show_menu_mouse)

count_characters = tk.Label(bottom_bar, text='0 characters | 1 lines')
count_characters.pack(side='left', padx=10, anchor='center')

utf_label = tk.Label(bottom_bar, text='UTF-8')
utf_label.pack(side='right', padx=10)

root.mainloop()
