# Import the Libraries
import sys
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption, QKeyEvent, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextBrowser, QTextEdit

# Class function
class DailyLogApp(QWidget):
    def __init__(self):
        super().__init__()

        self.total = 0
        self.history = []
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle('Daily Log App')

        # Load your icon image file
        icon = QIcon("../daily-log.ico")  # Replace with the actual path to your icon

        # Set the window icon
        self.setWindowIcon(icon)

        self.total_label = QLabel('Total : 0', self)  
        self.history_browser = QTextBrowser(self)
        self.history_browser.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)  # Enable word wrap
        self.history_browser.setLineWrapMode(QTextEdit.WidgetWidth)  # Allow wrapping at widget's width
        self.history_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrollbar
        self.history_browser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Enable vertical scrollbar

        self.input_line_edit = QLineEdit(self)
        self.input_line_edit.setFixedSize(300, 30)
        self.input_line_edit.setAlignment(Qt.AlignRight)

        # Increase the font size for the total label
        total_font = self.total_label.font()
        total_font.setPointSize(12)  # Adjust the font size as needed
        self.total_label.setFont(total_font)

        # Increase the font size for the input line
        input_line_font = self.input_line_edit.font()
        input_line_font.setPointSize(14)  # Adjust the font size as needed
        self.input_line_edit.setFont(input_line_font)

        # Create number buttons
        button_layout = QVBoxLayout()
        button_grid = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['q / clear','0', '.']
        ]
        for row in button_grid:
            h_layout = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text, self)
                if button_text == 'q / clear':
                    button.clicked.connect(lambda _, text=button_text: self.handle_button_click(text))
                else:
                    button.clicked.connect(lambda state, text=button_text: self.handle_button_click(text))
                
                # Increase the font size for the buttons
                button_font = button.font()
                button_font.setPointSize(14)  # Adjust the font size as needed
                button.setFont(button_font)
                
                h_layout.addWidget(button)
            button_layout.addLayout(h_layout)

        # Add / Enter buttons
        control_layout = QHBoxLayout()
        add_button = QPushButton('Add / Enter', self)
        add_button.clicked.connect(self.add_button_clicked)

        # Increase the font size for the "Add/Enter" button
        add_button_font = add_button.font()
        add_button_font.setPointSize(14)  # Adjust the font size as needed
        add_button.setFont(add_button_font)

        control_layout.addWidget(add_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.total_label, alignment=Qt.AlignTop)
        main_layout.addWidget(self.history_browser)  # Use QTextBrowser instead of QLabel
       
        # Use QHBoxLayout to center the input line
        input_line_layout = QHBoxLayout()
        input_line_layout.addWidget(self.input_line_edit, alignment=Qt.AlignCenter)
        main_layout.addLayout(input_line_layout)
        
        main_layout.addLayout(button_layout)
        main_layout.addLayout(control_layout)
        main_layout.setAlignment(Qt.AlignTop)

        self.setLayout(main_layout)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if 48 <= key <= 57:  # Handle number keys (0-9)
            self.input_line_edit.insert(str(key - 48))
        elif key == 46:  # Handle period key '.'
            self.input_line_edit.insert('.')
        elif key == Qt.Key_Backspace:  # Handle backspace
            self.input_line_edit.backspace()
        elif key == Qt.Key_Q:
            self.input_line_edit.clear()
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.add_button_clicked()
        elif key == Qt.Key_Plus:
            self.handle_button_click('+')
        else:
            # Handle other key events
            super().keyPressEvent(event)


    def handle_button_click(self, button_text):
        if button_text.isdigit() or button_text == '.':
            self.input_line_edit.insert(button_text)
        elif button_text.lower() == 'q / clear':
            self.input_line_edit.clear()


    def add_button_clicked(self):
        try:
            number = float(self.input_line_edit.text())
            self.history.append(number)
            self.total += number
            self.input_line_edit.clear()# Clear the input line for the next number
            self.update_display()
            self.save_data()
        except ValueError:
            pass  # Ignore invalid input

    def update_display(self):
        self.total_label.setText(f'Total: {self.total}')
        # self.history_browser.setPlainText(f'History: {self.history}')
        self.history_browser.setPlainText(f'History: {", ".join(map(str, self.history))}\n')
       

    def save_data(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # log_entry = f'INFO: "Added" | Timestamp: {timestamp} | Total: {self.total} | History: {self.history}\n'
        log_entry = f'INFO: "Added" | Timestamp: {timestamp} | Total: {self.total} | History: {",".join(map(str, self.history))}\n'

        with open('daily-spend-log.txt', 'a') as log_file:
            log_file.write(log_entry)
           

    def load_data(self):
        if not self.history:
            if not self.load_history_from_file():
                return
            self.total = sum(self.history)
            self.update_display()
    
    def load_history_from_file(self):
        try:
            with open('daily-spend-log.txt', 'r') as file:
                lines = file.readlines()
                for line in reversed(lines):
                    if "History:" in line:
                        # history_str = line.split(":")[4].strip()
                        history_str = line.split("History:")[1].strip()
                        print("History Values : " + history_str)

                        try:
                            self.history = [float(num.strip()) for num in history_str.split(',')]
                            return True
                        except ValueError:
                            print("Error parsing history values.")
                            return False
                # If no "History:" is found in the file, initialize history to an empty list
                self.history = []
                return True
        except FileNotFoundError:
            print("File not found. Creating a new file.")
            with open('daily-spend-log.txt', 'w'):
                pass
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
        return False


def main():
    app = QApplication(sys.argv)
    daily_log_app = DailyLogApp()
    daily_log_app.show()
    sys.exit(app.exec_())
    
# Main Function
if __name__ == '__main__':
    main()

