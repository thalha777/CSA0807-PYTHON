import math
import timeit

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

# PART 1: Operator precedence and associativity
print("PART 1: precedence and associativity")
print("2 + 3 * 4       =", 2 + 3 * 4)        # * before +
print("(2 + 3) * 4     =", (2 + 3) * 4)      # brackets first
print("2 ** 3 ** 2     =", 2 ** 3 ** 2)      # ** is right-to-left: 2 ** 9
print("-2 ** 2         =", -2 ** 2)          # ** before unary minus: -(2**2)
print("(-2) ** 2       =", (-2) ** 2)
print("100 / 10 / 2    =", 100 / 10 / 2)     # / is left-to-right

# PART 2: Surprising results
print("\nPART 2: surprises")
print("(4.2 - 3.5) / 0.1        =", (4.2 - 3.5) / 0.1)            # 7.000000000000001
print("round((4.2 - 3.5) / 0.1) =", round((4.2 - 3.5) / 0.1))     # 7
print("int((4.2 - 3.5) / 0.1)   =", int((4.2 - 3.5) / 0.1))       # 7
print("(3.1 - 3.5) / 0.1        =", (3.1 - 3.5) / 0.1)            # about -4.000000000000004
print("int((3.1 - 3.5) / 0.1)   =", int((3.1 - 3.5) / 0.1))
print("0.1 + 0.2                =", 0.1 + 0.2)
print("round(2.5), round(3.5)   =", round(2.5), round(3.5))       # banker's rounding

# PART 3: round(), int() and math.floor() for negative values
print("\nPART 3: round vs int vs floor")
for v in [-4.6, -4.5, -4.4, 4.4, 4.6]:
    print(f"{v:5}  round={round(v):3}  int={int(v):3}  floor={math.floor(v):3}")

# PART 4: Comparison chaining and Boolean operators
print("\nPART 4: chaining and Boolean operators")
fat = 4.2
print("2.0 <= fat <= 7.0              =", 2.0 <= fat <= 7.0)
print("2.0 <= fat and fat <= 7.0      =", 2.0 <= fat and fat <= 7.0)
fat = 7.5
print("fat = 7.5 -> 2.0 <= fat <= 7.0 =", 2.0 <= fat <= 7.0)
print("not (2.0 <= fat <= 7.0)        =", not (2.0 <= fat <= 7.0))
print("fat < 2.0 or fat > 7.0         =", fat < 2.0 or fat > 7.0)

# PART 5: Rate and amount expressions
def rate_round(fat, snf):
    fs = round((fat - 3.5) / 0.1)
    ss = round((snf - 8.5) / 0.1)
    return round(BASE_RATE + fs * FAT_STEP_VALUE + ss * SNF_STEP_VALUE, 2)


def rate_int(fat, snf):
    fs = int((fat - 3.5) / 0.1)
    ss = int((snf - 8.5) / 0.1)
    return round(BASE_RATE + fs * FAT_STEP_VALUE + ss * SNF_STEP_VALUE, 2)


def rate_floor(fat, snf):
    fs = math.floor((fat - 3.5) / 0.1)
    ss = math.floor((snf - 8.5) / 0.1)
    return round(BASE_RATE + fs * FAT_STEP_VALUE + ss * SNF_STEP_VALUE, 2)


print("\nPART 5: rate with round / int / floor (snf = 8.5)")
print("Expected: fat 4.2 -> 32.80, fat 3.1 -> 28.40")
for fat in [4.2, 3.1]:
    print(f"fat {fat}: round={rate_round(fat, 8.5)}  int={rate_int(fat, 8.5)}  floor={rate_floor(fat, 8.5)}")

litres = 8.5
print("amount = litres * rate =", round(litres * rate_round(4.2, 8.7), 2))

# PART 6: Cost of each method (all O(1))
N = 200000
print("\nPART 6: time for", N, "calls")
for name, f in [("round", rate_round), ("int", rate_int), ("floor", rate_floor)]:
    print(f"{name:6}: {timeit.timeit(lambda: f(4.2, 8.7), number=N):.4f}s")