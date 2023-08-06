The Car Rental System is a command-line application that allows users to manage vehicles and customers for a car rental service. It provides functionality for adding, deleting, and searching for cars, as well as managing customer information and renting out cars. The system uses JSON files to store and retrieve data, and it supports both normal cars and electric cars.

Files:

main.py: This file is the entry point of the application. It imports the necessary functions from the menu.py file and contains the main loop that prompts the user for actions.

menu.py: This file contains the menu functions and ASCII art for the different menus. It also imports the database.py file and the necessary classes and functions from it. The menu functions handle user input and perform the corresponding actions based on the choices made.

database.py: This file contains the Database class, which is responsible for handling JSON file operations. It includes functions to load and save car and customer data from and to JSON files. The class also provides utility functions to manipulate car and customer data.

car.py: This file defines the Car and ElectricCar classes, which represent the car objects in the system. The Car class represents a normal car, while the ElectricCar class represents an electric car. Both classes have methods to get and set car attributes and convert car objects to dictionaries.

customer.py: This file defines the Customer class, which represents a customer object in the system. The class has methods to get and set customer attributes and manage the rented car for each customer.

Documentation Guide:

Installation:

Download all the Python files: main.py, menu.py, database.py, car.py, customer.py.
Make sure you have Python 3 installed on your system.
Usage:

Open a command-line terminal or IDE.
Navigate to the directory where the Python files are saved.
Run the command "python main.py" to start the Car Rental System.

Main Menu:

After running the program, you will see the main menu with options.
Enter "V" to access the vehicle management menu.
Enter "C" to access the customer management menu.
Enter "X" to close the program.
Vehicle Management Menu:

In the vehicle management menu, you can perform the following actions:
Enter "S" to show all cars.
Enter "A" to add a new car (normal car or electric car).
Enter "I" to search for a car by its ID.
Enter "D" to delete a car by its ID.
Enter "X" to return to the main menu.
Customer Management Menu:

In the customer management menu, you can perform the following actions:
Enter "S" to show all customers.
Enter "A" to add a new customer.
Enter "R" to rent out a car to a customer.
Enter "C" to check a car back in from a customer.
Enter "X" to return to the main menu.

https://www.babelfish.de/ was used for Translation to english

MIT License

Copyright (c) 2023 Yann Schüler

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.