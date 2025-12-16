import tkinter as tk
from TDEE_calc import calculate_all_tdee
from ioutils import read_input, save_data
import pandas as pd
import datetime

def main() -> None:
    app = appGUI()

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

        for row in rows:
            index_cell = tk.Label(df_frame, text=str(index[row]))
            index_cell.grid(padx=10, pady=10, row=row+1, column=0)
            for col in cols:
                val = df.iloc[row, col]
                cell = tk.Label(df_frame, text=str(val))
                cell.grid(padx=10, pady=10, row=row+1, column=col+1)
        return df_frame

class appGUI:
    """
    uses tkinter
    has a master grid with frames for: header, body, and footer.
    body is cleared when screen changes, header and footer is not nessesarilly.
    currently header and footer is unused just there for completeness my learning.



    """
    def __init__(self) -> None:
        self.default_path = "data/sample_data.txt"

        self.root = tk.Tk()
        self.root.geometry("1500x1000")

        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0)
        self.primary_frame = tk.Frame(self.root)
        self.primary_frame.grid(row=1)
        self.footer_frame = tk.Frame(self.root)
        self.footer_frame.grid(row=2)

        self.main_get_path()

        self.root.mainloop()

    def clear_primary_frame(self) -> None:
        for widget in self.primary_frame.winfo_children():
            widget.destroy()

    def clear_header_frame(self) -> None:
        for widget in self.header_frame.winfo_children():
            widget.destroy()

    def clear_footer_frame(self) -> None:
        for widget in self.footer_frame.winfo_children():
            widget.destroy()

    def main_get_path(self) -> None:
        self.header_frame.welcome_label = tk.Label(self.header_frame, text="[Welcome Message]", font=("Arial", 25))
        self.header_frame.welcome_label.pack(pady=10)

        self.primary_frame.path_entrypoint = tk.Entry(self.primary_frame, text="Enter data path", )
        self.primary_frame.path_entrypoint.pack(padx=200, pady=30, fill="x")
        self.primary_frame.path_entrypoint.bind("<Return>", self.read_path)

        self.primary_frame.use_default_path_button = tk.Button(self.primary_frame, text="Use default path", command=self.use_default_path)
        self.primary_frame.use_default_path_button.pack()

        self.primary_frame.print_path_button = tk.Button(self.primary_frame, text="Print saved path", command=self.print_path)
        self.primary_frame.print_path_button.pack(pady=20)

        self.submit_button = tk.Button(self.primary_frame, text="next step", command=self.main_data_display)
        self.submit_button.pack()

    def read_path(self, _) -> None:
        self.path = self.primary_frame.path_entrypoint.get()

    def use_default_path(self) -> None:
        self.path = self.default_path
    
    def print_path(self) -> None:
        print(self.path)

    def main_data_display(self) -> None:
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
        
        self.clear_primary_frame()
        self.clear_header_frame()
        self.header_frame.path_label = tk.Label(self.header_frame, text=f"using path: {self.path}", font=("Arial, 50"))
        self.header_frame.path_label.pack()
        self.primary_frame_left = tk.Frame(self.primary_frame)
        self.primary_frame_left.grid(row=0, column=0)
        self.primary_frame_right = tk.Frame(self.primary_frame)
        self.primary_frame_right.grid(row=0, column=1)
    
        self.raw_df_frame_tk: tk.Frame = turn_dataframe_to_grid(self.primary_frame_left, self.raw_dataframe)
        self.raw_df_frame_tk.pack()

        self.add_data_frame = tk.Frame(self.primary_frame_right)
        self.add_data_frame.grid(row=0)
        self.calculate_tdee_frame = tk.Frame(self.primary_frame_right)
        self.calculate_tdee_frame.grid(row=1)
        self.edit_df_frame = tk.Frame(self.primary_frame_right)
        self.edit_df_frame.grid(row=2)

        self.add_data_button = tk.Button(self.add_data_frame, text="Add data")
        self.add_data_button.grid(row=0, columnspan=2)



        self.curr_tdee_strvar = tk.StringVar(value="Not yet calculated")
        self.calculate_tdee_button = tk.Button(self.calculate_tdee_frame, text="Calculate TDEE for today", command=self.calculate_tdee)
        self.calculate_tdee_button.grid(row=0)
        self.display_tdee = tk.Label(self.calculate_tdee_frame, textvariable=self.curr_tdee_strvar)
        self.display_tdee.grid(row=1)

        self.edit_df_checkbox = tk.Checkbutton(self.edit_df_frame, text="Edit data")
        self.edit_df_checkbox.grid(row=0)


    def calculate_tdee(self) -> None:
        energy_per_kg = 7700
        tdee_calc_window = datetime.timedelta(days=13)
        tdee_smoothing_factor = 0.1
        self.dataframe_with_tdee = calculate_all_tdee(self.raw_dataframe, energy_per_kg, tdee_calc_window, tdee_smoothing_factor)
        self.curr_tdee = self.dataframe_with_tdee["TDEE_Guess"].iloc[-1]
        self.curr_tdee_strvar.set(self.curr_tdee)
    

    

if __name__ == "__main__":
    main()