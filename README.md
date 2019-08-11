# vending-machine
 
Programming Exercise: Vending Machine Exercise
Design a vending machine using Python. The vending machine should perform as follows:

Once an item is selected and the appropriate amount of money is inserted, the vending machine should return the correct product.
It should also return change if too much money is provided, or ask for more money if insufficient funds have been inserted.
The machine should take an initial load of products and change. The change will be of denominations 1p, 2p, 5p, 10p, 20p, 50p, £1, £2.
There should be a way of reloading either products or change at a later point.
The machine should keep track of the products and change that it contains.

###Project Installation Instructions:
For Windows 10:

1.Download Python version 3.7.4. from https://www.python.org/downloads/, makes sure you have the following modules installed: pandas, os, inspect, sqlite3, re, unittest.
2. Download vending-machine-1.0.tar.gz and extract the contents where you see fit.
3. In the Command Prompt, inside the project folder, run the following line: python -m .main Example: C:\Users\Alex\Python\vending-machine-1.0>python -m main

###Description:
The project is separated into 3 main parts:
1. The database, database_architect.py.
2. The Mediator, mediator.py.
3. The vendor, vending_machine.py.

1. The data base is implemented using sqlite3. It creates a .db file in the "database" folder of the project. It connects to an existing data base or it creates a data base at run time if a data base of name "vendor_data_base.db" is not present.
The data base is filled with tables that contain data from .csv files using pandas. These .csv files are item_list.csv and machine_funds.csv
The .csv files are in the following format:
item_list.csv			       || machine_funds.csv
item_id,item_name,item_cost,item_amount||currency_id,currency_name,amount_available
1,Green Tea,£0.79,8		       ||1,1p,10
2,Peach Tea,£0.79,10		       ||2,2p,9
3,Coke Can,£0.89,10		       ||5,5p,10
4,Fanta Can,£0.89,10		       ||10,10p,10
5,Sprite Can,£0.89,10		       ||20,20p,8
6,Secret Surprise,£200.00,1	       ||50,50p,10
7,Pizza,£24.99,5		       ||100,£1,10
8,1/2 Pizza,£15.99,10		       ||200,£2,10
9,1/4 Pizza,£8.99,20		       ||
10,Sandwich,£5.99,5		       ||

item_list table and machine_funds table are created using these files. If you want to change these files to create new data base data the column names need to stay the same, but row data can be changed with less constraints(e.g. maybe you wish to use different item id's or currency amounts)
If you wish to add your own data, you need to delete the data base manually, and replace the data in the "csv_files" folder for it to appear in the new database.
It is possible for the data base to reset to an initial state of the data, but this data represents a "clean" form of "item_list.csv" and "machine_funds.csv" present in the "backup_csv_files" folder. It is also possible to change the files in the backup folder.
One can check the .csv files in the "csv_files" folder to see how the data from "vendor_data_base.db" changes with each purchase.

2. Acts as a bridge between the vendor and the data base, while also stopping the user from accessing the data base directly. It's role is to take data from the data base and prepare it for vendor use. 
Also relays commands to the data base based on the actions of the vendor. These commands are: data update in tables, commits and closing.

3. Takes data from the mediator on which it functions. Depending on the state of the data the vendor does the following:
- it can select what items to display based on their availability
- allows for users to purchase multiple of the same item
- it knows the amount of money available in the machine, while also keeping track of money given by users
- calculates the amount of change users need to receive, based on available currency
- dynamically removes items from display if their quantity reaches 0
- returns users their money if there is an insufficient amount of currency to use as change
Pseudocode for change calculation:
Data: payment_difference(inserted_change - item_cost)
Result: list of different coin types, each with it's individual quantity
	
	for each currency_token in tokens_to_give_back:
		if available_currency_tokens > 0:
			number_of_tokens = payment_difference // currency_token_value # floor divison to get only the number of times this token can be used as change
			if number_of_tokens > available_currency_tokens:
				tokens_to_give_back[currency_token] = available_currency_token # only use the tokens we have available
			else:
				tokens_to_give_back[currency_token] = number_of_tokens # use the number of tokens from the calculation
			payment_difference = payment_difference - currency_token_value * number_of_tokens
	if payment_difference > 0:
		print "there are not enough tokens available in the machine go give back change"
		refund()
	else:
		give_change_to_customer()
		update_data_base()

This pseudocode can be found in a form that closely resembles it in vending_machine.py , function: "calculate_change_amount(self, payment_difference)".

Conclusions:
I am happy with how this test turned out, I hope those that will see this repository believe the same.
I don't think it was necessary to use sqlite3 databases for the project but for a more real world approach I believed it was best to tackle a new area, as Python is a versatile language allowing for SQL commands to be executed in code.
The most difficult part of the project was implementing the vending_machine, considering all the edge cases that could lead to faulty data base updates and user behaviour, e.g. one bug allowed for data base updates despite giving change back to the user, giving the user a freebie if we consider the real world counterpart.

Future Targets:
1. An alternative to creating a .db file and loading its contents from .csv would be to create a data base in memory. Sqlite3 allows for this, with sqlite3.connect(":memory:"), with tables being filled with data from pandas/dictionaries created beforehand in the code.
2. Implementation for adding data to the data base at runtime, by the user, exists but is not available to the user in the end version. For this to happen I would consider the creation of an "interface" that switches between the vending and database behaviour while in the Python console.
3. There were initial plans for the creation of a third table that would contain transaction history with data columns representing purchased item, amount, currency given, currency taken, currency before purchase and currency after purchase.
The role of this table would have been to fit in as the recovery set in case of data base failure.
4. A better implementation for reading user input when it comes to the vending machine in general, especially when asking the user to input the amount of change they would like to give, as it is a bit confusing at the moment.
5. Cleaner code, there are minor issues where I split dictionaries into currency_name, currency_item but still call self.currency_list[currency_name] instead of the item directly in order to avoid confusion between the different lists.
