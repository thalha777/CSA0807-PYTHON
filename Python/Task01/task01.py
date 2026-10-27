
import sys
import time

# ---- Named constants (never change during a run) ----
BASE_RATE = 30.00        # Rs/litre at 3.5 % fat and 8.5 % SNF
STD_FAT = 3.5            # standard fat %
STD_SNF = 8.5            # standard SNF %
FAT_STEP_VALUE = 0.40    # Rs per 0.1 % fat
SNF_STEP_VALUE = 0.30    # Rs per 0.1 % SNF
MIN_FAT, MAX_FAT = 2.0, 7.0
PAY_CYCLE_DAYS = 10

# ---- Data inventory: name -> (python type, role, why) ----
DATA = [
    ("farmer_id", "str",   "input",  "label, no arithmetic, may have leading zeros"),
    ("litres",    "float", "input",  "fractional quantity measured on a scale"),
    ("fat",       "float", "input",  "percentage with decimals"),
    ("snf",       "float", "input",  "percentage with decimals"),
    ("shift",     "str",   "input",  "'M' or 'E' (morning/evening)"),
    ("rate",      "Decimal/float", "output", "Rs per litre, 2 decimals"),
    ("amount",    "Decimal/float", "output", "litres x rate, rounded to paise"),
    ("ten_day_total", "Decimal/float", "output", "sum of payments in 10 days"),
]
print(f"{'Name':14}{'Type':15}{'Role':8}Reason")
for name, typ, role, why in DATA:
    print(f"{name:14}{typ:15}{role:8}{why}")


# ---- Rules every valid entry must satisfy ----
def validate(farmer_id, litres, fat, snf, shift):
    """Return a list of rule violations (empty list = valid)."""
    errors = []
    if not farmer_id:
        errors.append("farmer id is empty")
    if litres < 0:
        errors.append("litres cannot be negative")
    if not (MIN_FAT <= fat <= MAX_FAT):
        errors.append("fat must be between 2.0 and 7.0")
    if snf <= 0:
        errors.append("snf must be positive")
    if shift not in ("M", "E"):
        errors.append("shift must be M or E")
    return errors


print("\nValidation demo:")
print(validate("F001", 10, 3.5, 8.5, "M"))
print(validate("F002", -5, 7.5, 8.5, "X"))

# ---- Alternative concept: 3 separate variables vs one tuple per entry ----
N = 300
print(f"\nAlternative: separate variables vs list of tuples for n = {N}")

# (a) separate variables: code would need 3*n names; we build the source text
src = "\n".join(f"litres{i}, fat{i}, snf{i} = 10.0, 3.5, 8.5" for i in range(N))
src += "\ntotal = " + " + ".join(f"litres{i}*(30.0)" for i in range(N))
print("Lines of code needed for separate variables:", src.count("\n") + 1)

t = time.perf_counter()
ns = {}
exec(src, ns)
t_sep = time.perf_counter() - t

# (b) one tuple per entry in a list: same code size for any n
entries = [(10.0, 3.5, 8.5)] * N
t = time.perf_counter()
total = 0.0
for litres, fat, snf in entries:
    total += litres * 30.0
t_list = time.perf_counter() - t

print(f"Separate variables (build + run): {t_sep:.6f} s, total = {ns['total']}")
print(f"List of tuples loop             : {t_list:.6f} s, total = {total}")
print("Memory of the list object:", sys.getsizeof(entries), "bytes")
print("Both are O(n) time and space, but only the list design uses a")
print("loop of fixed code size; the first needs ~3n names written by hand,")
print("so it cannot scale to 6,000 or 150,000 farmers.")