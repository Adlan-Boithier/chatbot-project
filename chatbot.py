from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_response(prompt, max_length=50):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

import tkinter as tk
from tkinter import scrolledtext

window = tk.Tk()
window.title("Chatbot avec GPT-2")
window.geometry("500x400")

chat_area = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(window)
input_frame.pack(padx=10, pady=10, fill=tk.X)

user_input = tk.Entry(input_frame, width=40)
user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

def send_message():
    user_text = user_input.get()
    if user_text.strip() == "":
        return

    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Toi: {user_text}\n")
    chat_area.config(state='disabled')

    response = generate_response(user_text)
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"Chatbot: {response}\n")
    chat_area.config(state='disabled')

    user_input.delete(0, tk.END)
    chat_area.yview(tk.END)

send_button = tk.Button(input_frame, text="Envoyer", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5)

window.mainloop()