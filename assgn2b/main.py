#import re
#import item
#import moneyCounter
import random
import vendingMachine

class Manager:

    def __init__(self, vendingMachines):
        self.vendingMachines = vendingMachines


    def start(self):
        while True:
            usr_in = input('VendingMachine> Are you a \'customer\' or \'vendor\'? ')
            args = usr_in.split()
            if not args:
                continue
        
            match args[0]:
                case 'customer':
                    print("customer logging in") 
                    inx = random.randint(0,len(self.vendingMachines)-1)
                    while True:
                        #selects random vending machine based on simulated GPS location
                        cus_in = input('VendingMachine - Customer - ' + list(self.vendingMachines)[inx] + '> ')

                        args1 = cus_in.split()
                        if not args1:
                            continue
                        match args1[0]:
                            case 'buy':
                                print("buying stuff")
                                self._buy(list(self.vendingMachines)[inx], cus_in)
                                
                            case 'logout':
                                break
                            case _:
                                print(f'\'{usr_in}\' is not a valid command')
                                self.help('u')
                case 'vendor':
                    while True:
                        ven_in = input('VendingMachine - Vendor> ')
                        args1 = ven_in.split()
                        if not args1:
                            continue
                        match args1[0]:
                            case 'history':
                                try:
                                    self._history(args1[1])
                                except IndexError:
                                    self._history()
                            case 'balance':
                                try:
                                    self.balance(args1[1])
                                except IndexError:
                                    self.balance()
                            case 'inventory':
                                try:
                                    self._inventory(args1[1])
                                except IndexError:
                                    self._inventory()
                            case 'add':
                                try:
                                    self._add(ven_in)
                                except ValueError as e:
                                    print(e)
                                    self.help('v')
                                    continue
                            case 'help':
                                self.help('v')
                            case 'logout':
                                break
                            case _:
                                print(f'\'{usr_in}\' is not a valid command')
                                self.help('v')
                case _:
                    print("try again")

    #buy 
    def _buy(self, id, input):
        print("buy stuff")
        self.vendingMachines[id]._buy(input)


    def _history(self, vendingMachineID = "all"):
        try:
            print("here is your " + vendingMachineID)
            if(vendingMachineID == "all"):
                #loop through all and display
                for key in self.vendingMachines:
                    print("Vending Machine " + key)
                    self.vendingMachines[key]._history()
            else:
                self.vendingMachines[vendingMachineID]._history()
        except ValueError as e:
            print("improper input")

    def balance(self, vendingMachineID = 'all'):
        print("here's your balance")
        if(vendingMachineID == "all"):
            #loop through all and display
            for key in self.vendingMachines:
                print("Vending Machine " + key)
                self.vendingMachines[key].mc.print_balance()
        else:
            self.vendingMachines[vendingMachineID].mc.print_balance()

    def _inventory(self, vendingMachineID = "all"):

        print("here's your inventory")
        try:
            if(vendingMachineID == "all"):
                #loop through all and display
                for key in self.vendingMachines:
                    print("Vending Machine " + key)
                    self.vendingMachines[key]._inventory()
            else:
                self.vendingMachines[vendingMachineID]._inventory()
        except ValueError as e:
            print("improper input")

    #add item 1 chips 2 4   -   add item vendingMachineID itemname quantity price
    def _add(self, ven_in):
        val_array = ven_in.rsplit(" ", 2)
        item_price = val_array[2]
        quantity = val_array[1]
        y = val_array[0].replace("add item", "").strip()
        id = y.split(" ", 1)[0]
        item_name = y.split(" ", 1)[1]
        #new_args = args1.copy()
        #del new_args[2]
        if(id == "all"):
            for key in self.vendingMachines:
                print("Vending Machine " + key)
                self.vendingMachines[key]._add("add item " + item_name + " " + val_array[1] + " " + val_array[2])
        else:
            
            self.vendingMachines[id]._add("add item " + item_name + " " + val_array[1] + " " + val_array[2])

    def help(self, usr):
        print("here's your help")
        if(usr == 'c'):
            vendingMachine.VendingMachine.help()

        elif(usr == 'v'):
            print('Vendor Help Screen')
            """Display list of available commands to the user"""
            print('''
Sample Commands
balance all                     shows the balance of all vending machines
balance <vending machine id>    shows the balance of the selected vending machine

history all                     prints list of transactions of all vending machines
history <vending machine id>    pritnts list of transactions of selected vending machine

inventory all                   prints current inventory (name, id, price, count) of all vending machines
inventory <vending machine id>  prints current inventory (name, id, price, count) of selected vending machines
                        
add item <str> <str> <int> <float>    add item to inventory. -vending machine id or all- -item name- -quantity- -cost-
help                            display this help message   
logout                          logout of vendor screen    
''')



if __name__ == '__main__':
    vendingMachines = {
        "123": vendingMachine.VendingMachine(),
        "234": vendingMachine.VendingMachine(),
        "345": vendingMachine.VendingMachine()
    }


    manager = Manager(vendingMachines)
    manager.start()

    

    #vm = vendingMachine.VendingMachine()
    #vm.input()

