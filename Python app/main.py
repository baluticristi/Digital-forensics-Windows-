# main.py

from tkinter import Tk
from Views.main_page import MainPageView


def main():
    root = Tk()
    app = MainPageView(root)
    root.geometry(f"400x500")
    root.mainloop()

if __name__ == "__main__":
    main()
