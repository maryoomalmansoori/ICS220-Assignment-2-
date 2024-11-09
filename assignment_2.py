import copy


# Class representing an e-book with attributes like title, author, publication date, genre, and price
class Ebook:
    def __init__(self, title, author, datePublished, bookGenre, price):
        self.title = title  # Title of the e-book
        self.author = author  # Author of the e-book
        self.datePublished = datePublished  # Date when the e-book was published
        self.bookGenre = bookGenre  # Genre of the e-book
        self._price = price  # Price of the e-book (private attribute)

    # Method to get the price of the e-book
    def price(self):
        return self._price

    # Method to apply a discount to the price of the e-book
    def apply_discount(self, discountRate):
        self._price *= (1 - discountRate)  # Reduces the price by the discount rate


# Class representing a customer who has an account and can manage a cart of items
class customer:
    def __init__(self, name, contacts, loyaltyMember=False):
        self.name = name  # Name of the customer
        self.contacts = contacts  # Contact information for the customer
        self.loyaltyMember = loyaltyMember  # Boolean flag indicating if the customer is a loyalty member
        self.account = account()  # Create an account for the customer


# Class representing a customer's account which has a cart and orders
class account:
    def __init__(self):
        self._cart = Cart()  # Initialize an empty cart for the account
        self._orders = []  # List to store all orders made by the customer

    # Method to add an e-book to the cart
    def addtoCart(self, ebook, quantity):
        self._cart.addItem(ebook, quantity)  # Add the given e-book to the cart

    # Method to checkout all items in the cart, creating an order
    def checkOut(self):
        # Make a copy of the items in the cart and pass to Order to avoid changes when clearing the cart
        order = Order(copy.deepcopy(self._cart._items))
        self._orders.append(order)  # Store the newly created order in the list of orders
        self._cart.clear()  # Clear the cart after checkout
        return order  # Return the order for further processing (e.g., for generating an invoice)


# Class representing a shopping cart where items (e-books) can be added, removed, or cleared
class Cart:
    def __init__(self):
        self._items = {}  # Dictionary to store e-books and their quantities

    # Method to add an e-book to the cart
    def addItem(self, ebook, quantity):
        if ebook in self._items:
            self._items[ebook] += quantity  # If the e-book is already in the cart, increase the quantity
        else:
            self._items[ebook] = quantity  # If the e-book is not in the cart, add it with the given quantity

    # Method to remove an e-book from the cart
    def removeItem(self, ebook):
        if ebook in self._items:
            del self._items[ebook]  # Remove the e-book from the cart if it exists

    # Method to clear all items from the cart
    def clear(self):
        """Clears all items in the cart."""
        self._items.clear()


# Class representing an order created after checkout, storing details of purchased items, their costs, and generating invoices
class Order:
    def __init__(self, items):
        self._ebooks = items  # Dictionary of e-books and their quantities (copied from the cart)
        self._subtotal = 0.0  # Subtotal of the order before tax and discounts
        self._discount = 0.0  # Discount applied to the order (if any)
        self._tax = 0.0  # Tax applied to the order
        self._totalPrice = 0.0  # Total price after adding tax and applying discount
        self.calculate_total()  # Calculate totals for the order

    # Method to calculate the subtotal, tax, and total price for the order
    def calculate_total(self):
        """Calculates the subtotal, tax, and total price for the order."""
        # Calculate the subtotal by summing price * quantity for each e-book
        self._subtotal = sum(ebook._price * quantity for ebook, quantity in self._ebooks.items())

        # Assuming an 8% tax rate
        self._tax = self._subtotal * 0.08
        self._totalPrice = self._subtotal + self._tax - self._discount

    # Method to generate a textual invoice detailing the items, subtotal, tax, and total price
    def generateInvoice(self):
        invoice_details = "Invoice:\n"
        for ebook, quantity in self._ebooks.items():
            # Add each e-book's details to the invoice
            invoice_details += f"Title: {ebook.title}, Author: {ebook.author} - Quantity: {quantity}, Price per item: ${ebook._price}\n"
        # Add subtotal, tax, and total price to the invoice
        invoice_details += f"Subtotal: ${self._subtotal:.2f}\n"
        invoice_details += f"Tax: ${self._tax:.2f}\n"
        invoice_details += f"Total Price: ${self._totalPrice:.2f}\n"
        return invoice_details  # Return the generated invoice as a string
