# Description: Insurance premium calculation program for One Stop Insurance Company.
# Author: ivan zymalov
# Date(s): nov 24

# Define required libraries.
import datetime
from formatvalues import format_currency, format_title_case, format_uppercase

# Define program constants.
CONST = {
    "next_policy_number": 1944,
    "base_premium": 869.00,
    "additional_car_discount": 0.25,
    "liability_coverage": 130.00,
    "glass_coverage": 86.00,
    "rental_coverage": 58.00,
    "hst_rate": 0.15,
    "monthly_processing_fee": 39.99,
}

VALID_PROVINCES = ["ON", "QC", "NS", "NB", "MB", "BC", "PE", "SK", "AB", "NL"]
PAYMENT_METHODS = ["Full Amount", "Monthly", "Down Payment"]

# Define program functions.
def calculate_premium(num_cars, liability, glass, rental):
    """Calculates the total insurance premium."""
    base_premium = CONST["base_premium"] + CONST["base_premium"] * CONST["additional_car_discount"] * (num_cars - 1)
    additional_costs = num_cars * (liability * CONST["liability_coverage"] +
                                   glass * CONST["glass_coverage"] +
                                   rental * CONST["rental_coverage"])
    total_premium = base_premium + additional_costs
    hst = total_premium * CONST["hst_rate"]
    total_cost = total_premium + hst
    return total_premium, hst, total_cost

def calculate_monthly_payment(total_cost, first_payment=0):
    """Calculates the monthly payment."""
    remaining = total_cost - first_payment
    monthly_payment = (remaining + CONST["monthly_processing_fee"]) / 8
    return monthly_payment

def display_receipt(client_data, total_premium, hst, total_cost, monthly_payment=None, claims=[]):
    """Displays the receipt with client data and calculations."""
    print("\n*** One Stop Insurance Company ***")
    print(f"Policy Number: {client_data['policy_number']}")
    print(f"Client: {client_data['first_name']} {client_data['last_name']}")
    print(f"Address: {client_data['address']}, {client_data['city']}, {client_data['province']} {client_data['postal_code']}")
    print(f"Phone: {client_data['phone']}")
    print(f"Number of Cars: {client_data['num_cars']}")
    print(f"Total Premium: {format_currency(total_premium)}")
    print(f"HST (15%): {format_currency(hst)}")
    print(f"Total Cost: {format_currency(total_cost)}")
    if monthly_payment:
        print(f"Monthly Payment: {format_currency(monthly_payment)}")
    print("\nClaims:")
    print("Claim Number     Claim Date        Amount")
    print("--------------------------------------------")
    for claim in claims:
        print(f"{claim['claim_number']:<16} {claim['claim_date']}      {format_currency(claim['claim_amount'])}")
    print("--------------------------------------------\n")

# Main program starts here.
def main():
    """Main program logic."""
    while True:
        # Gather user inputs.
        first_name = format_title_case(input("Enter client's first name: "))
        last_name = format_title_case(input("Enter client's last name: "))
        address = input("Enter client's address: ")
        city = format_title_case(input("Enter city: "))
        province = input("Enter province (e.g., ON): ").upper()
        while province not in VALID_PROVINCES:
            province = input("Invalid province. Please try again: ").upper()
        postal_code = input("Enter postal code: ")
        phone = input("Enter phone number: ")

        num_cars = int(input("Enter the number of cars: "))
        liability = format_uppercase(input("Add liability coverage? (Y/N): ")) == "Y"
        glass = format_uppercase(input("Add glass coverage? (Y/N): ")) == "Y"
        rental = format_uppercase(input("Add rental coverage? (Y/N): ")) == "Y"

        payment_method = format_title_case(input("Payment method (Full Amount/Monthly/Down Payment): "))
        while payment_method not in PAYMENT_METHODS:
            payment_method = format_title_case(input("Invalid payment method. Please try again: "))

        first_payment = 0
        if payment_method == "Down Payment":
            first_payment = float(input("Enter down payment amount: "))

        # Perform required calculations.
        claims = []
        while True:
            add_claim = format_uppercase(input("Add a claim? (Y/N): ")) == "Y"
            if not add_claim:
                break
            claim_number = input("Enter claim number: ")
            claim_date = input("Enter claim date (YYYY-MM-DD): ")
            claim_amount = float(input("Enter claim amount: "))
            claims.append({"claim_number": claim_number, "claim_date": claim_date, "claim_amount": claim_amount})

        total_premium, hst, total_cost = calculate_premium(num_cars, liability, glass, rental)
        monthly_payment = None
        if payment_method in ["Monthly", "Down Payment"]:
            monthly_payment = calculate_monthly_payment(total_cost, first_payment)

        # Display results.
        client_data = {
            "policy_number": CONST["next_policy_number"],
            "first_name": first_name,
            "last_name": last_name,
            "address": address,
            "city": city,
            "province": province,
            "postal_code": postal_code,
            "phone": phone,
            "num_cars": num_cars,
        }
        display_receipt(client_data, total_premium, hst, total_cost, monthly_payment, claims)

        # Write the values to a data file for storage.
        CONST["next_policy_number"] += 1

        # Continue or exit.
        continue_program = format_uppercase(input("Do you want to continue entering clients? (Y/N): ")) == "Y"
        if not continue_program:
            break

# Any housekeeping duties at the end of the program.
if __name__ == "__main__":
    main()
