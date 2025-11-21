import tkinter as tk
from tkinter import scrolledtext
import mysql.connector
from mysql.connector import Error
from nltk.chat.util import Chat, reflections
import pyttsx3
from datetime import datetime

# Define patterns and responses for the chatbot
patterns = [
    (r'hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']),
    (r'how are you?', ['I\'m doing well, thank you!', 'I\'m good, thanks for asking.']),
    (r'what is your name?', ['You can call me Chatbot.', 'I\'m just a humble chatbot.']),
    (r'bye|goodbye', ['Goodbye!', 'Have a great day!', 'Bye!']),
    (r'(.*)enquiry(.*)', ['How can I assist you with your enquiry?']),
    (r'(.*) (apply|application) to (college|university)', ['Our college admissions process typically involves...']),
    # Add more patterns and responses as needed
]

# Create a chatbot using the defined patterns
chatbot = Chat(patterns, reflections)

# Function to fetch response from database
def get_response_from_db(user_input):
    try:
        # Connect to your MySQL database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Subhanmohammad5943',
            database='svd_coaching_centre'
        )
        
        cursor = conn.cursor()
        
        # SQL query to fetch response from the chatbot_responses table
        query = "SELECT response FROM chatbot_responses WHERE question LIKE %s"
        cursor.execute(query, ('%' + user_input + '%',))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return result[0] if result else None
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to handle user input and display chatbot responses
def send_message(user_input=None):
    if not user_input:
        user_input = input_field.get()
        input_field.delete(0, tk.END)
    
    response = get_response_from_db(user_input)
    if not response:
        response = chatbot.respond(user_input)
    
    # Speak the response
    engine.say(response)
    engine.runAndWait()
    
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete(1.0, tk.END)
    conversation_area.insert(tk.END, "You: {}\n".format(user_input))
    conversation_area.insert(tk.END, "Bot: {}\n".format(response))
    conversation_area.config(state=tk.DISABLED)
    conversation_area.see(tk.END)

# Function to submit user query
def submit_query():
    user_input = user_query_entry.get()
    send_message(user_input)

# Function to handle About button click
def show_about():
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete(1.0, tk.END)
    
    # Set font to bold
    conversation_area.tag_configure("bold", font=("Times New Roman", 12, "bold"))
    
    about_text = """
    SVD Coaching Centre
    Established: 2000
    Founders: MD SUBHAN,C DIVYA,E.VIVEK
    Location:  Kandlakoya, Medchal, Hyderabad,Telangana,India
    """
    conversation_area.insert(tk.END, about_text, "bold")
    conversation_area.config(state=tk.DISABLED)

# Function to handle Contact button click
def show_contact():
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete(1.0, tk.END)
    
    # Set font to bold
    conversation_area.tag_configure("bold", font=("Times New Roman", 12, "bold"))
    
    contact_text = """
    Contact Information:
    Head:  Mr.M.Madhusudhan - 7869547387
    Founder: Mr.MD.Subhan-7799093361,Ms.Divya-8976534124,Mr.Vivek-9876543281
    Receptionist: Mary Johnson -  7778896574
    """
    conversation_area.insert(tk.END, contact_text, "bold")
    conversation_area.config(state=tk.DISABLED)

# Function to handle help button click
def ask_help():
    conversation_area.config(state=tk.NORMAL)
    conversation_area.delete(1.0, tk.END)
    
    # Set font to Times New Roman and bold
    conversation_area.tag_configure("bold", font=("Times New Roman", 12, "bold"))
    conversation_area.insert(tk.END, "Welcome to the Help Center! How can I assist you?\n")
    
    conversation_area.config(state=tk.DISABLED)
    
    # Show the submit button
    send_button.pack(side=tk.TOP, padx=10, pady=10)

    # Speak the welcome message
    engine.say("Welcome to the Help Center! How can I assist you?")
    engine.runAndWait()

# Function to greet user based on the current time
def greet_user():
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon!"
    elif 18 <= current_hour < 22:
        greeting = "Good evening!"
    else:
        greeting = "Good night!"
    
    welcome_message = f"{greeting} Welcome to SVD Coaching Centre!"
    
    conversation_area.config(state=tk.NORMAL)
    conversation_area.insert(tk.END, "Bot: {}\n".format(welcome_message))
    conversation_area.config(state=tk.DISABLED)
    conversation_area.see(tk.END)
    
    # Speak the greeting
    engine.say(welcome_message)
    engine.runAndWait()

# Create the main window
root = tk.Tk()
root.title("SVD COACHING CENTRE ENQUIRY")
root.configure(highlightbackground="green", highlightthickness=10, highlightcolor="green")

# Create and configure the conversation area
conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
conversation_area.pack(padx=10, pady=10)
conversation_area.config(state=tk.DISABLED)

# Create the user query entry field
user_query_entry = tk.Entry(root, width=50)
user_query_entry.pack(pady=(0, 10))

# Create the Send button
send_button = tk.Button(root, text="Send", command=submit_query)

# Create the About, Contact, and Help buttons
about_button = tk.Button(root, text="About", command=show_about)
about_button.pack(side=tk.LEFT, padx=10, pady=10)

contact_button = tk.Button(root, text="Contact", command=show_contact)
contact_button.pack(side=tk.LEFT, padx=10, pady=10)

help_button = tk.Button(root, text="Help", command=ask_help)
help_button.pack(side=tk.LEFT, padx=10, pady=10)

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

# Greet the user based on the current time
greet_user()

# Start the GUI event loop
root.mainloop()
 
