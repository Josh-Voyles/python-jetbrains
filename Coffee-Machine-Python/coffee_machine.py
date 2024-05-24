"""
Jet Brains Academy Coffee Machine Simulator
Code by: Josh Voyles
Python 3.9
22 Jan 24

Note: The project does not call for error checking.
"""
import sys
import textwrap
from enum import Enum


class MachineStatus(Enum):
    """
    Enum for handling coffee machine status
    """
    START = 0
    PARSE = 'parse'
    BUY = 'buy'
    FILL = 'fill'
    TAKE = 'take'
    BACK = 'back'
    REMAINING = 'remaining'
    EXIT = 'exit'
    WATER = 'water'
    MILK = 'milk'
    BEANS = 'beans'
    CUPS = 'cups'


class CoffeeMachine:
    """
    This class represents a coffee maker.
    You can buy one of three coffees, fill the machine, take money,
    check inventory,
    or exit
    """
    #  requirements for each of the coffee types (beans, water, milk, cups,
    #  cost)
    ESPRESSO_REQUIREMENTS = [16, 250, 0, 1, -4]
    LATTE_REQUIREMENTS = [20, 350, 75, 1, -7]
    CAPPUCCINO_REQUIREMENTS = [12, 200, 100, 1, -6]
    coffee_beans: int
    water: int
    milk: int
    cups: int
    money: int
    machine_resources: list
    state: Enum

    def __init__(self, water, milk, coffee_beans, cups, money) -> None:
        """
        Construct the initial state of the coffee machine

        :param water: amount in ml
        :param milk: amount in ml
        :param coffee_beans: amount in grams
        :param cups: quantity of cups
        :param money: quantity of money
        """
        self.machine_resources = [coffee_beans, water, milk, cups, money]
        self.state = MachineStatus(0)  # initial state machine

    def main_menu(self) -> str:
        """
        Main menu
        :return: string
        """
        return '\nWrite action (buy, fill, take, remaining, exit):'

    def run(self, user_input) -> str:
        """
        Main system menu
        :return: string version of menu
        """
        if self.state == MachineStatus.START:
            self.state = MachineStatus('parse')
            return self.main_menu()
        return self.parse_state(user_input)

    def parse_state(self, user_input) -> str:
        """
        Parses main menu and initiates further actions

        :param user_input: various inputs based on state
        :return: string notification of options selected by user
        """
        if self.state == MachineStatus.PARSE:
            if user_input in ['buy', 'fill', 'take', 'remaining', 'exit']:
                self.state = MachineStatus(user_input)
                if self.state == MachineStatus.BUY:
                    return ('What do you want to buy? 1 - espresso, '
                            '2 - latte, 3 - cappuccino, back - to main menu:')
                if self.state == MachineStatus.FILL:
                    self.state = MachineStatus('water')
                    return 'Write how many ml of water you want to add:'
                if self.state == MachineStatus.TAKE:
                    self.state = MachineStatus('parse')
                    return self.take() + "\n" + self.main_menu()
                if self.state == MachineStatus.REMAINING:
                    self.state = MachineStatus('parse')
                    return str(self) + "\n" + self.main_menu()
                if self.state == MachineStatus.EXIT:
                    sys.exit()
        return self.process_selection(user_input)

    def process_selection(self, user_input) -> str:
        """
        Further process the selections of the user
        :param user_input:
        :return: string notification of options selected by the user
        """
        if self.state == MachineStatus.BUY:
            if user_input in ['1', '2', '3']:
                self.state = MachineStatus('parse')
                return self.buy_coffee(user_input) + '\n' + self.main_menu()
            self.state = MachineStatus('parse')
            return self.main_menu()
        if self.state == MachineStatus.WATER:
            self.fill(int(user_input))
            self.state = MachineStatus('milk')
            return 'Write how many ml of milk you want to add:'
        if self.state == MachineStatus.MILK:
            self.fill(int(user_input))
            self.state = MachineStatus('beans')
            return 'Write how many grams of coffee beans you want to add:'
        if self.state == MachineStatus.BEANS:
            self.fill(int(user_input))
            self.state = MachineStatus('cups')
            return 'Write how many disposable cups you want to add:'
        if self.state == MachineStatus.CUPS:
            self.fill(int(user_input))
            self.state = MachineStatus('parse')
            return self.main_menu()
        return 'Not a valid selection'

    def buy_coffee(self, selection) -> str:
        """
        Triggers coffee to be processed
        :param selection: users option
        :return: string from completed process
        """
        if selection == '1':
            self.state = MachineStatus('parse')
            return self.process_coffee(self.ESPRESSO_REQUIREMENTS)
        if selection == '2':
            self.state = MachineStatus('parse')
            return self.process_coffee(self.LATTE_REQUIREMENTS)
        if selection == '3':
            self.state = MachineStatus('parse')
            return self.process_coffee(self.CAPPUCCINO_REQUIREMENTS)
        self.state = MachineStatus('parse')
        return ''

    def fill(self, amount) -> None:
        """
        Fills correct machine resource according to the state
        :return:
        """
        if self.state == MachineStatus.WATER:
            self.machine_resources[1] += amount
        elif self.state == MachineStatus.MILK:
            self.machine_resources[2] += amount
        elif self.state == MachineStatus.BEANS:
            self.machine_resources[0] += amount
        elif self.state == MachineStatus.CUPS:
            self.machine_resources[3] += amount

    def take(self) -> str:
        """
        Simulated action of removing money from the machine
        :return: string noting amount taken
        """
        amount = self.machine_resources[-1]
        self.machine_resources[-1] = 0
        return f'I gave you ${amount}'

    def process_coffee(self, requirements) -> str:
        """
        Checks machine resources and subtracts amounts
        based on coffee chosen
        or
        alerts user to which resource is low
        :param requirements: selected coffee requirements
        :return: friendly message with success or failure message
        """
        if (self.machine_resources[0] >= requirements[0]
                and
                self.machine_resources[1] >= requirements[1]
                and
                self.machine_resources[2] >= requirements[2]
                and
                self.machine_resources[3] >= requirements[3]):

            for count, req in enumerate(requirements):
                self.machine_resources[count] -= req

            return 'I have enough resources, making you a coffee!'

        low_amount = 'beans' if (self.machine_resources[0] <
                                 requirements[0]) \
            else 'water' if self.machine_resources[1] < requirements[1] \
            else 'milk' if self.machine_resources[2] < requirements[2] \
            else 'cups'
        return f'Sorry, not enough {low_amount}!'

    def __str__(self) -> str:
        """
        String representation of the machine resources
        :return: string
        """
        return textwrap.dedent(f'''
        The coffee machine has:
        {self.machine_resources[1]} ml of water
        {self.machine_resources[2]} ml of milk
        {self.machine_resources[0]} g of coffee beans
        {self.machine_resources[3]} disposable cups
        ${self.machine_resources[4]} of money''')


def main() -> None:
    """
    Main method to run the coffee machine
    :return: None
    """
    coffee_machine = CoffeeMachine(400, 540, 120, 9, 550)

    user_input = ''
    # coffee machine run loop till exit
    while True:
        print(coffee_machine.run(user_input))
        user_input = input()


if __name__ == '__main__':
    main()
