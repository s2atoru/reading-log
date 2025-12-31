import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from .data_handler import DataHandler, ReadingLogEntry

# UI定数
MAX_PAGE = 1000
MAX_CHAPTER = 100
MAX_SECTION = 50

class ReadingLogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reading Log")
        self.geometry("900x600")
        
        self.data_handler = DataHandler()
        
        self._setup_ui()
        self._refresh_summary()

    def _setup_ui(self):
        # Main container with two panels
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Input Form
        input_frame = ttk.LabelFrame(main_paned, text="Input Form", padding=10)
        main_paned.add(input_frame, weight=1)
        
        self._create_input_form(input_frame)
        
        # Right Panel - Summary View
        summary_frame = ttk.LabelFrame(main_paned, text="Summary / Search", padding=10)
        main_paned.add(summary_frame, weight=2)
        
        self._create_summary_view(summary_frame)

    def _create_input_form(self, parent):
        # Date
        ttk.Label(parent, text="Date:").pack(anchor=tk.W, pady=(0, 2))
        self.date_entry = DateEntry(parent, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(anchor=tk.W, fill=tk.X, pady=(0, 10))
        
        # Title - Using tk.Text (single line) for better IME support on Mac
        # tk.Entry has critical bugs with Japanese IME space conversion
        ttk.Label(parent, text="Title:").pack(anchor=tk.W, pady=(0, 2))
        self.title_text = tk.Text(parent, height=1, highlightthickness=1, relief=tk.SUNKEN, wrap=tk.NONE)
        self.title_text.pack(fill=tk.X, pady=(0, 10))
        # Disable newline insertion
        self.title_text.bind("<Return>", lambda e: "break")
        self.title_text.bind("<KP_Enter>", lambda e: "break")
        
        # Author - Using tk.Text (single line) for better IME support on Mac
        ttk.Label(parent, text="Author:").pack(anchor=tk.W, pady=(0, 2))
        self.author_text = tk.Text(parent, height=1, highlightthickness=1, relief=tk.SUNKEN, wrap=tk.NONE)
        self.author_text.pack(fill=tk.X, pady=(0, 10))
        # Disable newline insertion
        self.author_text.bind("<Return>", lambda e: "break")
        self.author_text.bind("<KP_Enter>", lambda e: "break")
        
        # Position (Page, Chapter, Section)
        pos_frame = ttk.LabelFrame(parent, text="Position (Fill at least one)", padding=5)
        pos_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Page
        ttk.Label(pos_frame, text="Page:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.page_combobox = ttk.Combobox(pos_frame, values=[str(i) for i in range(1, MAX_PAGE + 1, 10)])
        self.page_combobox.grid(row=1, column=0, padx=5, sticky=tk.EW)
        
        # Chapter
        ttk.Label(pos_frame, text="Chapter:").grid(row=0, column=1, padx=5, sticky=tk.W)
        self.chapter_combobox = ttk.Combobox(pos_frame, values=[str(i) for i in range(1, MAX_CHAPTER + 1)])
        self.chapter_combobox.grid(row=1, column=1, padx=5, sticky=tk.EW)
        
        # Section
        ttk.Label(pos_frame, text="Section:").grid(row=0, column=2, padx=5, sticky=tk.W)
        self.section_combobox = ttk.Combobox(pos_frame, values=["Intro", "Conclusion"] + [str(i) for i in range(1, MAX_SECTION)])
        self.section_combobox.grid(row=1, column=2, padx=5, sticky=tk.EW)
        
        pos_frame.columnconfigure(0, weight=1)
        pos_frame.columnconfigure(1, weight=1)
        pos_frame.columnconfigure(2, weight=1)

        # Comment
        ttk.Label(parent, text="Comment:").pack(anchor=tk.W, pady=(0, 2))
        self.comment_text = tk.Text(parent, height=5)
        self.comment_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Save Button
        ttk.Button(parent, text="Save", command=self._save_entry).pack(fill=tk.X, pady=5)
        
        # Status
        self.status_var = tk.StringVar()
        ttk.Label(parent, textvariable=self.status_var, foreground="blue").pack(anchor=tk.W)

    def _create_summary_view(self, parent):
        # Search Bar
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        
        # Using tk.Text (single line) instead of Entry for IME compatibility
        self.search_text = tk.Text(search_frame, height=1, highlightthickness=1, relief=tk.SUNKEN, wrap=tk.NONE)
        self.search_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_text.bind('<Return>', lambda e: (self._refresh_summary(), "break")[1])
        self.search_text.bind("<KP_Enter>", lambda e: (self._refresh_summary(), "break")[1])
        
        ttk.Button(search_frame, text="Go", width=4, command=self._refresh_summary).pack(side=tk.LEFT, padx=(5, 0))

        # Treeview
        columns = ("date", "title", "author", "position")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings")
        self.tree.heading("date", text="Date")
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("position", text="Position")
        
        self.tree.column("date", width=100)
        self.tree.column("title", width=200)
        self.tree.column("author", width=150)
        self.tree.column("position", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def _save_entry(self):
        try:
            # データ収集とバリデーション
            page_val = self.page_combobox.get().strip()
            page = None
            if page_val:
                try:
                    page = int(page_val)
                    if page < 1 or page > MAX_PAGE:
                        raise ValueError(f"ページは1から{MAX_PAGE}の範囲で入力してください。")
                except ValueError as e:
                    if "invalid literal" in str(e):
                        raise ValueError(f"ページには数値を入力してください: {page_val}")
                    raise
            
            entry = ReadingLogEntry(
                title=self.title_text.get("1.0", tk.END).strip(),
                author=self.author_text.get("1.0", tk.END).strip(),
                date=self.date_entry.get_date().isoformat(),
                page=page,
                chapter=self.chapter_combobox.get() or None,
                section=self.section_combobox.get() or None,
                comment=self.comment_text.get("1.0", tk.END).strip()
            )
            
            self.data_handler.save_entry(entry)
            self._clear_form()
            self._refresh_summary()
            self.status_var.set(f"Saved: {entry.title}")
            messagebox.showinfo("Success", "Reading log saved successfully!")
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _clear_form(self):
        self.title_text.delete("1.0", tk.END)
        self.author_text.delete("1.0", tk.END)
        self.page_combobox.set("")
        self.chapter_combobox.set("")
        self.section_combobox.set("")
        self.comment_text.delete("1.0", tk.END)
        # Keep date as is or reset to today? Usually keeping is fine, but resetting to today is safer default.
        self.date_entry.set_date(datetime.now())

    def _refresh_summary(self):
        # Clear current
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        query = self.search_text.get("1.0", tk.END).strip()
        entries = self.data_handler.search_entries(query)
        
        for entry in entries:
            # Format position string
            pos_parts = []
            if entry.page: pos_parts.append(f"p.{entry.page}")
            if entry.chapter: pos_parts.append(f"ch.{entry.chapter}")
            if entry.section: pos_parts.append(f"sec.{entry.section}")
            pos_str = ", ".join(pos_parts)
            
            self.tree.insert("", tk.END, values=(entry.date, entry.title, entry.author, pos_str))

if __name__ == "__main__":
    app = ReadingLogApp()
    app.mainloop()
