import re

class Vending_Machine:
    products = {}
    balance = 0
    transactions = []
    def __init__(self):
        self.products = {}
    
    def get_balance(self):
        return self.balance

    def get_transactions(self):
        print(f'{ "Action" :<7} { "Item Name" :<25} { "Quantity":<15} { "Price" :<15} ')

        for row in self.transactions:
            print("{: <7} {: <25} {: <15} {: <15}".format(*row))
        print("\n")

    def get_inventory(self):
        print("\n")
        print(f'{ "ID" :<20} { "Item Name" :<25} { "Quantity":<15} { "Price" :<15} ')
        for i in self.products:
            self.products[i].display()
        print("\n\n")

    def dispense(self, item_name, money):
        if self.products[item_name].quantity > 0:
            self.products[item_name].quantity -= 1
            if money >= float(self.products[item_name].item_price.replace("$","")):
                print("dispensing\n")
                change = money - float(self.products[item_name].item_price.replace("$",""))
                self.balance += float(self.products[item_name].item_price.replace("$",""))
                self.transactions.append(["buy", item_name, "1", item_price])
                if self.products[item_name].quantity == 0:
                    self.products.pop(item_name)
                return change
            else:
                #insufficient funds deposited
                return -2
        else:
            #item not in machine
            return -1

    def has_product(self, item_name):

        if item_name in self.products.keys():
            return True
        return False

    def add_existing_item(self, item_name, quantity):
        self.products[item_name].quantity += int(quantity)
        self.transactions.append(["Add", item_name, quantity, item_price])


    def add_new_product(self, product):
        self.products[product.item_name] = product
        self.transactions.append(["Add", item_name, product.quantity, item_price])


    
class Product:
    def __init__(self, name, quantity, price):
        self.quantity = int(quantity)
        self.item_price = price
        self.item_name = name
        self.id = ''.join(list(map(str,map(ord,name))))[0:12]

    def update_price(self, price):
        self.item_price = price

    def display(self):
        print(f'{self.id :<20} {self.item_name :<25} {self.quantity :<15} {self.item_price :<15}')
    
val = ""


vending_machine = Vending_Machine()
#add item chips 20 $.50
while val := input("Welcome to the cool vending machine\n"):
    if val == "exit":
        break;

    #reduce multiple spaces to 1 space between words
    val = re.sub(' +', ' ', val)

    #add item <str> <int> <float>
    #add item chips 2 $1.00
    if val.startswith("add item"):
        val_array = val.rsplit(" ", 2)
        item_price = val_array[2]
        quantity = val_array[1]
        item_name = val_array[0].replace("add item", "").strip()
        if vending_machine.has_product(item_name):
            vending_machine.add_existing_item(item_name, quantity)
            vending_machine.products[item_name].update_price(item_price)
        else: vending_machine.add_new_product(Product(item_name, quantity, item_price))




    #buy item <str> {5}<int>
    #buy item chips 1 2 2 4 3
    elif val.startswith("buy item"):
        val_array = val.rsplit(' ', 5) 
        item_name = val_array[0].replace("buy item", "").strip()
        dollars = int(val_array[1])
        quarters = float(val_array[2])
        dimes = float(val_array[3])
        nickels = float(val_array[4])
        pennies = float(val_array[5])
        print(dollars)
        print(quarters*.25)
        print(dimes*.1)
        print(nickels*.05)
        print(pennies*.01)
        total_amount_deposited = dollars + (quarters*.25) + (dimes*.1) + (nickels * .05) + (pennies * .01)
        print(total_amount_deposited)

        if vending_machine.has_product(item_name):
            change = vending_machine.dispense(item_name, total_amount_deposited)
            if change == -2:
                print("Insufficient funds deposited. Here's your money back")
            elif change > -1:
                print("Thank you. Your change is: " + "{:.2f}".format(change))     
            else:
                #will never get here because it's tested in has_product
                print("product not available")
        else:
            print("product not available")

    elif val.startswith("history"):
        print("Here's your history")
        vending_machine.get_transactions()
    elif val.startswith("inventory"):
        print("Here's your inventory")
        vending_machine.get_inventory()
    elif val.startswith("help"):
        print("Here's your help")
        f = open("help.txt", "r")
        f_arr = f.read().split("*col*")
        for inx in range(0,len(f_arr)-3,3):
            f_arr[inx] = f_arr[inx].replace('\n','')
            f_arr[inx] = re.sub(r"[\n\t]*", "", f_arr[inx])
            f_arr[inx+1] = re.sub(r"[\n\t]*", "", f_arr[inx+1])
            f_arr[inx+2] = re.sub(r"[\n\t]*", "", f_arr[inx+2])
            
            for cool_variable in range(0,3):
                if(len(f_arr[inx+cool_variable]) > 30):
                    for inx1 in range(0,len(f_arr[inx+cool_variable])-1):
                        if(inx1%30 == 0):
                            if(len(f_arr[inx+cool_variable][inx1+(2*inx1)+30:]) > 0):
                                f_arr[inx+cool_variable] = f_arr[inx+cool_variable][:inx1+(2*inx1)+30] + "\n" + (' ' * (cool_variable*30+3)) + f_arr[inx+cool_variable][inx1+(2*inx1)+30:]
                            else:
                                f_arr[inx+cool_variable] = f_arr[inx+cool_variable][:inx1+(2*inx1)+30]


                       
            print("{: <30} {: <30} {: <40}".format(*[f_arr[inx], f_arr[inx+1], f_arr[inx+2]]))

    elif val.startswith("balance"):
        print("Here's your balance")
        print ("$" + "{:.2f}".format(vending_machine.get_balance()))
