import tkinter as tk
import threading
import requests
from tkinter.filedialog import asksaveasfilename
import csv

class ChatApplication(tk.Tk):
    def __init__(self, api_url):
        super().__init__()

        self.title("Tarams ChatBot")

        # Server Requirements
        self.api_url = api_url
        self.messages = []

        self.chat_frame = tk.Frame(self)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.chat_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.chat_canvas = tk.Canvas(self.chat_frame, width=400, height=300, yscrollcommand=self.scrollbar.set)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.scrollbar.config(command=self.chat_canvas.yview)

        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        self.input_entry = tk.Entry(self.input_frame, width=60, font=("Arial", 12))
        self.input_entry.grid(row=0, column=0, padx=(10, 0), pady=10)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(10, 10), pady=10)

        self.chat_frame.columnconfigure(0, weight=1)
        self.chat_frame.rowconfigure(0, weight=1)

        self.messages_frame = tk.Frame(self.chat_canvas)
        self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor=tk.NW)

        self.messages_frame.bind("<Configure>", self.update_canvas_scrollregion)

    def update_canvas_scrollregion(self, event):
        self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)  # Scroll to the bottom

    def send_message(self):
        message = self.input_entry.get()
        self.messages.append({"role": "user", "content": message})
        self.input_entry.delete(0, tk.END)
        self.display_message(message, outgoing=True, sender="You")

        # Here, you can add code to process the message or send it to a chatbot API
        threading.Thread(target=self.process_message).start()

    def process_message(self):
        response = requests.post(self.api_url, json={"messages": self.messages})

        if response.status_code == 200:
            response_content = response.json()
            reply = response_content["reply"]
            self.display_message(reply)
            self.messages.append({"role": "assistant", "content": reply})

            results = response_content.get("results", None)
            if results:
                self.create_csv(results)
        else:
            self.display_message(message="There seems to be a problem with the server. Please contact my devs")
            
    def display_message(self, message, outgoing=False, sender="Bot"):

        bubble_color = "#C2E8FF" if outgoing else "#E8E8E8"  # Light blue for outgoing messages, light gray for incoming

        bubble_frame = tk.Frame(self.messages_frame, bg=bubble_color, padx=10, pady=5)
        bubble_frame.pack(fill=tk.X, padx=10, pady=5)

        sender_label = tk.Label(bubble_frame, text=sender, fg="gray", font=("Arial", 8))
        sender_label.pack(anchor="w")

        bubble_text = tk.Label(bubble_frame, text=message, wraplength=300, justify=tk.LEFT, bg=bubble_color)
        bubble_text.pack(anchor=tk.W if outgoing else tk.E)

    def create_csv(self, data):
        # Prompt the user to select a file location
        file_path = asksaveasfilename(defaultextension='.csv',
                                                filetypes=[('CSV Files', '*.csv')])

        if file_path:
            # Write the data to the selected file
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
                print('CSV file created and saved successfully.')



if __name__ == "__main__":
    app = ChatApplication(api_url="http://127.0.0.1:5000/chat")
    app.display_message(message="Hello, I'm your Database Assistant, ready to support you with all your data-related inquiries and tasks.")
    app.mainloop()
