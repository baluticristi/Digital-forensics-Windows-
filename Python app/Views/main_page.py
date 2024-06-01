# main_page.py

from tkinter import Tk, Button, Frame, PhotoImage, Label
import Views.static_analysis as StaticAnalysisPage

class MainPageView(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Digital Forensics Application")
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        logo_image = PhotoImage(file="Resources/logo.png")
        logo_image = logo_image.subsample(8, 8)
        logo_label = Label(self, image=logo_image)
        logo_label.image = logo_image
        logo_label.pack(pady=20)

        buttons_frame = Frame(self)
        buttons_frame.pack(pady=(20, 50))

        button_style = {"font": ("Arial", 12),
                        "bg": "#4CAF50",
                        "fg": "white",
                        "relief": "flat",
                        "bd": 2,
                        "width": 15,
                        "height": 2,
                        "borderwidth": 0,
                        "highlightthickness": 4,
                        "highlightbackground": "#2980b9",
                        "highlightcolor": "#2980b9",
                        "activebackground": "#16a085",
                        "activeforeground": "white",
                        "cursor": "hand2"
                        }

        self.static_analysis_button = Button(buttons_frame, text="Static Analysis", command=self.open_static_analysis, **button_style)
        self.static_analysis_button.grid(row=0, column=0, padx=10, pady=5)

        self.dynamic_analysis_button = Button(buttons_frame, text="Dynamic Analysis", command=self.open_dynamic_analysis, **button_style)
        self.dynamic_analysis_button.grid(row=1, column=0, padx=10, pady=20)

        self.report_history_button = Button(buttons_frame, text="Report History", command=self.open_report_history, **button_style)
        self.report_history_button.grid(row=2, column=0, padx=10, pady=5)


    def open_static_analysis(self):
        self.destroy()
        app = StaticAnalysisPage(self.master)

    def open_dynamic_analysis(self):
        pass

    def open_report_history(self):
        pass

# Example usage:
if __name__ == "__main__":
    root = Tk()
    main_page = MainPageView(master=root)
    root.mainloop()
