import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading


class AIStoryGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Story Generator")
        self.root.geometry("600x500")

        # --- Style Configuration ---
        self.bg_color = "#282c34"
        self.text_color = "#abb2bf"
        self.widget_bg = "#3c3f41"
        self.button_color = "#61afef"
        self.font = ("Consolas", 12)

        self.root.configure(bg=self.bg_color)

        # --- UI Elements ---
        main_frame = tk.Frame(root, bg=self.bg_color, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Prompt Label and Entry
        prompt_label = tk.Label(main_frame, text="Enter a story prompt:", font=(self.font[0], 14, "bold"),
                                bg=self.bg_color, fg=self.text_color)
        prompt_label.pack(anchor='w', pady=(0, 5))

        self.prompt_entry = tk.Entry(main_frame, font=self.font, bg=self.widget_bg, fg=self.text_color,
                                     insertbackground="white", width=70)
        self.prompt_entry.pack(fill=tk.X, ipady=5, pady=(0, 15))
        self.prompt_entry.insert(0, "A knight discovering a hidden, magical library.")

        # Generate Button
        self.generate_button = tk.Button(main_frame, text="Generate Story", font=(self.font[0], 12, "bold"),
                                         bg=self.button_color, fg="white", command=self.start_story_generation_thread,
                                         relief=tk.FLAT)
        self.generate_button.pack(fill=tk.X, ipady=8, pady=(0, 15))

        # Result Display
        self.story_display = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, font=self.font, bg=self.widget_bg,
                                                       fg=self.text_color, state=tk.DISABLED, borderwidth=0,
                                                       highlightthickness=0)
        self.story_display.pack(fill=tk.BOTH, expand=True)

    def generate_story(self):
        """Uses the Gemini API to generate a story based on the prompt."""
        prompt = self.prompt_entry.get()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt.")
            self.enable_ui()
            return

        self.story_display.config(state=tk.NORMAL)
        self.story_display.delete("1.0", tk.END)
        self.story_display.insert(tk.END, "✍️ Generating your story... please wait.")
        self.story_display.config(state=tk.DISABLED)
        self.root.update_idletasks()

        try:
            # Using the Gemini Flash model for speed
            api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

            # Note: A real app would use an API key, but for this demo we rely on free access where available.
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{
                    "parts": [
                        {"text": f"Write a short, creative story (about 200 words) based on this prompt: {prompt}"}]
                }]
            }

            response = requests.post(api_url, headers=headers, json=payload, timeout=45)
            response.raise_for_status()

            result = response.json()

            # Safely extract the text
            if result.get('candidates') and result['candidates'][0].get('content', {}).get('parts'):
                story_text = result['candidates'][0]['content']['parts'][0]['text']
            else:
                story_text = "Error: Could not find generated text in the API response."

            self.story_display.config(state=tk.NORMAL)
            self.story_display.delete("1.0", tk.END)
            self.story_display.insert(tk.END, story_text)
            self.story_display.config(state=tk.DISABLED)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("API Error", f"A network error occurred: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.enable_ui()

    def start_story_generation_thread(self):
        """Starts the story generation in a separate thread to keep the UI responsive."""
        self.disable_ui()
        thread = threading.Thread(target=self.generate_story)
        thread.daemon = True
        thread.start()

    def disable_ui(self):
        self.generate_button.config(state=tk.DISABLED, text="Generating...")
        self.prompt_entry.config(state=tk.DISABLED)

    def enable_ui(self):
        self.generate_button.config(state=tk.NORMAL, text="Generate Story")
        self.prompt_entry.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    app = AIStoryGeneratorApp(root)
    root.mainloop()
