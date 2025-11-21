# ChatbotwithDBMS
# SVD Coaching Centre — Chatbot with DBMS (Tkinter + MySQL + NLTK + pyttsx3)

This repository contains a simple desktop chatbot application (chatbot.py) that demonstrates:
- a Tkinter GUI for user interaction,
- NLTK's rule-based Chat for fallback pattern responses,
- a MySQL-backed responses table so the bot can fetch custom answers from a database,
- pyttsx3 for text-to-speech,
- time-based greetings and simple About / Contact / Help screens.

This README summarizes how the code works, installation steps, the database schema and sample data, and tips for customizing and running the app.

---

## Features (as implemented in chatbot.py)
- Graphical interface (Tkinter) with:
  - a scrollable conversation area,
  - an entry field for the user,
  - Send, About, Contact, and Help buttons.
- NLTK Chat patterns for simple rule-based replies.
- MySQL lookup: the bot first queries a `chatbot_responses` table for a matching question; if none found, it uses NLTK patterns.
- Text-to-speech using pyttsx3 for spoken responses.
- Time-aware greeting (morning/afternoon/evening/night).
- Simple About and Contact content displayed in the conversation area.

---

## Requirements

- Python 3.8+
- Packages:
  - tkinter (usually included with standard Python on most platforms)
  - mysql-connector-python
  - nltk
  - pyttsx3

Install Python packages with pip:

pip install mysql-connector-python nltk pyttsx3

If you don't have tkinter, install it with your OS package manager (e.g., apt, brew). On Windows/macOS it typically comes with Python.

---

## Quick setup

1. Clone the repo:
   git clone https://github.com/SkAfnaan1/ChatbotwithDBMS.git
   cd ChatbotwithDBMS

2. Create and configure the MySQL database (see next section).

3. Configure database credentials (do NOT hardcode credentials in files for production; see Configuration notes below).

4. Run:
   python chatbot.py

---

## Database schema and sample data

The bot expects a MySQL database named (by default) `svd_coaching_centre` and a table `chatbot_responses` with at least the following columns:

SQL to create the database and table:

```sql
-- create database (run as a user with appropriate privileges)
CREATE DATABASE IF NOT EXISTS svd_coaching_centre;
USE svd_coaching_centre;

-- create responses table
CREATE TABLE IF NOT EXISTS chatbot_responses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  question TEXT NOT NULL,
  response TEXT NOT NULL
);
```

Sample rows:

```sql
INSERT INTO chatbot_responses (question, response) VALUES
('admissions', 'Our college admissions process typically involves filling an online application, submitting transcripts, and an entrance interview.'),
('fees', 'Fee structure varies by program. Please contact the office for detailed fee information.'),
('location', 'SVD Coaching Centre is located in Kandlakoya, Medchal, Hyderabad, Telangana, India.'),
('office timing', 'Our office hours are Monday to Saturday, 9:00 AM to 6:00 PM.');
```

Notes:
- The code uses a `LIKE '%user_input%'` query, so shorter keywords can match stored questions. You can adapt to more robust matching if needed (full-text search, normalized columns, etc.).

---

## Configuration

In the shipped chatbot.py the DB connection is created like:

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Subhanmohammad5943',
    database='svd_coaching_centre'
)

Important security note: Do not commit real credentials. Instead, update the script to read credentials from environment variables or a config file. Example (use before connecting):

- Using environment variables (recommended):
  - export DB_HOST=localhost
  - export DB_USER=root
  - export DB_PASS=supersecret
  - export DB_NAME=svd_coaching_centre

Then in Python:

import os
host = os.environ.get('DB_HOST', 'localhost')
user = os.environ.get('DB_USER', 'root')
password = os.environ.get('DB_PASS', '')
database = os.environ.get('DB_NAME', 'svd_coaching_centre')

---

## How the key parts work (mapping to chatbot.py)

- patterns: A list of regex patterns and corresponding fallback responses used by NLTK's Chat.
- chatbot = Chat(patterns, reflections): creates the rule-based component.
- get_response_from_db(user_input): connects to MySQL and queries `chatbot_responses` for a row whose `question` contains the user input. Returns the stored response if found.
- send_message(user_input): orchestrates reading user input, trying DB lookup, falling back to NLTK Chat, speaking the response (pyttsx3), and updating the GUI conversation area.
- greet_user(): uses datetime.now().hour to choose a greeting and speaks + displays it.
- show_about(), show_contact(), ask_help(): utility functions to display static info in the conversation window.

---

## Usage / example

1. Start the app:
   python chatbot.py

2. The application window will appear and greet you.

3. Type queries into the input field and press "Send" (or use the GUI Send button). 
   - If your query matches a DB record (via LIKE), the database response is used.
   - Otherwise, the NLTK patterns are checked for a pattern match.
   - The bot will also speak the response via your system's audio.

Example interactions:
- User: hi
  Bot: Hello!
- User: how are you?
  Bot: I'm doing well, thank you!
- User: admissions
  Bot: Our college admissions process typically involves...

---

## Customization

- Add/modify NLTK patterns in the `patterns` list (top of chatbot.py).
- Populate `chatbot_responses` table with more question/response pairs to provide richer DB-driven replies.
- Improve matching logic: instead of LIKE, use pre-processing, tokenization, or full-text indexes.
- Replace text-to-speech engine or tune voice properties via pyttsx3 API.

---

## Troubleshooting

- "ModuleNotFoundError: No module named 'mysql.connector'": install mysql-connector-python.
- Pyttsx3 issues on Linux: you may need to install extra back-end packages (espeak, pulseaudio) depending on your distribution.
- Tkinter not found: install tkinter for your OS or use a Python distribution that includes it.
- Database connection errors: verify host, user, password, and that MySQL server is running and accessible. Check user privileges.

---

## Security & Privacy

- Never commit credentials (usernames, passwords) to source control.
- Prefer environment variables or a configuration file that's gitignored.
- If deploying or sharing, sanitize any real personal contact details.

---

## Extending to a networked bot / web
This project is a desktop GUI demo. To make it accessible to multiple users, you can:
- Build a web front-end (Flask / FastAPI) and expose API endpoints.
- Move DB access to a server process and secure endpoints with authentication.
- Replace NLTK Chat with ML-based intent classification for more robust understanding.

---

## License
Add a license of your choice (e.g., MIT). If you have no preference, add an `LICENSE` file.

---

If you'd like, I can:
- produce the SQL file with sample inserts ready to import,
- update chatbot.py to read DB credentials from environment variables,
- or prepare a more detailed README with screenshots and sample commands for Windows/macOS/Linux.
