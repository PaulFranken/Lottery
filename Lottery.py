__author__ = 'PaulFranken'

import random
import DatabaseFunctions
# Lottery follows the US Powerball rules.
# 5 numbers between 1 and 59 are chosen with the 6th number a
# "red ball" with a number between 1 and 35
# if multiple people have the same ticket numbers the prize gets shared
class Lottery():
    def generate_tickets(self):
        tickets = []
        # generate as many tickets as specified
        for i in range (0, self.number):
            ticket = []
            # generate the first 5 numbers of the ticket
            for x in range(0, 5):
                ticketNumber = random.randrange(1, 59)
                ticket.append(ticketNumber)
            # append a the "red ball" number to the ticket
            ticket.append(random.randrange(1, 35))
            tickets.append(ticket)

        return tickets

    def play(self, name):
        database = DatabaseFunctions.DatabaseFunctions()
        numberList = database.get_numbers(name)
        return numberList

    def get_winning_number(self):
        ticket = []
        for x in range(0,5):
            number = random.randrange(1, 59)
            ticket.append(number)
        ticket.append(random.randrange(1, 35))

        return ticket

    def check_number(self, entry, winning_number):
        points = 0
        redball = 0
        # The order of the numbers does not matter so each entry of the winning number needs to be compared
        # to the entire ticket of the user

        for x in range(0, 5):
            for y in range(0,5):
                if winning_number[x] == entry[y]:
                    points = points + 1
        if winning_number[5] == entry[5]:
            redball = redball + 1

        if redball == 0:
            result = str(points) + " numbers match without a matching redball"
        else:
            result = str(points) + " numbers match but the redball matches!"

        return result

    def __init__(self, number):
        self.number = number
        if number != 0:
            self.listOfTickets = self.generate_tickets()
