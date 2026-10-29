import timeit

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30


# PART 1: The functions
def rate_per_litre(fat, snf):
    """Return the price per litre (float, 2 decimals) for the given fat % and SNF %."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable (float, 2 decimals) for one entry."""
    return round(litres * rate_per_litre(fat, snf), 2)


def ten_day_total(entries):
    """Return the total payable for a list of (litres, fat, snf) tuples."""
    total = 0.0
    for litres, fat, snf in entries:
        total += payout(litres, fat, snf)
    return round(total, 2)


entries = [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]

print("PART 1: functions")
for litres, fat, snf in entries:
    print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate_per_litre(fat, snf):6.2f}  pay {payout(litres, fat, snf):8.2f}")
print("Ten-day total =", ten_day_total(entries))
print("Docstring of payout:", payout.__doc__)


# PART 2: return versus print
def payout_print(litres, fat, snf):
    """Print the payout but return nothing (bad design for calculations)."""
    print("payout is", round(litres * rate_per_litre(fat, snf), 2))


print("\nPART 2: return vs print")
result_return = payout(10, 3.5, 8.5)
result_print = payout_print(10, 3.5, 8.5)
print("returned value  :", result_return, "-> can be reused:", result_return + 1)
print("printing version:", result_print, "-> None, cannot be reused")


# PART 3: local and global names
def read_global():
    """Read a global constant (allowed)."""
    return BASE_RATE


def try_to_change_global():
    """Assign to BASE_RATE inside a function: this creates a LOCAL variable."""
    BASE_RATE = 99.0
    return BASE_RATE


def wrong_update():
    """Read then assign the same name: raises UnboundLocalError."""
    BASE_RATE = BASE_RATE + 1
    return BASE_RATE


print("\nPART 3: scope")
print("read_global()          =", read_global())
print("try_to_change_global() =", try_to_change_global(), "| global BASE_RATE is still", BASE_RATE)
try:
    wrong_update()
except UnboundLocalError as error:
    print("wrong_update() raised UnboundLocalError:", error)


# PART 4: Alternatives - one long script and lambda
print("\nPART 4: alternatives")
total_script = 0.0
for litres, fat, snf in entries:
    fs = round((fat - 3.5) / 0.1)
    ss = round((snf - 8.5) / 0.1)
    r = round(30.00 + fs * 0.40 + ss * 0.30, 2)
    total_script += round(litres * r, 2)
print("one long script total:", round(total_script, 2), "(rate formula is repeated for every use)")

rate_lambda = lambda fat, snf: round(BASE_RATE + round((fat - 3.5) / 0.1) * FAT_STEP_VALUE
                                     + round((snf - 8.5) / 0.1) * SNF_STEP_VALUE, 2)
payout_lambda = lambda litres, fat, snf: round(litres * rate_lambda(fat, snf), 2)
print("lambda payout(8.5, 4.2, 8.7):", payout_lambda(8.5, 4.2, 8.7))
print("lambda name:", rate_lambda.__name__, "(no meaningful name, no docstring)")

# PART 5: Does function-call overhead matter?
n = 100000
big = [(8.5, 4.2, 8.7)] * n


def inline_total(data):
    """Same calculation with no function calls inside the loop."""
    total = 0.0
    for litres, fat, snf in data:
        fs = round((fat - 3.5) / 0.1)
        ss = round((snf - 8.5) / 0.1)
        total += round(litres * round(BASE_RATE + fs * FAT_STEP_VALUE + ss * SNF_STEP_VALUE, 2), 2)
    return round(total, 2)


def lambda_total(data):
    """Same calculation using the lambda."""
    total = 0.0
    for litres, fat, snf in data:
        total += payout_lambda(litres, fat, snf)
    return round(total, 2)


print(f"\nPART 5: time for {n} entries")
for name, f in [("functions", ten_day_total), ("inline", inline_total), ("lambda", lambda_total)]:
    t = timeit.timeit(lambda: f(big), number=3) / 3
    print(f"{name:10}: {t:.4f}s   total = {f(big)}")