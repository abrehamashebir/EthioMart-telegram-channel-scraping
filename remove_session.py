import os

session_name = 'scraping_session'  # Replace with your session name
session_file = f'{session_name}.session'

if os.path.exists(session_file):
    os.remove(session_file)
    print(f"Session file '{session_file}' deleted.")
else:
    print(f"No session file named '{session_file}' found.")
