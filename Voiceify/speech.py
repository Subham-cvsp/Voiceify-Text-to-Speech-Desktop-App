#

from gtts import gTTS, lang                    # For text-to-speech and language support
from playsound import playsound                # For playing the generated MP3 audio
import requests                                # For fetching real-time quotes from an API
from tkinter import *                          # For creating the GUI (Tkinter toolkit)
from tkinter import messagebox, filedialog     # For pop-up dialogs and file saving
import random                                  # For selecting random content if needed

# -------------------------------- Functions --------------------------------

# Function: Convert text to speech and play it aloud
def text_to_speech():
    text = text_entry.get("1.0", "end-1c")      # Get text from the text box
    language = accent_entry.get()               # Get selected language code
    speed = slow_var.get()                      # True if 'slow voice' is checked
    
    if not text.strip() or not language.strip():
        messagebox.showerror("Error", "Please enter both text and language code.")
        return
    try:
        tts = gTTS(text=text, lang=language, slow=speed)
        tts.save("output.mp3")
        playsound("output.mp3")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function: Show a list of all supported language codes (e.g., en, hi)
def list_languages():
    languages = lang.tts_langs()
    all_langs = "\n".join([f"{k}: {v}" for k, v in languages.items()])
    messagebox.showinfo("Languages", all_langs)

# Function: Clear all input fields in the GUI
def clear_text():
    text_entry.delete("1.0", END)
    accent_entry.delete(0, END)

# Function: Save the generated speech as an MP3 file with custom filename
def save_as_mp3():
    text = text_entry.get("1.0", "end-1c")
    language = accent_entry.get()
    speed = slow_var.get()
    if not text.strip() or not language.strip():
        messagebox.showerror("Error", "Please enter both text and language code.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if filename:
        try:
            tts = gTTS(text=text, lang=language, slow=speed)
            tts.save(filename)
            messagebox.showinfo("Saved", f"Speech saved as: {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Function: Fetch a random motivational quote from ZenQuotes API and speak it
def speak_random_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        if response.status_code == 200:
            data = response.json()
            quote = data[0]['q'] + " - " + data[0]['a']
            tts = gTTS(text=quote, lang='en')
            tts.save("quote.mp3")
            playsound("quote.mp3")
        else:
            messagebox.showerror("Error", "Could not fetch quote. Try again.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch quote.\n{e}")

# -------------------------------- GUI Setup --------------------------------

# Create the main window
window = Tk()
window.title("🔊 Voiceify: Text to Speech")
window.geometry("600x500")
window.configure(bg="#1e1e1e")

# -------------------- Styling --------------------
# Define fonts and styles for widgets
FONT = ("Segoe UI", 10)
BTN_STYLE = {"bg": "#2e8b57", "fg": "white", "font": FONT, "activebackground": "#3cb371"}
LABEL_STYLE = {"bg": "#1e1e1e", "fg": "white", "font": ("Segoe UI", 10, "bold")}

# -------------------- Layout --------------------

Label(window, text="🔊 Voiceify: Text to Speech", font=("Segoe UI", 14, "bold"), bg="#1e1e1e", fg="#00ffcc").pack(pady=10)

frame = Frame(window, bg="#1e1e1e")
frame.pack(padx=20, pady=5, fill="both")

Label(frame, text="Enter Text:", **LABEL_STYLE).grid(row=0, column=0, sticky="w", pady=5)
text_entry = Text(frame, height=5, width=60, bg="#2d2d2d", fg="white", insertbackground="white")
text_entry.grid(row=1, column=0, columnspan=2, pady=5)

Label(frame, text="Language Code:", **LABEL_STYLE).grid(row=2, column=0, sticky="w", pady=5)
accent_entry = Entry(frame, width=20, bg="#2d2d2d", fg="white", insertbackground="white")
accent_entry.grid(row=2, column=1, pady=5, sticky="w")

slow_var = BooleanVar()
Checkbutton(frame, text="Slow Voice", variable=slow_var, bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").grid(row=3, column=0, sticky="w", pady=5)

# -------------------- Buttons --------------------

btn_frame = Frame(window, bg="#1e1e1e")
btn_frame.pack(pady=15)

Button(btn_frame, text="🎧 Speak", command=text_to_speech, width=15, **BTN_STYLE).grid(row=0, column=0, padx=8, pady=5)
Button(btn_frame, text="📁 Save as MP3", command=save_as_mp3, width=15, **BTN_STYLE).grid(row=0, column=1, padx=8, pady=5)
Button(btn_frame, text="🧠 Motivate Me", command=speak_random_quote, width=15, **BTN_STYLE).grid(row=1, column=0, padx=8, pady=5)
Button(btn_frame, text="🧹 Clear Text", command=clear_text, width=15, **BTN_STYLE).grid(row=1, column=1, padx=8, pady=5)
Button(window, text="🌐 List Languages", command=list_languages, **BTN_STYLE).pack(pady=10)

# -------------------- Start --------------------

window.mainloop()
