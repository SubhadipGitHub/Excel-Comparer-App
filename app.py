import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import font

class DataComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Comparer Application")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        self.file1 = None
        self.file2 = None
        self.df1 = None
        self.df2 = None

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_font = font.Font(family="Helvetica", size=16, weight="bold")
        ttk.Label(self.root, text="Data Comparer Application", font=title_font, background="#f0f0f0").pack(pady=10)

        # File Upload Section
        ttk.Label(self.root, text="Upload Excel/CSV Files:", background="#f0f0f0").pack(pady=5)
        
        self.upload_button1 = ttk.Button(self.root, text="Upload File 1", command=self.upload_file1)
        self.upload_button1.pack(pady=5)
        
        self.file1_info = ttk.Label(self.root, text="No file uploaded", background="#f0f0f0")
        self.file1_info.pack(pady=5)

        self.upload_button2 = ttk.Button(self.root, text="Upload File 2", command=self.upload_file2)
        self.upload_button2.pack(pady=5)
        
        self.file2_info = ttk.Label(self.root, text="No file uploaded", background="#f0f0f0")
        self.file2_info.pack(pady=5)

        # Column Selection
        ttk.Label(self.root, text="Select Columns to Compare:", background="#f0f0f0").pack(pady=10)

        self.column1_combo = ttk.Combobox(self.root, state="disabled")
        self.column1_combo.pack(pady=5, fill=tk.X, padx=20)

        self.column2_combo = ttk.Combobox(self.root, state="disabled")
        self.column2_combo.pack(pady=5, fill=tk.X, padx=20)

        # Compare Button
        self.compare_button = ttk.Button(self.root, text="Compare Data", command=self.compare_data)
        self.compare_button.pack(pady=20)

    def upload_file1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file1 = file_path
            self.df1 = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            self.update_file_info()

    def upload_file2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file2 = file_path
            self.df2 = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            self.update_file_info()

    def update_file_info(self):
        if self.df1 is not None:
            file1_size = self.df1.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
            self.file1_info.config(text=f"File 1: {self.file1.split('/')[-1]} | Size: {file1_size:.2f} MB | Columns: {', '.join(self.df1.columns)}")

        if self.df2 is not None:
            file2_size = self.df2.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
            self.file2_info.config(text=f"File 2: {self.file2.split('/')[-1]} | Size: {file2_size:.2f} MB | Columns: {', '.join(self.df2.columns)}")
        
        if self.df1 is not None and self.df2 is not None:
            self.update_columns()

    def update_columns(self):
        columns1 = self.df1.columns.tolist()
        columns2 = self.df2.columns.tolist()

        self.column1_combo['values'] = columns1
        self.column2_combo['values'] = columns2

        self.column1_combo.state(["!disabled"])
        self.column2_combo.state(["!disabled"])

    def compare_data(self):
        # Check if the DataFrames are None (i.e., not uploaded)
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Warning", "Please upload both files first.")
            return

        column1 = self.column1_combo.get()
        column2 = self.column2_combo.get()

        # Check if columns are selected
        if not column1 or not column2:
            messagebox.showwarning("Warning", "Please select columns to compare.")
            return

        # Check if the selected columns exist in the DataFrames
        if column1 not in self.df1.columns or column2 not in self.df2.columns:
            messagebox.showerror("Error", "Selected columns are not present in the respective files.")
            return

        # Convert columns to string to ensure they are of the same type
        self.df1[column1] = self.df1[column1].astype(str)
        self.df2[column2] = self.df2[column2].astype(str)

        # Perform the comparison
        mismatches = self.df1[[column1]].merge(self.df2[[column2]], left_on=column1, right_on=column2, how='outer', indicator=True)
        mismatches = mismatches[mismatches['_merge'] != 'both']

        # Check if there are mismatches and handle the result
        if mismatches.empty:
            messagebox.showinfo("Result", "No mismatches found.")
        else:
            mismatches_file = "mismatches.xlsx"
            mismatches.to_excel(mismatches_file, index=False)
            messagebox.showinfo("Result", f"Mismatches found. Check '{mismatches_file}' for details.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DataComparerApp(root)
    root.mainloop()
