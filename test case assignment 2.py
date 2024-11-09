import unittest
from assignment_2 import (Ebook, customer, account, Cart, Order)  # Import the necessary classes from assignment_2.py


class TestEBookStoreSystem(unittest.TestCase):
    """Test suite for the e-book store system."""

    def setUp(self):
        """Set up common test data for each test."""
        # Creating test e-books with title, author, publication date, genre, and price
        self.ebook1 = Ebook("Howl's moving castle", "Diana Wynne Jones", "1986-04-012", "Fantasy Fiction", 50.0)
        self.ebook2 = Ebook("Castle in the Air", "Diana Wynne Jones", "1990-05-15", "Fantasy Fiction", 60.0)

        # Creating a test customer with name, email, and loyalty membership status
        self.customer = customer("Maryam", "Almansoori@gmail.com", loyaltyMember=True)

    def test_ebook_discount(self):
        """Test that applying a discount correctly updates the e-book price."""
        original_price = self.ebook1._price
        discount_rate = 0.1  # 10% discount
        self.ebook1.apply_discount(discount_rate)

        expected_price = original_price * (1 - discount_rate)
        self.assertAlmostEqual(self.ebook1._price, expected_price, places=2)

    def test_customer_account_creation(self):
        """Test if a customer account is created correctly."""
        self.assertIsNotNone(self.customer.account)
        self.assertIsInstance(self.customer.account, account)

    def test_add_multiple_same_item_to_cart(self):
        """Test adding the same e-book multiple times to the cart."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 1)
        account.addtoCart(self.ebook1, 3)  # Add 3 more of the same e-book

        cart_items = account._cart._items
        self.assertEqual(cart_items[self.ebook1], 4)  # Total quantity should now be 4

    def test_remove_item_from_cart(self):
        """Test removing an e-book from the cart."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 2)  # Add 2 copies of ebook1 to the cart
        account._cart.removeItem(self.ebook1)  # Remove the e-book from the cart

        cart_items = account._cart._items
        self.assertNotIn(self.ebook1, cart_items)  # E-book should be removed from the cart

    def test_clear_cart_after_checkout(self):
        """Test if the cart is cleared after checkout."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 1)  # Add ebook1
        account.addtoCart(self.ebook2, 1)  # Add ebook2

        account.checkOut()  # Perform checkout
        cart_items = account._cart._items
        self.assertEqual(len(cart_items), 0)  # Cart should be empty after checkout

    def test_apply_discount_changes_price(self):
        """Test if apply_discount method changes the e-book price correctly."""
        original_price = self.ebook1._price
        self.ebook1.apply_discount(0.2)  # Apply a 20% discount
        self.assertEqual(self.ebook1._price, original_price * 0.8)  # Assert the price is updated correctly

    def test_order_calculate_total(self):
        """Test if the order calculates the total correctly based on the items."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 2)  # Add 2 copies of ebook1 to the cart
        order = account.checkOut()  # Perform checkout

        expected_total = self.ebook1._price * 2  # Expected subtotal for the order
        self.assertAlmostEqual(order._subtotal, expected_total, places=2)  # Assert the subtotal is correct

    def test_order_with_tax(self):
        """Test if tax is applied correctly in the order."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 1)  # Add 1 copy of ebook1
        order = account.checkOut()  # Perform checkout

        order.calculate_total()  # Calculate totals
        expected_tax = order._subtotal * 0.08  # Assuming an 8% tax rate
        self.assertAlmostEqual(order._tax, expected_tax, places=2)  # Assert that the calculated tax is correct

    def test_invoice_contains_correct_information(self):
        """Test if the generated invoice contains correct e-book and pricing information."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 1)  # Add 1 copy of ebook1 to the cart

        order = account.checkOut()  # Perform checkout
        invoice = order.generateInvoice()  # Generate the invoice

        # Check if the invoice contains the expected details
        self.assertIn("Title: Howl's moving castle", invoice)
        self.assertIn("Diana Wynne Jones", invoice)
        self.assertIn("Price per item: $50.0", invoice)

    def test_display_order_details(self):
        """Test to display order details with subtotal, tax, and total price."""
        account = self.customer.account
        account.addtoCart(self.ebook1, 2)  # Add 2 copies of ebook1
        account.addtoCart(self.ebook2, 1)  # Add 1 copy of ebook2

        order = account.checkOut()  # Perform checkout
        order.calculate_total()  # Calculate totals for the order

        # Display customer account details
        print("\n--- Customer Account Details ---")
        print(f"Name: {self.customer.name}")
        print(f"Contact: {self.customer.contacts}")

        # Display order details
        print("\n--- Order Details ---")
        print("Items Ordered:")
        for ebook, quantity in account._cart._items.items():
            print(
                f"  - Title: {ebook.title}, Author: {ebook.author}, "
                f"Quantity: {quantity}, Price per item: ${ebook._price}")

        # Display billing summary
        print("\n--- Billing Summary ---")
        print(f"Subtotal: ${order._subtotal:.2f}")
        print(f"Tax (8%): ${order._tax:.2f}")
        print(f"Total Price: ${order._totalPrice:.2f}")

        # Assertions to ensure calculations are correct
        self.assertGreater(order._subtotal, 0)  # Subtotal should be greater than zero
        self.assertGreater(order._totalPrice, order._subtotal)  # Total price should be greater than subtotal

if __name__ == '__main__':
    unittest.main()
