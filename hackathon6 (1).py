import io
import json
import os
import random
import time
import urllib.request
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Voice Output & Input Libraries
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr

# ============================================================
# NORTH EASTERN LANGUAGES & TTS SUPPORT
# ============================================================

LANGUAGES = {
    "English": "en",
    "Assamese (অসমীয়া)": "as",
    "Bengali (বাংলা)": "bn",
    "Nepali (নেपाली)": "ne",
    "Hindi (हिंदी)": "hi"
}

GRANDDAUGHTER_PHRASES = {
    "en": {
        "greeting": "Hello Grandpa/Grandma! It's your favorite granddaughter. I am here to talk with you!",
        "breakfast": "Did you have a yummy breakfast today? Tell me what you ate!",
        "lunch": "It's lunch time! Make sure to fill your tummy with warm food!",
        "dinner": "Dinner time! Don't skip your meal tonight, okay?",
        "medicine": "Time for your medicine! Take your pills now so you stay strong and healthy!",
        "jokes": [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a fake noodle? An impasta!",
            "Why did the bicycle fall over? Because it was two-tired!"
        ],
        "play_game": "Let's play a fun memory game together to keep your brain active!",
        "default": "I'm always right here listening to you. Tell me more about what you're thinking today!"
    },
    "as": {
        "greeting": "নমস্কাৰ! মই আপোনাৰ মৰমৰ নাতি। মই আপোনাৰ লগত কথা পাতিবলৈ আহিছোঁ!",
        "breakfast": "আপুনি আজি ৰাতিপুৱাৰ আহাৰ খালেনে?",
        "lunch": "দুপৰীয়াৰ আহাৰৰ সময় হ'ল! দেৰি নকৰিব দেই।",
        "dinner": "ৰাতিৰ আহাৰৰ সময় হ'ল, ভালদৰে খাই লওক।",
        "medicine": "দৱাই খোৱাৰ সময় হ'ল! এতিয়াই ঔষধটো খাই লওক।",
        "jokes": [
            "প্ৰশ্ন: মানুহে কিয় চকলেট খায়? উত্তৰ: কাৰণ ই খুব মিঠা!",
            "হাঁহিবলৈ কথা এটা মনত পৰিল, আপুনি সদায় হাঁহি থাকক!"
        ],
        "play_game": "আহক আমি একেলগে এটা ধুনীয়া খেল খেলোঁ!",
        "default": "মই আপোনাৰ কথা শুনি আছোঁ। মোক আৰু কিছু কথা কওক।"
    },
    "bn": {
        "greeting": "নমস্কার! আমি তোমার আদরের নাতনি। তোমার সাথে গল্প করতে এসেছি!",
        "breakfast": "তুমি কি সকালের খাবার খেয়েছ?",
        "lunch": "দুপুরের খাওয়ার সময় হয়ে গেছে! পেট ভরে খেয়ে নাও।",
        "dinner": "রাতের খাবারের সময় হয়েছে, ভালো করে খেয়ে নাও কিন্তু।",
        "medicine": "ওষুধ খাওয়ার সময় হয়ে গেছে! লক্ষ্মী সোনার মতো ওষুধটা খেয়ে নাও তো!",
        "jokes": [
            "শিক্ষক: বলো তো পৃথিবীর সবচেয়ে পুরোনো প্রাণী কোনটা? ছাত্র: জেব্রা! কারণ সেটা এখনো সাদাকালো!"
        ],
        "play_game": "চলো আমরা একটা সুন্দর খেলা খেলি!",
        "default": "আমি মন দিয়ে তোমার কথা শুনছি। বলো, আজ সারাদিন কী করলে?"
    },
    "ne": {
        "greeting": "नमस्ते! म तपाइँको प्यारा नातिनी हुँ। तपाइँसँग कुरा गर्न आएको छु!",
        "breakfast": "के तपाइँले बिहानको खाना खानुभयो?",
        "lunch": "दिउँसोको खाना खाने समय भयो! मीठो मानि खानुहोस् है।",
        "dinner": "रातिको खाना खाने समय भयो, समयमा खानुहोस्।",
        "medicine": "औषधि खाने समय भयो! छिटो औषधि खानुहोस्।",
        "jokes": [
            "सधैं मुस्कुराउनुहोस्, मुस्कानले उमेर बढाउँछ!"
        ],
        "play_game": "आउनुहोस् एउटा रमाइलो खेल खेलौं!",
        "default": "म तपाइँको कुरा सुन्दैछु। मलाई अझै धेरै कुरा भन्नुहोस्।"
    },
    "hi": {
        "greeting": "नमस्ते! मैं आपकी पोती हूँ। आपसे ढेर सारी बातें करने आई हूँ!",
        "breakfast": "क्या आपने सुबह का नाश्ता कर लिया?",
        "lunch": "दोपहर के खाने का समय हो गया है! जल्दी से खाना खा लीजिए।",
        "dinner": "रात के खाने का समय हो गया है, खाना मिस मत करना!",
        "medicine": "दवाई लेने का समय हो गया है! सेहत के लिए दवाई जल्दी खा लो।",
        "jokes": [
            "टीचर: बताओ सबसे बड़ा आलसी कौन है? छात्र: जो प्यास लगने पर भी पानी न पिये!"
        ],
        "play_game": "चलिए साथ में एक मज़ेदार गेम खेलते हैं!",
        "default": "मैं आपकी पूरी बात सुन रही हूँ। मुझे और बताइए!"
    }
}


def speak_text(text, lang_code="en"):
    """Runs TTS audio output in a separate thread to keep the GUI responsive."""
    def _speak():
        temp_file = f"temp_speech_{int(time.time())}.mp3"
        try:
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(temp_file)
            playsound(temp_file)
        except Exception as e:
            print(f"Text-to-Speech Error: {e}")
        finally:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    threading.Thread(target=_speak, daemon=True).start()


# ============================================================
# MAIN APPLICATION CONTROLLER WITH VOICE RECOGNITION AI
# ============================================================

class UnifiedMemoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Granddaughter Voice AI & Memory Suite")
        self.geometry("1100x800")
        self.minsize(950, 700)
        self.configure(bg="#1e1e2e")

        self.current_lang = "en"
        self.recognizer = sr.Recognizer()

        self.container = tk.Frame(self, bg="#1e1e2e")
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_container()
        self.title("Memory Suite - Main Menu & AI Granddaughter Voice Companion")

        # Top Control Bar for Voice Language Selection
        top_bar = tk.Frame(self.container, bg="#11111b", height=50)
        top_bar.pack(side="top", fill="x")

        tk.Label(
            top_bar, text="🗣️ Select Granddaughter Language: ",
            font=("Helvetica", 11, "bold"), fg="#cdd6f4", bg="#11111b"
        ).pack(side="left", padx=15, pady=10)

        self.lang_combobox = ttk.Combobox(
            top_bar, values=list(LANGUAGES.keys()), state="readonly", font=("Helvetica", 10)
        )
        self.lang_combobox.set("English")
        self.lang_combobox.pack(side="left", pady=10)
        self.lang_combobox.bind("<<ComboboxSelected>>", self.on_language_change)

        header = tk.Frame(self.container, bg="#1e1e2e")
        header.pack(pady=(15, 5))

        tk.Label(
            header, text="👵 Voice Interactive Companion & Brain Suite 🧠",
            font=("Helvetica", 20, "bold"), fg="#89b4fa", bg="#1e1e2e"
        ).pack()

        main_split = tk.Frame(self.container, bg="#1e1e2e")
        main_split.pack(fill="both", expand=True, padx=20, pady=5)

        # Left Column: AI Chatbot Granddaughter Interface with Voice Input
        chatbot_frame = tk.Frame(main_split, bg="#181825", highlightbackground="#313244", highlightthickness=2)
        chatbot_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.build_chatbot_ui(chatbot_frame)

        # Right Column: Memory Games & Setup Modules
        menu_frame = tk.Frame(main_split, bg="#1e1e2e")
        menu_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.create_menu_card(
            menu_frame, title="🌿 1. Memory Garden Setup",
            desc="Configure patient and family profiles.",
            btn_text="Launch Setup", command=self.launch_memory_garden, row=0, col=0
        )
        self.create_menu_card(
            menu_frame, title="🖼️ 2. Photo Grid Matching",
            desc="Match visual pairs through levels.",
            btn_text="Play Grid", command=self.launch_photo_grid, row=0, col=1
        )
        self.create_menu_card(
            menu_frame, title="⚡ 3. Color Memory Rush",
            desc="Color sequence recall exercise.",
            btn_text="Play Color Rush", command=self.launch_color_rush, row=1, col=0
        )
        self.create_menu_card(
            menu_frame, title="📖 4. Story & Profile Quiz",
            desc="Customized memory recall quiz.",
            btn_text="Play Quiz", command=self.launch_story_quiz, row=1, col=1
        )

    def on_language_change(self, event):
        selected = self.lang_combobox.get()
        self.current_lang = LANGUAGES.get(selected, "en")
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        greeting = phrases["greeting"]
        self.append_chat("Granddaughter", greeting)
        speak_text(greeting, self.current_lang)

    def build_chatbot_ui(self, parent):
        tk.Label(
            parent, text="👧 Voice AI Granddaughter",
            font=("Helvetica", 14, "bold"), fg="#a6e3a1", bg="#181825"
        ).pack(pady=5)

        self.chat_display = tk.Text(
            parent, bg="#1e1e2e", fg="#cdd6f4", font=("Helvetica", 10),
            wrap="word", state="disabled", height=12
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=5)

        # Quick Action Buttons
        btn_grid = tk.Frame(parent, bg="#181825")
        btn_grid.pack(fill="x", padx=10, pady=2)

        tk.Button(btn_grid, text="🍚 Meals", bg="#f9e2af", fg="#11111b", font=("Helvetica", 9, "bold"),
                  command=self.bot_ask_meal).grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        tk.Button(btn_grid, text="💊 Medicine", bg="#f38ba8", fg="#11111b", font=("Helvetica", 9, "bold"),
                  command=self.bot_remind_medicine).grid(row=0, column=1, padx=2, pady=2, sticky="ew")
        tk.Button(btn_grid, text="😂 Joke", bg="#89b4fa", fg="#11111b", font=("Helvetica", 9, "bold"),
                  command=self.bot_tell_joke).grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        tk.Button(btn_grid, text="🎮 Games", bg="#a6e3a1", fg="#11111b", font=("Helvetica", 9, "bold"),
                  command=self.bot_suggest_game).grid(row=1, column=1, padx=2, pady=2, sticky="ew")

        btn_grid.grid_columnconfigure(0, weight=1)
        btn_grid.grid_columnconfigure(1, weight=1)

        # Status Label for Voice Microphone Input
        self.status_mic_label = tk.Label(parent, text="Press '🎤 Speak' to talk to your granddaughter", font=("Helvetica", 9, "italic"), fg="#a6adc8", bg="#181825")
        self.status_mic_label.pack(pady=(4, 0))

        # Input Frame: Microphone Button, Text Box, and Send Button
        input_frame = tk.Frame(parent, bg="#181825")
        input_frame.pack(fill="x", padx=10, pady=8)

        # Dedicated Patient Voice Microphone Button
        self.mic_button = tk.Button(
            input_frame, text="🎤 Speak", font=("Helvetica", 10, "bold"), bg="#a6e3a1", fg="#11111b",
            activebackground="#94e2d5", command=self.listen_to_patient_voice
        )
        self.mic_button.pack(side="left", padx=(0, 5))

        self.user_entry = tk.Entry(input_frame, font=("Helvetica", 11), bg="#313244", fg="#cdd6f4", insertbackground="white")
        self.user_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.user_entry.bind("<Return>", lambda event: self.send_chat_message())

        tk.Button(input_frame, text="Send", font=("Helvetica", 10, "bold"), bg="#89b4fa", fg="#11111b",
                  command=self.send_chat_message).pack(side="right")

    def append_chat(self, sender, text):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, f"{sender}: {text}\n\n")
        self.chat_display.config(state="disabled")
        self.chat_display.see(tk.END)

    def listen_to_patient_voice(self):
        """Captures voice input directly from the user's microphone."""
        def _listen():
            self.status_mic_label.config(text="🎙️ Listening... Speak into your microphone now.", fg="#a6e3a1")
            self.mic_button.config(state="disabled")
            
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=6, phrase_time_limit=10)
                    
                    self.status_mic_label.config(text="⚡ Processing speech...", fg="#f9e2af")
                    spoken_text = self.recognizer.recognize_google(audio, language=self.current_lang)
                    
                    self.user_entry.delete(0, tk.END)
                    self.user_entry.insert(0, spoken_text)
                    self.send_chat_message()

            except sr.WaitTimeoutError:
                self.status_mic_label.config(text="⚠️ Didn't hear anything. Try pressing 'Speak' again.", fg="#f38ba8")
            except sr.UnknownValueError:
                self.status_mic_label.config(text="⚠️ Could not understand audio. Try speaking clearly.", fg="#f38ba8")
            except Exception as error:
                self.status_mic_label.config(text=f"⚠️ Mic Error: {error}", fg="#f38ba8")
            finally:
                self.mic_button.config(state="normal")
                if "Processing" in self.status_mic_label.cget("text") or "Listening" in self.status_mic_label.cget("text"):
                    self.status_mic_label.config(text="Press '🎤 Speak' to talk to your granddaughter", fg="#a6adc8")

        threading.Thread(target=_listen, daemon=True).start()

    def process_ai_response(self, user_msg):
        """Generates conversational response using keyword mapping and intent classification."""
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        msg_lower = user_msg.lower()

        if any(w in msg_lower for w in ["hi", "hello", "hey", "namaste", "good morning", "good evening"]):
            return phrases["greeting"]
        elif any(w in msg_lower for w in ["food", "ate", "eat", "breakfast", "lunch", "dinner", "rice", "roti"]):
            return phrases["breakfast"]
        elif any(w in msg_lower for w in ["medicine", "pill", "tablet", "doctor", "health", "sick"]):
            return phrases["medicine"]
        elif any(w in msg_lower for w in ["joke", "funny", "laugh", "story"]):
            return random.choice(phrases["jokes"])
        elif any(w in msg_lower for w in ["game", "play", "bored", "quiz", "match"]):
            return phrases["play_game"]
        elif any(w in msg_lower for w in ["who are you", "your name"]):
            return "I am your loving granddaughter! I am here to chat, play games, and remind you of your daily routine."
        elif any(w in msg_lower for w in ["sad", "lonely", "miss", "forget", "help"]):
            return "Don't worry at all. I am right here with you! You are safe and doing great today."
        else:
            return phrases.get("default", phrases["greeting"])

    def send_chat_message(self):
        msg = self.user_entry.get().strip()
        if not msg:
            return
        self.append_chat("You", msg)
        self.user_entry.delete(0, tk.END)

        reply = self.process_ai_response(msg)
        self.append_chat("Granddaughter", reply)
        speak_text(reply, self.current_lang)

    def bot_ask_meal(self):
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        hour = time.localtime().tm_hour
        if hour < 11:
            msg = phrases["breakfast"]
        elif hour < 16:
            msg = phrases["lunch"]
        else:
            msg = phrases["dinner"]
        self.append_chat("Granddaughter", msg)
        speak_text(msg, self.current_lang)

    def bot_remind_medicine(self):
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        msg = phrases["medicine"]
        self.append_chat("Granddaughter", msg)
        speak_text(msg, self.current_lang)

    def bot_tell_joke(self):
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        joke = random.choice(phrases["jokes"])
        self.append_chat("Granddaughter", joke)
        speak_text(joke, self.current_lang)

    def bot_suggest_game(self):
        phrases = GRANDDAUGHTER_PHRASES.get(self.current_lang, GRANDDAUGHTER_PHRASES["en"])
        msg = phrases["play_game"]
        self.append_chat("Granddaughter", msg)
        speak_text(msg, self.current_lang)

    def create_menu_card(self, parent, title, desc, btn_text, command, row, col):
        card = tk.Frame(
            parent, bg="#181825", highlightbackground="#313244",
            highlightthickness=1, padx=10, pady=10
        )
        card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

        tk.Label(card, text=title, font=("Helvetica", 11, "bold"), fg="#cdd6f4", bg="#181825").pack(anchor="w")
        tk.Label(card, text=desc, font=("Helvetica", 9), fg="#a6adc8", bg="#181825", wraplength=180, justify="left").pack(anchor="w", pady=(2, 8))
        tk.Button(card, text=btn_text, font=("Helvetica", 9, "bold"), bg="#89b4fa", fg="#11111b", relief="flat", padx=10, pady=4, command=command, cursor="hand2").pack(anchor="e")

    def create_top_nav(self, parent_frame):
        nav_frame = tk.Frame(parent_frame, bg="#11111b", height=40)
        nav_frame.pack(side="top", fill="x")

        tk.Button(
            nav_frame, text="🏠 Back to Main Menu & Voice AI Chatbot",
            font=("Helvetica", 10, "bold"), fg="#cdd6f4", bg="#313244",
            activebackground="#45475a", relief="flat", padx=10, pady=4,
            command=self.show_main_menu, cursor="hand2"
        ).pack(side="left", padx=10, pady=5)

    def launch_memory_garden(self):
        self.clear_container()
        game_frame = tk.Frame(self.container, bg="#F4F7FB")
        game_frame.pack(fill="both", expand=True)
        self.create_top_nav(game_frame)
        sub_container = tk.Frame(game_frame, bg="#F4F7FB")
        sub_container.pack(fill="both", expand=True)
        MemoryGardenView(sub_container)

    def launch_photo_grid(self):
        self.clear_container()
        game_frame = tk.Frame(self.container, bg="#2c3e50")
        game_frame.pack(fill="both", expand=True)
        self.create_top_nav(game_frame)
        sub_container = tk.Frame(game_frame, bg="#2c3e50")
        sub_container.pack(fill="both", expand=True)
        RandomizedProgressiveGameView(sub_container)

    def launch_color_rush(self):
        self.clear_container()
        game_frame = tk.Frame(self.container, bg="#1e1e2e")
        game_frame.pack(fill="both", expand=True)
        self.create_top_nav(game_frame)
        sub_container = tk.Frame(game_frame, bg="#1e1e2e")
        sub_container.pack(fill="both", expand=True)
        ColorMemoryRushView(sub_container)

    def launch_story_quiz(self):
        self.clear_container()
        game_frame = tk.Frame(self.container, bg="#ecf0f1")
        game_frame.pack(fill="both", expand=True)
        self.create_top_nav(game_frame)
        sub_container = tk.Frame(game_frame, bg="#ecf0f1")
        sub_container.pack(fill="both", expand=True)
        MemoryGameStoryQuizView(sub_container)


# ============================================================
# MODULE 1: MEMORY GARDEN GUARDIAN SETUP
# ============================================================

BG = "#F4F7FB"
CARD = "#FFFFFF"
PRIMARY = "#5B6CFF"
PRIMARY_DARK = "#4352D8"
TEXT = "#24304A"
MUTED = "#6B7280"
SOFT = "#E9EDFF"

class MemoryGardenView:
    def __init__(self, master):
        self.master = master
        self.page_number = 0

        self.profile = {
            "guardian_name": "", "relationship": "", "contact": "",
            "patient_name": "", "patient_gender": "", "patient_age": "",
            "patient_difficulty": "", "patient_school": "", "patient_village": "",
            "relatives": [], "place_photos": [], "personal_stories": ""
        }
        self.pages = []
        self.show_welcome()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def header(self, title, subtitle):
        tk.Label(self.master, text="🌿 Memory Garden", font=("Arial", 20, "bold"), fg=PRIMARY, bg=BG).pack(anchor="w", padx=50, pady=(20, 5))
        tk.Label(self.master, text=title, font=("Arial", 24, "bold"), fg=TEXT, bg=BG).pack(anchor="w", padx=50)
        tk.Label(self.master, text=subtitle, font=("Arial", 11), fg=MUTED, bg=BG).pack(anchor="w", padx=50, pady=(5, 10))

    def create_card(self):
        card = tk.Frame(self.master, bg=CARD, highlightbackground="#DDE2EA", highlightthickness=1)
        card.pack(fill="both", expand=True, padx=50, pady=10)
        return card

    def field_label(self, parent, text, required=False):
        label_text = text + ("  *" if required else "")
        tk.Label(parent, text=label_text, font=("Arial", 11, "bold"), fg=TEXT, bg=CARD).pack(anchor="w", pady=(10, 2))

    def entry(self, parent, value=""):
        variable = tk.StringVar(value=value)
        widget = tk.Entry(parent, textvariable=variable, font=("Arial", 11), relief="solid", bd=1)
        widget.pack(fill="x", ipady=6)
        return variable

    def navigation(self, parent, back=True):
        bottom = tk.Frame(parent, bg=CARD)
        bottom.pack(side="bottom", fill="x", padx=25, pady=15)

        if back:
            tk.Button(bottom, text="← Back", font=("Arial", 11), command=self.previous_page).pack(side="left")

        tk.Button(bottom, text="Continue →", font=("Arial", 11, "bold"), fg="white", bg=PRIMARY, activebackground=PRIMARY_DARK, relief="flat", padx=20, pady=8, command=self.next_page).pack(side="right")

    def start_setup(self):
        self.pages = [self.guardian_page, self.patient_page, self.details_page, self.relatives_page, self.places_page, self.review_page]
        self.page_number = 0
        self.show_page()

    def show_page(self):
        self.clear_screen()
        self.pages[self.page_number]()

    def show_welcome(self):
        self.clear_screen()
        container = tk.Frame(self.master, bg=BG)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="🌿", font=("Arial", 50), bg=BG).pack(pady=(60, 5))
        tk.Label(container, text="Memory Garden", font=("Arial", 32, "bold"), fg=PRIMARY, bg=BG).pack()
        tk.Label(container, text="A personalized memory-support game", font=("Arial", 14), fg=MUTED, bg=BG).pack(pady=5)
        tk.Label(container, text="Create a gentle, familiar world using\npeople, places and memories that matter.", font=("Arial", 12), fg=TEXT, bg=BG, justify="center").pack(pady=15)
        tk.Button(container, text="CLICK TO ENTER  →", font=("Arial", 13, "bold"), fg="white", bg=PRIMARY, activebackground=PRIMARY_DARK, relief="flat", padx=25, pady=10, cursor="hand2", command=self.start_setup).pack(pady=20)

    def guardian_page(self):
        self.header("Guardian / User Details", "Required information about the person setting up the game.")
        card = self.create_card()
        self.field_label(card, "Enter Your Name", required=True)
        self.guardian_name = self.entry(card, self.profile["guardian_name"])

        self.field_label(card, "Your Relationship to Patient", required=True)
        self.relationship = ttk.Combobox(card, values=["Parent", "Sibling", "Grandparent", "Relative", "Caregiver", "Other"], state="readonly", font=("Arial", 11))
        self.relationship.pack(fill="x", ipady=5)
        self.relationship.set(self.profile["relationship"])

        self.field_label(card, "Your Contact Information", required=True)
        self.contact = self.entry(card, self.profile["contact"])
        self.navigation(card, back=False)

    def patient_page(self):
        self.header("Patient Details", "Required basic information about the patient.")
        card = self.create_card()
        self.field_label(card, "Enter Name of Patient", required=True)
        self.patient_name = self.entry(card, self.profile["patient_name"])

        self.field_label(card, "Enter Gender of Patient", required=True)
        self.patient_gender = tk.StringVar(value=self.profile["patient_gender"])
        gender_frame = tk.Frame(card, bg=CARD)
        gender_frame.pack(anchor="w", pady=5)

        for value in ["Female", "Male", "Other", "Prefer not to say"]:
            tk.Radiobutton(gender_frame, text=value, variable=self.patient_gender, value=value, font=("Arial", 11), bg=CARD, selectcolor=SOFT).pack(side="left", padx=10)

        self.field_label(card, "Enter Age of Patient", required=True)
        self.patient_age = self.entry(card, self.profile["patient_age"])
        self.navigation(card)

    def details_page(self):
        self.header("Additional Details of Patient", "Information used to personalize the patient's game.")
        card = self.create_card()
        self.field_label(card, "Memory Condition of Patient", required=True)
        self.patient_difficulty = tk.StringVar(value=self.profile["patient_difficulty"])
        difficulty_frame = tk.Frame(card, bg=CARD)
        difficulty_frame.pack(fill="x", pady=5)

        options = [("Better", "Needs less assistance"), ("Intermediate", "Needs some assistance"), ("Difficult", "Needs frequent assistance")]
        for title, description in options:
            box = tk.Frame(difficulty_frame, bg="#F4F6FA", highlightbackground="#DDE2EA", highlightthickness=1)
            box.pack(side="left", fill="both", expand=True, padx=5)
            tk.Radiobutton(box, text=title, variable=self.patient_difficulty, value=title, font=("Arial", 11, "bold"), bg="#F4F6FA", selectcolor=SOFT).pack(pady=(8, 2))
            tk.Label(box, text=description, font=("Arial", 9), fg=MUTED, bg="#F4F6FA", wraplength=170).pack(pady=(0, 8))

        self.field_label(card, "School / Workplace of Patient", required=True)
        self.patient_school = self.entry(card, self.profile["patient_school"])
        self.field_label(card, "Village / Town of Patient", required=True)
        self.patient_village = self.entry(card, self.profile["patient_village"])
        self.navigation(card)

    def relatives_page(self):
        self.header("Relatives of Patient", "Add as many familiar people as you want.")
        card = self.create_card()
        left = tk.Frame(card, bg=CARD)
        left.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        self.field_label(left, "Name of Relative", required=True)
        self.relative_name = self.entry(left)
        self.field_label(left, "Relationship to Patient", required=True)
        self.relative_relation = ttk.Combobox(left, values=["Father", "Mother", "Son", "Daughter", "Brother", "Sister", "Grandfather", "Grandmother", "Uncle", "Aunt", "Cousin", "Friend", "Other"], state="readonly", font=("Arial", 11))
        self.relative_relation.pack(fill="x", ipady=5)

        self.field_label(left, "Personal Story / Memory")
        self.story = tk.Text(left, height=4, font=("Arial", 11), relief="solid", bd=1, wrap="word")
        self.story.pack(fill="both", expand=True)

        right = tk.Frame(card, bg="#F7F8FC", width=320)
        right.pack(side="right", fill="y", padx=20, pady=10)
        right.pack_propagate(False)

        tk.Label(right, text="📸 Photo of Relative", font=("Arial", 13, "bold"), fg=TEXT, bg="#F7F8FC").pack(pady=(10, 5))
        self.relative_photo_preview = tk.Label(right, text="No photo selected", font=("Arial", 9), fg=MUTED, bg="#E9ECF3", width=25, height=6)
        self.relative_photo_preview.pack(pady=5)
        self.relative_photo_path = None
        self.relative_photo_image = None

        tk.Button(right, text="＋ Choose Photo", font=("Arial", 10, "bold"), fg="white", bg=PRIMARY, activebackground=PRIMARY_DARK, relief="flat", padx=10, pady=6, command=self.choose_relative_photo).pack(pady=5)
        self.navigation(card)

    def choose_relative_photo(self):
        filename = filedialog.askopenfilename(title="Choose Photo of Relative", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")])
        if not filename: return
        self.relative_photo_path = filename
        try:
            image = Image.open(filename)
            image.thumbnail((200, 150))
            self.relative_photo_image = ImageTk.PhotoImage(image)
            self.relative_photo_preview.config(image=self.relative_photo_image, text="")
        except Exception as error:
            messagebox.showerror("Photo Error", f"Could not open the selected image.\n\n{error}")

    def places_page(self):
        self.header("Familiar Places", "Add multiple photos of places that are familiar to the patient.")
        card = self.create_card()
        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x", padx=20, pady=10)
        tk.Label(top, text="📍 Place Photos", font=("Arial", 14, "bold"), fg=TEXT, bg=CARD).pack(anchor="w")

        button_row = tk.Frame(card, bg=CARD)
        button_row.pack(fill="x", padx=20)
        tk.Button(button_row, text="＋ Add Multiple Place Photos", font=("Arial", 10, "bold"), fg="white", bg=PRIMARY, activebackground=PRIMARY_DARK, relief="flat", padx=15, pady=8, command=self.add_place_photos).pack(side="left")

        self.place_list = tk.Listbox(card, font=("Arial", 10), height=8, relief="solid", bd=1)
        self.place_list.pack(fill="both", expand=True, padx=20, pady=10)
        self.refresh_place_list()
        self.navigation(card)

    def add_place_photos(self):
        filenames = filedialog.askopenfilenames(title="Choose Photos", filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp"), ("All Files", "*.*")])
        if not filenames: return
        for filename in filenames:
            if filename not in self.profile["place_photos"]:
                self.profile["place_photos"].append(filename)
        self.refresh_place_list()

    def refresh_place_list(self):
        if hasattr(self, "place_list"):
            self.place_list.delete(0, tk.END)
            for i, path in enumerate(self.profile["place_photos"], start=1):
                self.place_list.insert(tk.END, f"{i}. {os.path.basename(path)}")

    def save_current_page(self):
        if self.page_number == 0:
            self.profile["guardian_name"] = self.guardian_name.get().strip()
            self.profile["relationship"] = self.relationship.get().strip()
            self.profile["contact"] = self.contact.get().strip()
        elif self.page_number == 1:
            self.profile["patient_name"] = self.patient_name.get().strip()
            self.profile["patient_gender"] = self.patient_gender.get().strip()
            self.profile["patient_age"] = self.patient_age.get().strip()
        elif self.page_number == 2:
            self.profile["patient_difficulty"] = self.patient_difficulty.get().strip()
            self.profile["patient_school"] = self.patient_school.get().strip()
            self.profile["patient_village"] = self.patient_village.get().strip()
        elif self.page_number == 3:
            name = self.relative_name.get().strip()
            relation = self.relative_relation.get().strip()
            story = self.story.get("1.0", "end").strip()
            if name:
                self.profile["relatives"].append({"name": name, "relationship": relation, "story": story, "photo": self.relative_photo_path})

    def validate_page(self):
        if self.page_number == 0:
            if not self.guardian_name.get().strip() or not self.relationship.get().strip() or not self.contact.get().strip():
                messagebox.showwarning("Required", "Please complete all fields.")
                return False
        elif self.page_number == 1:
            if not self.patient_name.get().strip() or not self.patient_gender.get().strip() or not self.patient_age.get().strip():
                messagebox.showwarning("Required", "Please complete all fields.")
                return False
        elif self.page_number == 2:
            if not self.patient_difficulty.get().strip() or not self.patient_school.get().strip() or not self.patient_village.get().strip():
                messagebox.showwarning("Required", "Please complete all fields.")
                return False
        return True

    def next_page(self):
        if not self.validate_page(): return
        self.save_current_page()
        if self.page_number < len(self.pages) - 1:
            self.page_number += 1
            self.show_page()
        else:
            self.save_profile()

    def previous_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.show_page()

    def review_page(self):
        self.header("Review Memory Garden", "Check the profile before creating the personalized game.")
        card = self.create_card()
        summary = (
            f"Guardian / User: {self.profile['guardian_name']}\n"
            f"Relationship: {self.profile['relationship']}\n"
            f"Patient Name: {self.profile['patient_name']}\n"
            f"Gender of Patient: {self.profile['patient_gender']}\n"
            f"Age of Patient: {self.profile['patient_age']}\n"
            f"Memory Condition: {self.profile['patient_difficulty']}\n"
            f"Relatives Added: {len(self.profile['relatives'])}\n"
            f"Familiar Place Photos: {len(self.profile['place_photos'])}"
        )
        tk.Label(card, text=summary, font=("Arial", 11), fg=TEXT, bg=CARD, justify="left").pack(anchor="w", padx=25, pady=20)
        bottom = tk.Frame(card, bg=CARD)
        bottom.pack(side="bottom", fill="x", padx=25, pady=15)
        tk.Button(bottom, text="← Back", command=self.previous_page).pack(side="left")
        tk.Button(bottom, text="✓ SAVE PROFILE", font=("Arial", 11, "bold"), fg="white", bg=PRIMARY, activebackground=PRIMARY_DARK, relief="flat", padx=20, pady=10, command=self.save_profile).pack(side="right")

    def save_profile(self):
        filename = filedialog.asksaveasfilename(title="Save Profile", defaultextension=".json", filetypes=[("JSON Profile", "*.json")])
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(self.profile, file, indent=4, ensure_ascii=False)
                messagebox.showinfo("Profile Created!", "The profile was created successfully!")
            except Exception as error:
                messagebox.showerror("Save Error", f"Could not save profile: {error}")


# ============================================================
# MODULE 2: AUTO-PROGRESSION PHOTO MEMORY GAME
# ============================================================

PHOTO_URLS = [
    "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1564349683136-77e08dba1ef9?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1550958727-4473a65da0a8?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1540573133985-780688d172e2?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1534188753412-3e26d0d618d6?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1551085254-e96b210df58a?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1574063413132-355dbfd83e0c?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?w=150&h=150&fit=crop",
    "https://images.unsplash.com/photo-1507666405768-8274b023b380?w=150&h=150&fit=crop",
]

class RandomizedProgressiveGameView:
    def __init__(self, master):
        self.master = master
        self.levels = [
            ("Easy (2x3 Grid)", 2, 3),
            ("Medium (3x4 Grid)", 3, 4),
            ("Hard (4x4 Grid)", 4, 4),
        ]
        self.current_level_idx = 0
        self.images_cache = {}
        
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.matches_found = 0
        self.can_click = True
        self.card_buttons = []
        self.cards_data = []

        self.preload_images()
        self.create_header()

        self.grid_container = tk.Frame(self.master, bg="#34495e", padx=15, pady=15)
        self.grid_container.pack(pady=10)

        self.start_level()

    def preload_images(self):
        loading = tk.Toplevel(self.master)
        loading.title("Loading Photos...")
        tk.Label(loading, text="Downloading photo library, please wait...", padx=25, pady=25).pack()
        loading.update()

        for url in PHOTO_URLS:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                raw_data = urllib.request.urlopen(req).read()
                img = Image.open(io.BytesIO(raw_data)).resize((75, 75), Image.Resampling.LANCZOS)
                self.images_cache[url] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error downloading {url}: {e}")

        loading.destroy()

    def create_header(self):
        header_frame = tk.Frame(self.master, bg="#2c3e50", pady=10)
        header_frame.pack(fill="x")

        self.level_label = tk.Label(header_frame, text="", font=("Helvetica", 13, "bold"), fg="#f1c40f", bg="#2c3e50")
        self.level_label.pack(side="left", padx=20)

        self.score_label = tk.Label(header_frame, text="Moves: 0", font=("Helvetica", 12, "bold"), fg="white", bg="#2c3e50")
        self.score_label.pack(side="right", padx=20)

    def start_level(self):
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.card_buttons.clear()
        self.first_card = None
        self.second_card = None
        self.moves = 0
        self.matches_found = 0
        self.can_click = True

        level_name, rows, cols = self.levels[self.current_level_idx]
        self.level_label.config(text=f"Level: {level_name}")
        self.score_label.config(text="Moves: 0")

        total_pairs = (rows * cols) // 2
        available_urls = list(self.images_cache.keys())
        selected_urls = random.sample(available_urls, min(total_pairs, len(available_urls)))

        self.cards_data = selected_urls * 2
        random.shuffle(self.cards_data)

        for i in range(len(self.cards_data)):
            btn = tk.Button(
                self.grid_container, text="?", font=("Helvetica", 14, "bold"),
                width=5, height=2, bg="#3498db", fg="white", relief="raised", bd=3,
                command=lambda idx=i: self.on_card_click(idx)
            )
            btn.grid(row=i // cols, column=i % cols, padx=4, pady=4)
            self.card_buttons.append(btn)

    def on_card_click(self, idx):
        if not self.can_click or self.card_buttons[idx]["state"] == "disabled" or self.first_card == idx:
            return

        url = self.cards_data[idx]
        self.card_buttons[idx].config(image=self.images_cache[url], width=75, height=75, bg="#ffffff")

        if self.first_card is None:
            self.first_card = idx
        else:
            self.second_card = idx
            self.moves += 1
            self.score_label.config(text=f"Moves: {self.moves}")
            self.can_click = False
            self.master.after(600, self.check_match)

    def check_match(self):
        idx1, idx2 = self.first_card, self.second_card
        _, rows, cols = self.levels[self.current_level_idx]
        total_pairs = (rows * cols) // 2

        if self.cards_data[idx1] == self.cards_data[idx2]:
            self.card_buttons[idx1].config(bg="#2ecc71", state="disabled")
            self.card_buttons[idx2].config(bg="#2ecc71", state="disabled")
            self.matches_found += 1

            if self.matches_found == total_pairs:
                if self.current_level_idx < len(self.levels) - 1:
                    messagebox.showinfo("Level Cleared!", "Great job! Advancing to the next level...")
                    self.current_level_idx += 1
                    self.start_level()
                else:
                    messagebox.showinfo("Victory!", "Congratulations! You completed all levels!")
                    self.current_level_idx = 0
                    self.start_level()
        else:
            for idx in (idx1, idx2):
                self.card_buttons[idx].config(image="", text="?", width=5, height=2, bg="#3498db", fg="white")

        self.first_card = None
        self.second_card = None
        self.can_click = True


# ============================================================
# MODULE 3: COLOR MEMORY RUSH GAME
# ============================================================

DATA_FILE = "game_history.json"

class ColorMemoryRushView:
    def __init__(self, master):
        self.master = master
        self.colors = {
            "RED": {"normal": "#f38ba8", "flash": "#ff0055"},
            "GREEN": {"normal": "#a6e3a1", "flash": "#00ff66"},
            "BLUE": {"normal": "#89b4fa", "flash": "#0066ff"},
            "YELLOW": {"normal": "#f9e2af", "flash": "#ffcc00"},
        }
        self.round_number = 0
        self.sequence = []
        self.player_sequence = []
        self.score = 0
        self.is_playing = False
        self.start_time = None
        self.timer_running = False

        self.history = self.load_history()
        self.setup_ui()

    def load_history(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"last_time": None, "best_time": None}

    def save_history(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.history, f, indent=4)

    def setup_ui(self):
        self.status_label = tk.Label(self.master, text="Reach 100 points to win!", font=("Helvetica", 15, "bold"), bg="#1e1e2e", fg="#cdd6f4")
        self.status_label.pack(pady=10)

        stats_frame = tk.Frame(self.master, bg="#1e1e2e")
        stats_frame.pack(pady=2)

        self.score_label = tk.Label(stats_frame, text="Score: 0 / 100", font=("Helvetica", 11), bg="#1e1e2e", fg="#a6adc8")
        self.score_label.pack(side="left", padx=15)

        self.timer_label = tk.Label(stats_frame, text="Time: 0.0s", font=("Helvetica", 11, "bold"), bg="#1e1e2e", fg="#fab387")
        self.timer_label.pack(side="right", padx=15)

        record_frame = tk.Frame(self.master, bg="#181825", padx=10, pady=5)
        record_frame.pack(pady=8, fill="x", padx=40)

        last_txt = f"{self.history['last_time']}s" if self.history["last_time"] else "None"
        best_txt = f"{self.history['best_time']}s" if self.history["best_time"] else "None"

        self.record_label = tk.Label(record_frame, text=f"Last Win: {last_txt}  |  Best Win: {best_txt}", font=("Helvetica", 10, "italic"), bg="#181825", fg="#bac2de")
        self.record_label.pack()

        frame = tk.Frame(self.master, bg="#1e1e2e")
        frame.pack(pady=10)

        self.buttons = {}
        positions = [("RED", 0, 0), ("GREEN", 0, 1), ("BLUE", 1, 0), ("YELLOW", 1, 1)]
        for color, row, col in positions:
            btn = tk.Button(
                frame, text=color, font=("Helvetica", 11, "bold"), width=12, height=4,
                bg=self.colors[color]["normal"], activebackground=self.colors[color]["flash"], relief="flat",
                command=lambda c=color: self.handle_click(c)
            )
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.buttons[color] = btn

        self.start_btn = tk.Button(
            self.master, text="START GAME", font=("Helvetica", 12, "bold"), bg="#89b4fa", fg="#11111b",
            activebackground="#b4befe", relief="flat", command=self.start_game
        )
        self.start_btn.pack(pady=10)

    def start_game(self):
        self.round_number = 0
        self.score = 0
        self.score_label.config(text="Score: 0 / 100")
        self.start_btn.config(state="disabled")

        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

        self.next_round()

    def update_timer(self):
        if self.timer_running:
            elapsed = round(time.time() - self.start_time, 1)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.master.after(100, self.update_timer)

    def next_round(self):
        self.round_number += 1
        self.player_sequence = []
        self.sequence = [random.choice(list(self.colors.keys())) for _ in range(self.round_number)]
        self.status_label.config(text=f"Round {self.round_number}: Watch!")
        self.is_playing = False
        self.master.after(1000, self.play_sequence, 0)

    def play_sequence(self, index):
        if index < len(self.sequence):
            color = self.sequence[index]
            self.flash_button(color)
            self.master.after(800, self.play_sequence, index + 1)
        else:
            self.status_label.config(text="Your turn!")
            self.is_playing = True

    def flash_button(self, color):
        btn = self.buttons[color]
        btn.config(bg=self.colors[color]["flash"])
        self.master.after(400, lambda: btn.config(bg=self.colors[color]["normal"]))

    def handle_click(self, color):
        if not self.is_playing: return

        self.flash_button(color)
        self.player_sequence.append(color)
        current_step = len(self.player_sequence) - 1

        if self.player_sequence[current_step] != self.sequence[current_step]:
            self.game_over()
            return

        if len(self.player_sequence) == len(self.sequence):
            self.score += 10
            self.score_label.config(text=f"Score: {self.score} / 100")
            self.is_playing = False

            if self.score >= 100:
                self.game_win()
            else:
                self.status_label.config(text="Nice! Next round...")
                self.master.after(1000, self.next_round)

    def game_win(self):
        self.timer_running = False
        current_time = round(time.time() - self.start_time, 2)
        prev_best = self.history["best_time"]

        if prev_best is None or current_time < prev_best:
            self.history["best_time"] = current_time

        self.history["last_time"] = current_time
        self.save_history()

        self.record_label.config(text=f"Last Win: {current_time}s  |  Best Win: {self.history['best_time']}s")
        messagebox.showinfo("🎉 YOU WIN!", f"Time Taken: {current_time}s")
        self.status_label.config(text="You won! Press Start to Play Again.")
        self.start_btn.config(state="normal")

    def game_over(self):
        self.timer_running = False
        self.is_playing = False
        messagebox.showinfo("Game Over", f"Wrong sequence!\nFinal Score: {self.score}")
        self.status_label.config(text="Press Start to Try Again")
        self.start_btn.config(state="normal")


# ============================================================
# MODULE 4: MEMORY GAME & PERSONAL STORIES QUIZ
# ============================================================

class MemoryGameStoryQuizView:
    def __init__(self, master):
        self.master = master
        self.stored_entries = []
        self.questions = []
        self.current_q_index = 0
        self.selected_photos = []

        self.relative_name = tk.StringVar()
        self.relation = tk.StringVar()

        self.setup_frame = tk.Frame(self.master, bg="#ecf0f1")
        self.quiz_frame = tk.Frame(self.master, bg="#ecf0f1")

        self.build_setup_ui()

    def build_setup_ui(self):
        self.setup_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        left_panel = tk.Frame(self.setup_frame, bg="#ecf0f1")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(left_panel, text="Add Personal Details & Stories", font=("Arial", 14, "bold"), fg="#2c3e50", bg="#ecf0f1").pack(anchor="w", pady=(0, 10))
        tk.Label(left_panel, text="Name / Title:", bg="#ecf0f1").pack(anchor="w")
        tk.Entry(left_panel, textvariable=self.relative_name, width=35).pack(anchor="w", pady=(0, 10))

        tk.Label(left_panel, text="Relation / Category:", bg="#ecf0f1").pack(anchor="w")
        tk.Entry(left_panel, textvariable=self.relation, width=35).pack(anchor="w", pady=(0, 10))

        tk.Label(left_panel, text="Memory / Story / Detail:", bg="#ecf0f1").pack(anchor="w")
        self.memory_text = tk.Text(left_panel, width=35, height=4)
        self.memory_text.pack(anchor="w", pady=(0, 10))

        btn_frame = tk.Frame(left_panel, bg="#ecf0f1")
        btn_frame.pack(anchor="w")
        tk.Button(btn_frame, text="Save Entry", command=self.save_entry, bg="#27ae60", fg="white", padx=10).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_frame, text="Start Quiz ->", command=self.start_game, bg="#2980b9", fg="white", padx=10).pack(side=tk.LEFT)

        right_panel = tk.Frame(self.setup_frame, bg="#ecf0f1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        tk.Label(right_panel, text="Photos Selected:", font=("Arial", 10, "bold"), bg="#ecf0f1").pack(anchor="w")
        self.photos_listbox = tk.Listbox(right_panel, width=30, height=3)
        self.photos_listbox.pack(fill=tk.X, pady=(0, 5))

        tk.Button(right_panel, text="+ Add Photo(s)", command=self.add_photos).pack(anchor="w", pady=(0, 10))
        tk.Label(right_panel, text="Saved Profiles:", font=("Arial", 10, "bold"), bg="#ecf0f1").pack(anchor="w")
        self.entries_listbox = tk.Listbox(right_panel, width=30, height=5)
        self.entries_listbox.pack(fill=tk.BOTH, expand=True)

    def add_photos(self):
        files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if files:
            for f in files:
                self.selected_photos.append(f)
                self.photos_listbox.insert(tk.END, os.path.basename(f))

    def save_entry(self):
        name = self.relative_name.get().strip()
        rel = self.relation.get().strip()
        story = self.memory_text.get("1.0", tk.END).strip()

        if not name or not rel:
            messagebox.showwarning("Input Error", "Please provide at least a Name and Relation.")
            return

        entry = {"name": name, "relation": rel, "story": story, "photos": list(self.selected_photos)}
        self.stored_entries.append(entry)

        display_text = f"{name} ({rel}) - {len(entry['photos'])} photo(s)"
        self.entries_listbox.insert(tk.END, display_text)

        self.relative_name.set("")
        self.relation.set("")
        self.memory_text.delete("1.0", tk.END)
        self.selected_photos.clear()
        self.photos_listbox.delete(0, tk.END)

    def generate_quiz_questions(self):
        self.questions.clear()
        all_names = [e["name"] for e in self.stored_entries]
        all_relations = list(set([e["relation"] for e in self.stored_entries]))

        for entry in self.stored_entries:
            name, rel, story, photos = entry["name"], entry["relation"], entry["story"], entry["photos"]

            if photos:
                for photo in photos:
                    wrong_names = [n for n in all_names if n != name]
                    opts = random.sample(wrong_names, min(3, len(wrong_names))) + [name]
                    random.shuffle(opts)
                    self.questions.append({"question": "Who or what place is shown in this picture?", "photo": photo, "correct_answer": name, "options": opts})

            wrong_rels = [r for r in all_relations if r != rel]
            opts_rel = random.sample(wrong_rels, min(3, len(wrong_rels))) + [rel]
            random.shuffle(opts_rel)
            self.questions.append({"question": f"What is the category associated with '{name}'?", "photo": photos[0] if photos else "", "correct_answer": rel, "options": opts_rel})

            if story:
                wrong_names = [n for n in all_names if n != name]
                opts_story = random.sample(wrong_names, min(3, len(wrong_names))) + [name]
                random.shuffle(opts_story)
                self.questions.append({"question": f"Who is connected to this memory?\n\"{story}\"", "photo": photos[0] if photos else "", "correct_answer": name, "options": opts_story})

        random.shuffle(self.questions)

    def start_game(self):
        if not self.stored_entries:
            messagebox.showwarning("No Data", "Please save at least one entry before starting!")
            return

        self.generate_quiz_questions()
        self.setup_frame.pack_forget()
        self.quiz_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        self.current_q_index = 0
        self.render_quiz_screen()

    def render_quiz_screen(self):
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()

        if self.current_q_index >= len(self.questions):
            tk.Label(self.quiz_frame, text="Quiz Completed!", font=("Arial", 18, "bold"), bg="#ecf0f1").pack(pady=30)
            tk.Button(self.quiz_frame, text="Return to Setup", command=self.back_to_setup, bg="#2980b9", fg="white", padx=10, pady=5).pack()
            return

        q_data = self.questions[self.current_q_index]

        tk.Label(self.quiz_frame, text=f"Question {self.current_q_index + 1} of {len(self.questions)}", font=("Arial", 10), fg="#7f8c8d", bg="#ecf0f1").pack(pady=5)
        tk.Label(self.quiz_frame, text=q_data["question"], font=("Arial", 12, "bold"), wraplength=550, justify="center", bg="#ecf0f1").pack(pady=10)

        photo_info = os.path.basename(q_data["photo"]) if q_data["photo"] else "No Image Attached"
        tk.Label(self.quiz_frame, text=f"[ Photo: {photo_info} ]", bg="#bdc3c7", width=35, height=5).pack(pady=10)

        options_frame = tk.Frame(self.quiz_frame, bg="#ecf0f1")
        options_frame.pack(pady=10)

        for opt in q_data["options"]:
            tk.Button(options_frame, text=opt, width=22, font=("Arial", 10), command=lambda chosen=opt: self.check_answer(chosen)).pack(pady=3)

    def check_answer(self, choice):
        current_q = self.questions[self.current_q_index]
        if choice == current_q["correct_answer"]:
            messagebox.showinfo("Correct!", "That is correct!")
        else:
            messagebox.showerror("Incorrect", f"Incorrect. The correct answer was '{current_q['correct_answer']}'.")

        self.current_q_index += 1
        self.render_quiz_screen()

    def back_to_setup(self):
        self.quiz_frame.pack_forget()
        self.setup_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    app = UnifiedMemoryApp()
    app.mainloop()
    