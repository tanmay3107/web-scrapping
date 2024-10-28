import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox 
from tkinter import filedialog
import pandas as pd
from io import StringIO
import time
import validators 
from PIL import Image ,ImageTk


def scrape_text():
    url = entry.get()  
    if not validators.url(url):  
        messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        return
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        content_div = soup.find('main', class_='mw-body') or \
                      soup.find('div', class_='entry-content') or \
                      soup.find('div', id='content') or \
                      soup.find('article')
        if content_div:
            paragraphs = content_div.find_all('p')
            text_data = '\n'.join([p.get_text() for p in paragraphs])
            result_text.delete(1.0, END)  
            result_text.insert(END, text_data)  
        else:
            result_text.delete(1.0, END) 
            result_text.insert(END, "No text found on the webpage.")
    else:
        result_text.delete(1.0, END)  
        result_text.insert(END, f"Error: Unable to fetch URL ({response.status_code})")

def scrape_table():
    url = entry.get()  
    if not validators.url(url):  
        messagebox.showerror("Invalid URL", "Please enter a valid URL.")
        return
    response = requests.get(url)  
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table')
        if table:
            df = pd.read_html(url)
            result_text.delete(1.0, END)  
            result_text.insert(END, df)  
        else:
            result_text.delete(1.0, END)  
            result_text.insert(END, "No table found on the webpage.")
    else:
        result_text.delete(1.0, END)
        result_text.insert(END, f"Error: Unable to fetch URL ({response.status_code})")

def save_to_txt():
    filename = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text file', '.txt'), ('HTML file', '.html'), ('All files', '.*')])
    if filename:
        output = result_text.get(1.0, END)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(output)
        messagebox.showinfo("File Saved", f"Output saved to {filename}")




window = Tk()

entry = Entry(window, font=('Arial', 20), fg="#00FF00", bg="black")
entry.pack()

icon=ImageTk.PhotoImage(Image.open("koeniggsegg odin.png")) 
window.iconphoto(True,icon) 

button_frame = Frame(window)
button_frame.pack(side=BOTTOM, pady=10)

scrape_text_button = Button(button_frame, text="Scrape Text", command=scrape_text,fg='cyan',bg='black')
scrape_text_button.pack(side=LEFT, padx=5)

scrape_table_button = Button(button_frame, text="Scrape Table", command=scrape_table,fg='cyan',bg='black')
scrape_table_button.pack(side=LEFT, padx=5)

save_button = Button(button_frame, text="Save to .txt", command=save_to_txt,fg='cyan',bg='black')
save_button.pack(side=LEFT, padx=5)

result_text = Text(window, font=('Arial', 14), wrap=WORD, height=20, width=60,fg='cyan',bg='black')
result_text.pack()

window.mainloop()
