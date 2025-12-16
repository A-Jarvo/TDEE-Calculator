import tkinter as tk
from TDEE_calc import calculate_all_tdee
from ioutils import read_input, save_data
import pandas as pd

def main() -> None:
    app = appGUI()

def clear_frame(frame: tk.Frame) -> None:
    for widget in frame.winfo_children():
        widget.destroy()

def turn_dataframe_to_grid(root, df: pd.DataFrame) -> tk.Frame: 
        df_frame: tk.Frame = tk.Frame(root)
        cols: int = list(range(len(df.columns)))
        rows: int = list(range(len(df.index)))
        index = df.index
        column_names = df.columns
        column_names = [df.index.name, *column_names]
        for col_num, col in enumerate(column_names):
            col_cell = tk.Label(df_frame, text=str(col))
            col_cell.grid(padx=10, pady=10, row=0, column=col_num)

        for row in rows[1:]:
            index_cell = tk.Label(df_frame, text=str(index[row]))
            index_cell.grid(padx=10, pady=10, row=row, column=0)
            for col in cols:
                val = df.iloc[row, col]
                cell = tk.Label(df_frame, text=str(val))
                cell.grid(padx=10, pady=10, row=row, column=col+1)
        return df_frame

class appGUI:
    def __init__(self) -> None:
        self.default_path = "data/sample_data.txt"

        self.root = tk.Tk()
        self.root.geometry("1500x1000")

        self.main_get_path()

        self.root.mainloop()

    #def clear_frame(self) -> None:
    #    for widget in self.primary_frame.winfo.children():
    #        widget.destroy

    def main_get_path(self) -> None:
        self.get_path_frame = tk.Frame()
        self.get_path_frame.pack()
        self.get_path_frame.welcome_label = tk.Label(self.get_path_frame, text="[Welcome Message]", font=("Arial", 25))
        self.get_path_frame.welcome_label.pack(pady=10)

        self.get_path_frame.path_entrypoint = tk.Entry(self.get_path_frame, text="Enter data path", )
        self.get_path_frame.path_entrypoint.pack(padx=200, pady=30, fill="x")
        self.get_path_frame.path_entrypoint.bind("<Return>", self.read_path)

        self.get_path_frame.use_default_path_button = tk.Button(self.get_path_frame, text="Use default path", command=self.use_default_path)
        self.get_path_frame.use_default_path_button.pack()

        self.get_path_frame.print_path_button = tk.Button(self.get_path_frame, text="Print saved path", command=self.print_path)
        self.get_path_frame.print_path_button.pack(pady=20)

        self.submit_button = tk.Button(self.get_path_frame, text="next step", command=self.post_path)
        self.submit_button.pack()

    def read_path(self, _) -> None:
        self.path = self.get_path_frame.path_entrypoint.get()

    def use_default_path(self) -> None:
        self.path = self.default_path
    
    def print_path(self) -> None:
        print(self.path)

    def post_path(self) -> None:
        try:
            self.path
        except AttributeError:
            print("no path was entered, using default")
            self.path = self.default_path
        try: 
            self.raw_dataframe = read_input(self.path)
        except FileNotFoundError:
            self.failed_to_read_file_label = tk.Label(self.get_path_frame, text="Failed to read input file", font=("Arial", 50), fg="red")
            self.failed_to_read_file_label.pack()
            return
        
        clear_frame(self.get_path_frame)
        self.path_label = tk.Label(self.root, text=self.path, font=("Arial, 50"))
        self.path_label.pack()
        self.raw_df_frame_tk: tk.Frame = turn_dataframe_to_grid(self.root, self.raw_dataframe)
        self.raw_df_frame_tk.pack()
    
    

    

if __name__ == "__main__":
    main()