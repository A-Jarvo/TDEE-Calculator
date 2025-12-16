import tkinter as tk

def main():
    app = appGUI()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    del frame

class appGUI:
    def __init__(self):
        self.default_path = "data/sample_data.txt"

        self.root = tk.Tk()
        self.root.geometry("1500x1000")

        self.main_get_path()



    def main_get_path(self):
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

        self.root.mainloop()  

    def read_path(self, _):
        self.path = self.get_path_frame.path_entrypoint.get()

    def use_default_path(self):
        self.path = self.default_path

    def post_path(self):
        clear_frame(self.get_path_frame)
        try:
            self.path_label = tk.Label(self.root, text=self.path, font=("Arial, 50"))
        except AttributeError:
            print("no path was entered, using default")
        self.path_label = tk.Label(self.root, text=self.default_path, font=("Arial, 50"))
        self.path_label.pack()

    def print_path(self):
        print(self.path)

    

if __name__ == "__main__":
    main()