import json
import os

class FoodOrderingSystem:
    def __init__(self):
        self.menu = {
            "pizza": 250,
            "burger": 129,
            "pasta": 180,
            "cold drink": 50
        }

        self.cart = {}
        self.order_file = "orders.json"
        self.user_type = None

    # ================= LOGIN =================

    def login(self):
        print("\n===== LOGIN SYSTEM =====")
        print("1. Admin Login")
        print("2. Customer Login")

        choice = input("Enter choice: ")

        if choice == "1":
            password = input("Enter Admin Password: ")

            if password == "admin123":
                self.user_type = "admin"
                print("Admin Login Successful!")

            else:
                print("Wrong Password!")
                self.user_type = None

        elif choice == "2":
            self.user_type = "customer"
            print("Customer Login Successful!")

        else:
            print("Invalid Choice")
            self.user_type = None

    # ================= MENU =================

    def show_menu(self):
        print("\n----- MENU -----")

        for item, price in self.menu.items():
            print(f"{item.title():15} ₹{price}")

    # ================= ADD ITEM =================

    def add_item(self):

        while True:

            item = input("Enter food item name: ").lower()
            price = float(input("Enter item price: "))
            self.menu[item] = price
            print("Item added successfully!")
            more = input("Add another item? (yes/no): ").lower()
            if more != "yes":
               break

    # ================= PLACE ORDER =================

    def place_order(self):
        self.show_menu()

        while True:

            item = input("\nEnter item name: ").lower()
            if item in self.menu:
                try:
                    qty = int(input("Enter quantity: "))

                    if qty > 0:
                        self.cart[item] = (self.cart.get(item,0)+ qty)
                        print("Item added to cart!")

                    else:
                        print("Quantity must be greater than 0")

                except:
                    print("Invalid quantity!")

            else:
                print("Item not available!")

            more = input("Order more? (yes/no): ").lower()

            if more != "yes":
                break

    # ================= REMOVE ITEM =================

    def remove_item(self):

        if not self.cart:
            print("Cart is empty!")
            return

        item = input("Enter item to remove: ").lower()

        if item in self.cart:
            del self.cart[item]
            print("Item removed!")

        else:
            print("Item not in cart!")

    # ================= VIEW CART =================

    def view_cart(self):
        print("\n----- ORDER SUMMARY -----")

        if not self.cart:
            print("Cart is empty")
            return
        total = 0

        for item, qty in self.cart.items():
            price = self.menu[item]
            amount = price * qty
            total += amount

            print(f"{item.title():15}"f"{qty} x ₹{price}"f" = ₹{amount}")

        print("------------------------")
        print(f"Total = ₹{total}")

    # ================= SAVE ORDER =================

    def save_order(self, order):
        data = []

        if os.path.exists(self.order_file):
            with open(self.order_file,"r") as file:

                try:
                    data = json.load(file)

                except:
                    data = []

        data.append(order)
        with open(self.order_file,"w") as file:
            json.dump(data,file,indent=4)

        print("Order saved successfully!")

    # ================= GENERATE BILL =================

    def generate_bill(self):

        print("\n----- FINAL BILL -----")

        if not self.cart:
            print("No items ordered!")
            return
        total = 0
        bill_data = []

        for item, qty in self.cart.items():
            price = self.menu[item]
            amount = price * qty
            total += amount
            bill_data.append({
                "item": item,
                "qty": qty,
                "price": price,
                "amount": amount
                })

            print(f"{item.title():15}"f"{qty} x ₹{price}"f" = ₹{amount}")
            discount = 0
            if total >= 500:
                discount = total * 0.10

        gst = (total - discount) * 0.05

        final_total = (total- discount + gst)

        print("------------------------")

        print(f"Subtotal = ₹{total}")
        print(f"Discount = ₹{discount}")
        print(f"GST (5%) = ₹{gst}")
        print(f"FINAL TOTAL = ₹{final_total}")

        order = {
            "items":bill_data,
            "subtotal":total,
            "discount":discount,
            "gst":gst,
            "total":final_total
            }

        self.save_order(order)

    # ================= MAIN MENU =================

    def run(self):

        self.login()

        if self.user_type is None:
            return

        while True:

            print("\n===== ONLINE FOOD ORDERING SYSTEM =====")
            print("1. Add Food Item (Admin)")
            print("2. View Menu")
            print("3. Place Order")
            print("4. Remove Item")
            print("5. View Cart")
            print("6. Generate Bill")
            print("7. Exit")

            choice = input("Enter choice: ")
            if choice == "1":
                if self.user_type == "admin":
                    self.add_item()

                else:
                    print("Only Admin can add items!")

            elif choice == "2":
                self.show_menu()

            elif choice == "3":
                self.place_order()

            elif choice == "4":
                self.remove_item()

            elif choice == "5":
                self.view_cart()

            elif choice == "6":
                self.generate_bill()

            elif choice == "7":
                print("Thank you! Visit Again...")

                break

            else:
                print("Invalid choice!")

if __name__ == "__main__":
    
    app = FoodOrderingSystem()
    app.run()