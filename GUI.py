
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from query import run

def browse_file():
    """Open file dialog to select FASTA file(s)."""
    paths = filedialog.askopenfilenames(
        title="Select FASTA file(s)",
        filetypes=[("FASTA files", "*.fasta *.fa *.txt"), ("All files", "*.*")]
    )
    fasta_var.set(" ".join(paths))

def start_search():
    """Run the search and show results in text box."""
    pattern = pattern_var.get().strip()
    fasta_files = fasta_var.get().split()

    if not pattern:
        messagebox.showerror("Error", "Please enter a pattern.")
        return
    if not fasta_files:
        messagebox.showerror("Error", "Please select at least one FASTA file.")
        return

    # Clear previous results
    results_box.delete(1.0, tk.END)

    try:
        hit_count = run(pattern, fasta_files, ignore_case=not case_sensitive_var.get())
        if hit_count == 0:
            results_box.insert(tk.END, "No matches found.\n")
        else:
            results_box.insert(tk.END, f"Search complete. Found {hit_count} matches.\n")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("Protein Sequence Search (BMH)")
root.geometry("600x400")

# Pattern input
tk.Label(root, text="Pattern:").pack(anchor="w", padx=10, pady=5)
pattern_var = tk.StringVar()
tk.Entry(root, textvariable=pattern_var, width=40).pack(anchor="w", padx=10)

# FASTA file input
tk.Label(root, text="FASTA File(s):").pack(anchor="w", padx=10, pady=5)
fasta_var = tk.StringVar()
tk.Entry(root, textvariable=fasta_var, width=50).pack(anchor="w", padx=10, side="left")
tk.Button(root, text="Browse", command=browse_file).pack(anchor="w", padx=10, pady=5)

# Case sensitivity
case_sensitive_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Case-sensitive search", variable=case_sensitive_var).pack(anchor="w", padx=10, pady=5)

# Search button
tk.Button(root, text="Search", command=start_search, bg="#4CAF50", fg="white").pack(pady=10)

# Results box
results_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
results_box.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()