#!/usr/bin/env python3
"""
Web-based Text Creation Application with datetime
This application provides a web interface for creating, viewing, and searching text notes with timestamps.
"""

import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)
STORAGE_FILE = "notes.txt"

def load_notes():
    """Load notes from the storage file if it exists."""
    notes = []
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                note_blocks = content.split("===== NOTE START =====")
                
                for block in note_blocks:
                    if not block.strip():
                        continue
                    
                    lines = block.strip().split('\n')
                    if len(lines) >= 3:  # At least timestamp, date, and some content
                        timestamp = lines[0].strip()
                        date = lines[1].strip()
                        note_content = '\n'.join(lines[2:]).strip()
                        
                        note = {
                            "timestamp": timestamp,
                            "date": date,
                            "content": note_content
                        }
                        notes.append(note)
        except Exception as e:
            print(f"Error reading {STORAGE_FILE}: {e}. Starting with empty notes.")
            return []
    return notes

def save_notes(notes):
    """Save notes to the storage file."""
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        for note in notes:
            f.write("===== NOTE START =====\n")
            f.write(f"{note['timestamp']}\n")
            f.write(f"{note['date']}\n")
            f.write(f"{note['content']}\n")
            f.write("===== NOTE END =====\n\n")

@app.route('/')
def index():
    """Render the main page."""
    notes = load_notes()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return render_template('index.html', notes=notes, current_date=current_date)

@app.route('/create', methods=['POST'])
def create_note():
    """Create a new note with the current timestamp."""
    content = request.form.get('content', '')
    if not content.strip():
        return redirect(url_for('index'))
    
    timestamp = datetime.datetime.now().isoformat()
    note = {
        "timestamp": timestamp,
        "content": content,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    
    notes = load_notes()
    notes.append(note)
    save_notes(notes)
    
    return redirect(url_for('index'))

@app.route('/search')
def search():
    """Search notes by date."""
    date_str = request.args.get('date', '')
    notes = load_notes()
    
    if date_str:
        try:
            # Validate date format
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            filtered_notes = [note for note in notes if note["date"] == date_str]
        except ValueError:
            filtered_notes = []
    else:
        filtered_notes = notes
    
    return jsonify(filtered_notes)

# Create templates directory and HTML template
def create_templates():
    """Create the templates directory and HTML template if they don't exist."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    index_html = os.path.join(templates_dir, 'index.html')
    if not os.path.exists(index_html):
        with open(index_html, 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Creation App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        textarea {
            width: 100%;
            height: 150px;
            padding: 10px;
            box-sizing: border-box;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
        }
        .note {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        .note-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            color: #666;
        }
        .search-container {
            margin: 20px 0;
            display: flex;
            align-items: center;
        }
        .search-container input {
            padding: 8px;
            margin-right: 10px;
        }
    </style>
</head>
<body>
    <h1>Text Creation App</h1>
    
    <div class="form-container">
        <h2>Create a New Note</h2>
        <form action="/create" method="post">
            <div class="form-group">
                <textarea name="content" placeholder="Enter your note here..."></textarea>
            </div>
            <button type="submit">Save Note</button>
        </form>
    </div>
    
    <div class="search-container">
        <h2>Search Notes by Date</h2>
        <input type="date" id="search-date" value="{{ current_date }}">
        <button onclick="searchNotes()">Search</button>
    </div>
    
    <div id="notes-container">
        <h2>Your Notes</h2>
        {% if notes %}
            {% for note in notes %}
                <div class="note">
                    <div class="note-header">
                        <span>Date: {{ note.date }}</span>
                        <span>Time: {{ note.timestamp.split('T')[1].split('.')[0] }}</span>
                    </div>
                    <div class="note-content">{{ note.content }}</div>
                </div>
            {% endfor %}
        {% else %}
            <p>No notes found. Create your first note above!</p>
        {% endif %}
    </div>
    
    <script>
        function searchNotes() {
            const date = document.getElementById('search-date').value;
            fetch(`/search?date=${date}`)
                .then(response => response.json())
                .then(notes => {
                    const container = document.getElementById('notes-container');
                    container.innerHTML = '<h2>Search Results</h2>';
                    
                    if (notes.length === 0) {
                        container.innerHTML += '<p>No notes found for this date.</p>';
                        return;
                    }
                    
                    notes.forEach(note => {
                        const time = note.timestamp.split('T')[1].split('.')[0];
                        const noteDiv = document.createElement('div');
                        noteDiv.className = 'note';
                        noteDiv.innerHTML = `
                            <div class="note-header">
                                <span>Date: ${note.date}</span>
                                <span>Time: ${time}</span>
                            </div>
                            <div class="note-content">${note.content}</div>
                        `;
                        container.appendChild(noteDiv);
                    });
                })
                .catch(error => console.error('Error searching notes:', error));
        }
    </script>
</body>
</html>""")

if __name__ == "__main__":
    create_templates()
    app.run(host='0.0.0.0', port=50349, debug=True)