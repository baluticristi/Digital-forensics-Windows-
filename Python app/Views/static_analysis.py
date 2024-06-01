from tkinter import Tk, Button, Frame, Label, Checkbutton, StringVar, IntVar

class StaticAnalysisPage(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Static Analysis")
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        # Top buttons
        top_frame = Frame(self)
        top_frame.pack(pady=10)

        import_button = Button(top_frame, text="Import Image", command=self.import_image)
        import_button.grid(row=0, column=0, padx=10)

        create_button = Button(top_frame, text="Create Image", command=self.create_image)
        create_button.grid(row=0, column=1, padx=10)

        # Label for "No image selected"
        self.no_image_label = Label(self, text="No image selected", font=("Arial", 12))
        self.no_image_label.pack(pady=10)

        # Static Analysis options
        options_frame = Frame(self)
        options_frame.pack(pady=10)

        self.option1_var = IntVar(value=0)
        option1_checkbox = Checkbutton(options_frame, text="Static Analysis Option 1", variable=self.option1_var)
        option1_checkbox.grid(row=0, column=0, padx=10, sticky="w")

        self.option2_var = IntVar(value=0)
        option2_checkbox = Checkbutton(options_frame, text="Static Analysis Option 2", variable=self.option2_var)
        option2_checkbox.grid(row=1, column=0, padx=10, sticky="w")

        self.option3_var = IntVar(value=0)
        option3_checkbox = Checkbutton(options_frame, text="Static Analysis Option 3", variable=self.option3_var)
        option3_checkbox.grid(row=2, column=0, padx=10, sticky="w")

        self.option4_var = IntVar(value=0)
        option4_checkbox = Checkbutton(options_frame, text="Static Analysis Option 4", variable=self.option4_var)
        option4_checkbox.grid(row=3, column=0, padx=10, sticky="w")

        # Start analysis button
        start_button = Button(self, text="Start Analysis", command=self.start_analysis)
        start_button.pack(pady=20)

    def import_image(self):
        print("Import Image")

    def create_image(self):
        print("Create Image")

    def start_analysis(self):
        print("Start Analysis")

if __name__ == "__main__":
    root = Tk()
    static_analasys = StaticAnalysisPage(master=root)
    root.mainloop()
