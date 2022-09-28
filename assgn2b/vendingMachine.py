import re
import item
import moneyCounter


class ItemNotFound(Exception):
    pass


class VendingMachine:
    """
    Command Line Based Vending Machine

    The user can interact with the vending machine via the command line.
    This is done using a list of supported functions available via the self.help() function.
    To enter interact with the vending machine use the self.input() function

    This class has 4 attributes and 7 methods

    Attributes
    ----------
    * items:        A dictionary of items in the inventory keyed by the item's name
    * history_list: A list of successfully completed transaction commands as inputted by the user
    * mc:           An instance of the MoneyCounter class. This deals with most of the math involved in transactions
    * next_ID:      An int to be assigned as the unique ID number to the next item added to the inventory

    Methods
    -------
    input:
    _buy:
    _add:
    _inventory:
    help:
    _history:

    """

    def __init__(self):
        self.items = {}
        self.history_list = []
        self.mc = moneyCounter.MoneyCounter()
        self.next_ID = 0

    def input(self):
        """
        Continual loop that gets user input and checks it against valid commands,
         then executes those commands as appropriate
        """
        while True:
            usr_in = input('VendingMachine>')
            args = usr_in.split()
            if not args:
                continue

            match args[0]:
                case 'history':
                    self._history()
                case 'balance':
                    self.mc.print_balance()
                case 'inventory':
                    self._inventory()
                case 'add':
                    try:
                        #self._add(args, usr_in)
                        self._add(usr_in)
                    except ValueError as e:
                        print(e)
                        self.help()
                        continue
                case 'buy':
                    try:
                        self._buy(args, usr_in)
                    except (ItemNotFound, item.OutOfStock, moneyCounter.InsufficientFunds) as e:
                        print(e)
                        continue
                case 'help':
                    self.help()
                case 'exit':
                    break
                case _:
                    print(f'\'{usr_in}\' is not a valid command')
                    self.help()

    def _buy(self, usr_in: str):
        """
        Functionality for purchasing an item from the vending machine

        First checks for multi-word item name,
         then checks to see if item is in the inventory,
         finally completes the purchase via the money counter

        :param args: usr input string split into list of strings
        :param usr_in: raw string of user input
        """


        val_array = usr_in.rsplit(' ', 5) 
        item_name = val_array[0].replace("buy item", "").strip()
        dollars = int(val_array[1])
        quarters = float(val_array[2])
        dimes = float(val_array[3])
        nickels = float(val_array[4])
        pennies = float(val_array[5])
        the_money = list(val_array[1:6])


        i = self.items.get(item_name)
        if i is None:
            raise ItemNotFound(f'No item \'{item_name}\' found in inventory')
        self.mc.purchase(i.price, the_money)
        i.buy()
        self.history_list.append(usr_in)

    #def has_product(self, item_name):


    #def add_existing_item(self, item_name, quantity):



    def _add(self, val):
        """
        Adds a new item to the inventory or updates an existing item's stock

        First checks for multi-word item names
         Then checks if item is already in the inventory
         If not it is added by creating a new entry in the items dictionary
         If it is the properties of the item are updated

        :param args: usr input string split into list of strings
        :param usr_in: raw string of user input
        """

        #if val.startswith("add item"):
        val_array = val.rsplit(" ", 2)
        item_price = val_array[2]
        quantity = val_array[1]
        item_name = val_array[0].replace("add item", "").strip()
        try:
            if self.items.get(item_name) is None:
                self.items[item_name] = item.Item(self.next_ID, item_name, item_price, quantity)
                self.next_ID += 1
                print(f'Successfully added item {self.items[item_name]}')

            else:
                #self.add_existing_item(item_name, quantity)
                self.items[item_name].update_price(item_price)

                self.items[item_name].inventory += quantity
                self.items[item_name].price = item_price
                print(f'Successfully updated item {self.items[item_name]}')
       
        except IndexError:
            print('Invalid input')
        #else: #self.add_new_product(Product(item_name, quantity, item_price))
            

            self.history_list.append(val)





        """
        args[2] = re.findall('(?<=item)(.*?)(?=[0-9])', usr_in)[0].strip()
        for i in range(len(args[2].split()) - 1):
            args.pop(3 + i)
        try:
            if args[1] == 'item':
                if self.items.get(args[2]) is None:
                    self.items[args[2]] = item.Item(self.next_ID, args[2], args[4], args[3])
                    self.next_ID += 1
                    print(f'Successfully added item {self.items[args[2]]}')
                else:
                    self.items[args[2]].inventory += args[3]
                    self.items[args[2]].price = args[4]
                    print(f'Successfully updated item {self.items[args[2]]}')
                self.history_list.append(usr_in)
            else:
                raise IndexError
        except IndexError:
            print('Invalid input')
        """
        
    def _inventory(self):
        """
        Prints the inventory of the vending machine using the __str__ method of the item class

        Iterates of the self.items dictionary and prints items.
        Or indicates the inventory is empty if that is true
        """
        # print('Name(ID) #in stock, price')
        if self.items:
            for i in self.items:
                print(self.items[i])
        else:
            print('the inventory is empty')

    @staticmethod
    def help():
        print('''
Sample Commands

inventory all                   prints current inventory (name, id, price, count) of all vending machines
inventory <vending machine id>  prints current inventory (name, id, price, count) of selected vending machines
buy item <str> {5}<int>         immediately buy item with provided coins. -item name- - D Q D N P -
                       
help                            display this help message   
logout                          logout of vendor screen    
''')

    def _history(self):
        """Print a list of successful transactions completed during the session"""
        if self.history_list:
            for command in self.history_list:
                print(command)
        else:
            print('no transaction history')


