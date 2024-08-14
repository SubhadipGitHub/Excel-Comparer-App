import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import tkinter.font as tkFont

class DataComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Comparer Application")
        self.root.geometry("1200x800")  # Set initial size
        self.root.state('zoomed')  # Start full-screen
        self.root.configure(bg="#f8f9fa")  # Light background color

        self.file1 = None
        self.file2 = None
        self.df1 = None
        self.df2 = None

        self.selected_columns1 = []
        self.selected_columns2 = []

        self.create_widgets()

    def create_widgets(self):
        # Load and resize logo
        self.logo_img = Image.open("logo.png")  # Ensure you have a logo.png file in the working directory
        self.logo_img = self.logo_img.resize((80, 80), Image.LANCZOS)  # Resize the logo
        self.logo = ImageTk.PhotoImage(self.logo_img)
        
        # Header Frame
        header_frame = ttk.Frame(self.root, padding="10", style="Header.TFrame")
        header_frame.pack(fill=tk.X)
        
        # Header Layout
        header_layout = ttk.Frame(header_frame, padding="10", style="HeaderLayout.TFrame")
        header_layout.pack(fill=tk.X, expand=True)

        # Logo and Title
        ttk.Label(header_layout, image=self.logo, background="#f8f9fa").pack(side=tk.LEFT, padx=10)
        
        title_font = tkFont.Font(family="Helvetica", size=16, weight="bold")
        ttk.Label(header_layout, text="Data Comparer Application", font=title_font, background="#f8f9fa").pack(side=tk.LEFT, padx=10)

        # Help Text
        help_text = (
            "1. Upload two files for comparison.\n"
            "2. Select columns from each file.\n"
            "3. Ensure an equal number of columns are selected for comparison.\n"
            "4. Click 'Compare Data' to see the mismatches."
        )
        ttk.Label(self.root, text=help_text, background="#f8f9fa", font=("Arial", 10)).pack(pady=10, padx=20, anchor="w")

        # File Upload and Column Selection Section
        file_frame = ttk.Frame(self.root, padding="10", style="FileFrame.TFrame")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # Grid Layout
        file_frame.grid_columnconfigure(0, weight=2)
        file_frame.grid_columnconfigure(1, weight=1)
        file_frame.grid_columnconfigure(2, weight=2)  # Column for buttons
        file_frame.grid_rowconfigure(0, weight=1)

        # File 1 Section
        file1_frame = ttk.Frame(file_frame, padding="10", style="File1.TFrame")
        file1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(file1_frame, text="Upload File 1", background="#f8f9fa").pack(pady=5)
        self.upload_button1 = ttk.Button(file1_frame, text="Upload File 1", command=self.upload_file1)
        self.upload_button1.pack(pady=5)

        self.file1_info = ttk.Label(file1_frame, text="No file uploaded", background="#f8f9fa")
        self.file1_info.pack(pady=5)

        self.column1_label = ttk.Label(file1_frame, text="File 1 Columns:", background="#f8f9fa")
        self.column1_label.pack(pady=5)
        self.column1_listbox = tk.Listbox(file1_frame, selectmode=tk.MULTIPLE, height=10)
        self.column1_listbox.pack(pady=5, fill=tk.X)

        self.select_columns1_button = ttk.Button(file1_frame, text="Select Columns from File 1", command=self.update_selected_columns1)
        self.select_columns1_button.pack(pady=5)

        self.selected_columns1_label = ttk.Label(file1_frame, text="Selected Columns from File 1:", background="#f8f9fa")
        self.selected_columns1_label.pack(pady=5)
        self.selected_columns1_display = ttk.Label(file1_frame, text="", background="#f8f9fa")
        self.selected_columns1_display.pack(pady=5)

        # Button Section
        button_frame = ttk.Frame(file_frame, padding="10", style="ButtonFrame.TFrame")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Reset Button with Image
        self.reset_img = Image.open("reset.png")  # Ensure you have a reset.png file in the working directory
        self.reset_img = self.reset_img.resize((40, 40), Image.LANCZOS)  # Resize the reset image using Image.LANCZOS
        self.reset_img = ImageTk.PhotoImage(self.reset_img)
        self.reset_button = ttk.Button(button_frame, image=self.reset_img, command=self.reset, style='TButton')
        self.reset_button.pack(pady=10)

        # Compare Button
        self.compare_button = ttk.Button(button_frame, text="Compare Data", command=self.compare_data)
        self.compare_button.pack(pady=150)
        

        # File 2 Section
        file2_frame = ttk.Frame(file_frame, padding="10", style="File2.TFrame")
        file2_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ttk.Label(file2_frame, text="Upload File 2", background="#f8f9fa").pack(pady=5)
        self.upload_button2 = ttk.Button(file2_frame, text="Upload File 2", command=self.upload_file2)
        self.upload_button2.pack(pady=5)

        self.file2_info = ttk.Label(file2_frame, text="No file uploaded", background="#f8f9fa")
        self.file2_info.pack(pady=5)

        self.column2_label = ttk.Label(file2_frame, text="File 2 Columns:", background="#f8f9fa")
        self.column2_label.pack(pady=5)
        self.column2_listbox = tk.Listbox(file2_frame, selectmode=tk.MULTIPLE, height=10)
        self.column2_listbox.pack(pady=5, fill=tk.X)

        self.select_columns2_button = ttk.Button(file2_frame, text="Select Columns from File 2", command=self.update_selected_columns2)
        self.select_columns2_button.pack(pady=5)

        self.selected_columns2_label = ttk.Label(file2_frame, text="Selected Columns from File 2:", background="#f8f9fa")
        self.selected_columns2_label.pack(pady=5)
        self.selected_columns2_display = ttk.Label(file2_frame, text="", background="#f8f9fa")
        self.selected_columns2_display.pack(pady=5)

    def upload_file1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file1 = file_path
            self.df1 = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            self.update_file_info()
            self.update_column_listbox(self.df1, self.column1_listbox)
            self.upload_button1.config(state=tk.DISABLED)  # Disable the upload button after the file is uploaded

    def upload_file2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if file_path:
            self.file2 = file_path
            self.df2 = pd.read_excel(file_path) if file_path.endswith('.xlsx') else pd.read_csv(file_path)
            self.update_file_info()
            self.update_column_listbox(self.df2, self.column2_listbox)
            self.upload_button2.config(state=tk.DISABLED)  # Disable the upload button after the file is uploaded

    def update_file_info(self):
        if self.df1 is not None:
            file1_size = self.df1.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
            self.file1_info.config(text=f"File 1: {self.file1.split('/')[-1]} | Size: {file1_size:.2f} MB | Rows: {len(self.df1)} | Columns: {len(self.df1.columns)}")

        if self.df2 is not None:
            file2_size = self.df2.memory_usage(deep=True).sum() / (1024 * 1024)  # Size in MB
            self.file2_info.config(text=f"File 2: {self.file2.split('/')[-1]} | Size: {file2_size:.2f} MB | Rows: {len(self.df2)} | Columns: {len(self.df2.columns)}")

    def update_column_listbox(self, df, listbox):
        listbox.delete(0, tk.END)
        for column in df.columns:
            listbox.insert(tk.END, column)

    def update_selected_columns1(self):
        self.selected_columns1 = [self.column1_listbox.get(i) for i in self.column1_listbox.curselection()]
        self.selected_columns1_display.config(text=", ".join(self.selected_columns1))

    def update_selected_columns2(self):
        self.selected_columns2 = [self.column2_listbox.get(i) for i in self.column2_listbox.curselection()]
        self.selected_columns2_display.config(text=", ".join(self.selected_columns2))

    def compare_data(self):
        # Check if the DataFrames are None (i.e., not uploaded)
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Warning", "Please upload both files first.")
            return

        # Check if columns are selected
        if not hasattr(self, 'selected_columns1') or not hasattr(self, 'selected_columns2') or (not self.selected_columns1) or (not self.selected_columns2):
            messagebox.showwarning("Warning", "Please select columns from both files.")
            return
        
        # Check if same number of columns are there in both files
        if len(self.df1.columns) != len(self.df2.columns):
            messagebox.showwarning("Warning", f"Files being compared have mismatch in number of columns. File 1 has {len(self.df1.columns)} columns and File 2 has {len(self.df2.columns)} columns")
            return

        # Ensure that the number of selected columns is equal
        if len(self.selected_columns1) != len(self.selected_columns2):
            messagebox.showwarning("Warning", "Please select an equal number of columns from both files.")
            return

        # Ensure that all selected columns exist in the DataFrames
        if any(col not in self.df1.columns for col in self.selected_columns1) or any(col not in self.df2.columns for col in self.selected_columns2):
            messagebox.showerror("Error", "Selected columns are not present in the respective files.")
            return

        # Convert columns to string to ensure they are of the same type
        for column in self.selected_columns1:
            self.df1[column] = self.df1[column].astype(str)
        for column in self.selected_columns2:
            self.df2[column] = self.df2[column].astype(str)

        # Perform the comparison for each selected column pair
        mismatches = pd.DataFrame()
        for column1 in self.selected_columns1:
            for column2 in self.selected_columns2:
                # Merge dataframes to find mismatches
                temp_mismatches = self.df1[[column1]].merge(self.df2[[column2]], left_on=column1, right_on=column2, how='outer', indicator=True)
                temp_mismatches = temp_mismatches[temp_mismatches['_merge'] != 'both']
                
                # Append additional columns to the mismatch dataframe
                if not temp_mismatches.empty:
                    temp_mismatches['File1_Column'] = column1
                    temp_mismatches['File2_Column'] = column2
                    mismatches = pd.concat([mismatches, temp_mismatches], ignore_index=True)

        # Check if there are mismatches and handle the result
        if mismatches.empty:
            messagebox.showinfo("Result", "No mismatches found.")
        else:
            mismatches_file = "mismatches.xlsx"
            mismatches.to_excel(mismatches_file, index=False)
            messagebox.showinfo("Result", f"Mismatches found. Check '{mismatches_file}' for details.")

    def reset(self):
        # Clear all file details and selections
        self.file1 = None
        self.file2 = None
        self.df1 = None
        self.df2 = None

        # Update file information labels
        self.file1_info.config(text="No file uploaded")
        self.file2_info.config(text="No file uploaded")

        # Clear column listboxes
        self.column1_listbox.delete(0, tk.END)
        self.column2_listbox.delete(0, tk.END)

        # Clear selected columns display
        self.selected_columns1_display.config(text="")
        self.selected_columns2_display.config(text="")

        # Reset file upload buttons
        self.upload_button1.config(text="Upload File 1")
        self.upload_button2.config(text="Upload File 2")

        # Reset file upload buttons
        self.upload_button1.config(text="Upload File 1", state=tk.NORMAL)
        self.upload_button2.config(text="Upload File 2", state=tk.NORMAL)

        # Reset selected columns
        self.selected_columns1 = []
        self.selected_columns2 = []

        # Optionally reset any additional UI components related to file comparison results


if __name__ == "__main__":
    root = tk.Tk()
    app = DataComparerApp(root)
    root.mainloop()
