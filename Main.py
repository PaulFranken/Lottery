__author__ = 'PaulFranken'

import tkinter as tk
import re
import Lottery
import DatabaseFunctions


class Main(tk.Frame):
    def create_tickets_ui(self):
        self.drop_ui()
        self.title = tk.Label(self, text="Step right up, step right up! The Powerball is back in town!", wraplength=200)
        self.title.grid(row=0, column=0, columnspan=2)

        self.entry = tk.Entry(self, width=10, validate="focusout", validatecommand=self.check_name_db)
        self.entry.grid(row=1, column=1)

        self.entryError = tk.Label(self, text="This user is already playing, enter a different name")
        self.entryError.grid(row=1, column=2)
        self.entryError.grid_forget()

        self.entryLabel = tk.Label(self, text="Name: ")
        self.entryLabel.grid(row=1, column=0, sticky="W")

        self.spinbox = tk.Spinbox(self, from_=1, to=20, width=3)
        self.spinbox.grid(row=2, column=1)

        self.spinboxLabel = tk.Label(self, text="Number of tickets:")
        self.spinboxLabel.grid(row=2, column=0)

        self.button = tk.Button(self, text="Get Tickets!", command=self.get_numbers)
        self.button.grid(row=3, column=1, columnspan=2)

    def create_play_ui(self):
        self.drop_ui()
        self.userLabel = tk.Label(self, text="Play as:").grid(row=0, column=0)

        var1 = tk.StringVar()
        self.userEntry = tk.OptionMenu(self, var1, *self.database.get_players())
        self.userEntry.grid(row=0, column=1)

        self.playLottoButton = tk.Button(self, text="Play!", command=lambda: self.play_lotto(var1.get())).grid(row=1, column=0)



    def play_lotto(self, name):
        lottery = Lottery.Lottery(0)
        winningNumber = lottery.get_winning_number()
        #onnette manier om een bug te fixen
        regex = re.compile('[^a-zA-Z]')
        name = regex.sub('', name)
        numberList = lottery.play(name)
        labelList = []
        rowNumber = 3

        for entry in numberList:

            labelList.append(tk.Label(self, text=entry).grid(row=rowNumber, column=1))
            labelList.append(tk.Label(self, text=lottery.check_number(entry, winningNumber)).grid(row=rowNumber, column=2))
            rowNumber = rowNumber + 1


        self.userEntry.config(state="disabled")
        self.yourNumbersLabel = tk.Label(self, text="These are your numbers").grid(row = 1, column=1)
        self.winningNumberLabel = tk.Label(self, text="The winning number is:").grid(row=rowNumber + 1, column=0)
        self.winningNumber = tk.Label(self, text=winningNumber).grid(row=rowNumber + 1, column=1)
        self.playAgain = tk.Button(self, text="Play Again!", command=self.restart).grid(row=rowNumber + 2, column=1)


    def drop_ui(self):
        self.buttonPlay.grid_forget()
        self.buttonTickets.grid_forget()

    def get_numbers(self):
        lottery = Lottery.Lottery(int(self.spinbox.get()))
        name = self.entry.get()
        labelList = []
        rowNumber = 5
        for entry in lottery.listOfTickets:
            labelList.append(tk.Label(self, text=entry).grid(row=rowNumber, column=1))
            rowNumber = rowNumber + 1

        self.button.destroy()
        self.confirmLabel = tk.Label(self, text="Are you happy with these numbers?").grid(row=3, column=1)
        self.yesButton = tk.Button(self, text="Yes", command=lambda: self.save_numbers(name, lottery.listOfTickets, self.nameExists)).grid(row=4, column=1, sticky="W")
        self.noButton = tk.Button(self, text="Generate again", command=self.get_numbers).grid(row=4, column=1, sticky="E")

    #check if the name entered in self.entry already exists in the database
    def check_name_db(self):
        name = self.database.check_name(self.entry.get())
        if name == False:
            self.entry.config(bg="red")
            self.nameExists = True
            return False
        if name == True:
            self.entry.config(bg="White")
            self.nameExists = False
            return True

    def save_numbers(self, name, list, name_exist):
        self.database.save_to_db(name, list, name_exist)
        self.restart()

    def restart(self):
        self.grid_forget()
        self.__init__()

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.buttonTickets = tk.Button(self, text="Get Tickets!", command=self.create_tickets_ui)
        self.buttonTickets.grid(row=0, column=0)
        self.buttonPlay = tk.Button(self, text="Play!", command=self.create_play_ui)
        self.buttonPlay.grid(row=0, column=1)

        self.nameExists = False
        self.grid()

        self.database = DatabaseFunctions.DatabaseFunctions()

root = tk.Tk()
#root.geometry("300x500")
app = Main(master=root)
app.mainloop()









