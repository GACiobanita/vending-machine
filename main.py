from machine_functionality import VendingMachine


def verify_closing_input(vending_machine):
    print("Would you like to order something from the vending machine?\n")
    print("Input [Y] or [N], yes or no respectively, without [].\n")
    check = str(input("Or, if you'd like to reset the data base, input [R].\n")).lower().strip()
    try:
        if check[0] == 'y':
            vending_machine.item_purchase_process()
            verify_closing_input(vending_machine)
        elif check[0] == 'n':
            vending_machine.close_vending_machine()
        elif check[0] == 'r':
            vending_machine.request_mediator_to_reset_data_base()
            verify_closing_input(vending_machine)
        else:
            print('Invalid Input')
            return verify_closing_input(vending_machine)
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return verify_closing_input(vending_machine)


def main():
    vending_machine = VendingMachine()
    verify_closing_input(vending_machine)


if __name__ == "__main__":
    main()
