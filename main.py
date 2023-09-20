
import os
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
import sys

# Function to combine CSV files
def combine_csv_files(directory_path, output_file_name):
    all_dfs = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            full_file_path = os.path.join(directory_path, filename)
            df = pd.read_csv(full_file_path)
            df['Source File'] = filename
            all_dfs.append(df)
    combined_df = pd.concat(all_dfs, ignore_index=True)
    output_file = os.path.join(directory_path, output_file_name)
    if not output_file_name.lower().endswith('.csv'):
        output_file += '.csv'
    combined_df.to_csv(output_file, index=False)

# Initialize PyQt application
app = QApplication(sys.argv)

# Main window setup
window = QWidget()
window.setWindowTitle('Combine CSV Files')
layout = QVBoxLayout()

# Widgets
directory_edit = QLineEdit()
directory_edit.setPlaceholderText('Directory path containing CSV files')
output_edit = QLineEdit()
output_edit.setPlaceholderText('Output file name (e.g., combined)')
status_label = QLabel('Status: Awaiting input')
combine_button = QPushButton('Combine CSV Files')
browse_button = QPushButton('Browse Directory')

# Directory browsing functionality
def browse_directory():
    dialog = QFileDialog()
    directory_path = dialog.getExistingDirectory(window, "Select Directory")
    if directory_path:
        directory_edit.setText(directory_path)

# Combine button functionality
def start_combining():
    directory_path = directory_edit.text()
    output_file_name = output_edit.text()
    if not directory_path or not output_file_name:
        status_label.setText('Status: Please fill in both fields.')
        return
    try:
        combine_csv_files(directory_path, output_file_name)
        status_label.setText(f'Status: CSV files combined and saved as {output_file_name}.csv')
    except Exception as e:
        status_label.setText(f'Status: An error occurred. {str(e)}')

# Connect button signals to functions
combine_button.clicked.connect(start_combining)
browse_button.clicked.connect(browse_directory)

# Add widgets to layout
layout.addWidget(directory_edit)
layout.addWidget(browse_button)
layout.addWidget(output_edit)
layout.addWidget(combine_button)
layout.addWidget(status_label)

# Set layout and show window
window.setLayout(layout)
window.show()

# Run the application
app.exec()
