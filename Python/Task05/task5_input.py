import timeit

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
MIN_FAT = 2.0
MAX_FAT = 7.0


def looks_like_number(text):
    """Checks with str methods whether text is a valid non-negative or negative decimal."""
    text = text.strip()
    if text.startswith("-"):
        text = text[1:]
    return text.count(".") <= 1 and text.replace(".", "", 1).isdigit()


def convert_try(text):
    """Converts with try/except. Returns the float or None."""
    try:
        return float(text)
    except ValueError:
        return None


# PART 1: input() always returns a string, so convert it
print("PART 1: conversion")
print("int('10')   =", int("10"), type(int("10")))
print("float('8.5') =", float("8.5"), type(float("8.5")))
print("'8.5' + '1.5' =", "8.5" + "1.5", "(string joining, not addition)")
print("float('8.5') + float('1.5') =", float("8.5") + float("1.5"))

# PART 2: what happens with bad input
print("\nPART 2: bad input")
for bad in ["8,5", "eight", " 8.5 ", "", "8.5.1", "-3", "1e3", "nan"]:
    print(f"{bad!r:8} string-check: {str(looks_like_number(bad)):5}  try/except: {convert_try(bad)}")
print("float('8,5') directly would raise ValueError, the program would crash")

# PART 3: timing of both approaches
N = 200000
t1 = timeit.timeit(lambda: looks_like_number("8.5"), number=N)
t2 = timeit.timeit(lambda: convert_try("8.5"), number=N)
t3 = timeit.timeit(lambda: convert_try("eight"), number=N)
print(f"\nPART 3: {N} calls -> string check: {t1:.4f}s  try (valid): {t2:.4f}s  try (invalid): {t3:.4f}s")


# PART 4: read one real entry from the clerk
def read_number(prompt, low, high):
    """Asks until the clerk types a valid number between low and high."""
    while True:
        text = input(prompt)
        if not looks_like_number(text):
            print("  Invalid number, use digits and one dot, for example 8.5")
            continue
        value = float(text)
        if not (low <= value <= high):
            print(f"  Must be between {low} and {high}")
            continue
        return value


print("\nPART 4: enter one entry")
text = input("Farmer ID (whole number): ")
while not text.strip().isdigit():
    print("  Invalid ID, digits only")
    text = input("Farmer ID (whole number): ")
farmer_id = int(text)
print("type of the typed value:", type(text), "-> after int():", type(farmer_id))

litres = read_number("Litres (0.1 to 500): ", 0.1, 500)
fat = read_number("Fat % (2.0 to 7.0): ", MIN_FAT, MAX_FAT)
snf = read_number("SNF % (6.0 to 12.0): ", 6.0, 12.0)
shift = input("Shift (M/E): ").strip().upper()

rate = round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE
             + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
amount = round(litres * rate, 2)

print()
print(f"{'ID':>6} {'Shift':>5} {'Litres':>8} {'Fat':>5} {'SNF':>5} {'Rate':>8} {'Amount':>10}")
print(f"{farmer_id:>6} {shift:>5} {litres:8.2f} {fat:5.2f} {snf:5.2f} {rate:8.2f} {amount:10.2f}")