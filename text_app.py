#!/usr/bin/env python3
"""
Text Creation Application with datetime
This application allows users to create, view, and search text notes with timestamps.
"""

import os
import datetime

class TextApp:
    def __init__(self, storage_file="notes.txt"):
        """Initialize the text application with a storage file."""
        self.storage_file = storage_file
        self.notes = self._load_notes()

    def _load_notes(self):
        """Load notes from the storage file if it exists."""
        notes = []
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
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
                print(f"Error reading {self.storage_file}: {e}. Starting with empty notes.")
                return []
        return notes

    def _save_notes(self):
        """Save notes to the storage file."""
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            for note in self.notes:
                f.write("===== NOTE START =====\n")
                f.write(f"{note['timestamp']}\n")
                f.write(f"{note['date']}\n")
                f.write(f"{note['content']}\n")
                f.write("===== NOTE END =====\n\n")

    def create_note(self, content):
        """Create a new note with the current timestamp."""
        timestamp = datetime.datetime.now().isoformat()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        note = {
            "timestamp": timestamp,
            "content": content,
            "date": date
        }
        self.notes.append(note)
        self._save_notes()
        print(f"Note created at {timestamp}")

    def view_all_notes(self):
        """Display all notes."""
        if not self.notes:
            print("No notes found.")
            return

        for i, note in enumerate(self.notes, 1):
            dt = datetime.datetime.fromisoformat(note["timestamp"])
            formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Note {i} ({formatted_time}) ---")
            print(note["content"])
            print("-" * 30)

    def search_by_date(self, date_str):
        """Search notes by date (YYYY-MM-DD format)."""
        try:
            # Validate date format
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        found_notes = [note for note in self.notes if note["date"] == date_str]
        
        if not found_notes:
            print(f"No notes found for date {date_str}.")
            return

        print(f"\nFound {len(found_notes)} notes for {date_str}:")
        for i, note in enumerate(found_notes, 1):
            dt = datetime.datetime.fromisoformat(note["timestamp"])
            formatted_time = dt.strftime("%H:%M:%S")
            print(f"\n--- Note {i} ({formatted_time}) ---")
            print(note["content"])
            print("-" * 30)

def main():
    """Main function to run the text application."""
    app = TextApp()
    
    while True:
        print("\n===== Text Creation App =====")
        print("1. Create a new note")
        print("2. View all notes")
        print("3. Search notes by date")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == "1":
            content = input("\nEnter your note content (type 'done' on a new line to finish):\n")
            multi_line_content = []
            
            while True:
                multi_line_content.append(content)
                content = input()
                if content.lower() == 'done':
                    break
            
            final_content = "\n".join(multi_line_content)
            app.create_note(final_content)
            
        elif choice == "2":
            app.view_all_notes()
            
        elif choice == "3":
            date_str = input("Enter date to search (YYYY-MM-DD): ")
            app.search_by_date(date_str)
            
        elif choice == "4":
            print("Thank you for using the Text Creation App. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()