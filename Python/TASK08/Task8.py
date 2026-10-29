
def get_valid_input(prompt, minimum, maximum=None):
    while True:
        try:
            value = float(input(prompt))

            if value < minimum:
                print(f"Value must be at least {minimum}.")
            elif maximum is not None and value > maximum:
                print(f"Value must not exceed {maximum}.")
            else:
                return value

        except ValueError:
            print("Please enter a valid number.")


def rate_per_litre(fat, snf):
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    return round(30.00 + fat_steps * 0.40 + snf_steps * 0.30, 2)


def payout(litres, fat, snf):
    return round(litres * rate_per_litre(fat, snf), 2)


def main():
    litres = get_valid_input("Enter milk quantity in litres: ", 0)
    fat = get_valid_input("Enter fat percentage: ", 2.0, 7.0)
    snf = get_valid_input("Enter SNF percentage: ", 0)

    rate = rate_per_litre(fat, snf)
    payment = payout(litres, fat, snf)

    print(f"Rate per litre: Rs. {rate:.2f}")
    print(f"Total payment: Rs. {payment:.2f}")


if __name__ == "__main__":
    main()
