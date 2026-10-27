import timeit

# PART 1: Named constants (UPPER_CASE). A rate revision is made here only.
BASE_RATE = 30.00        # Rs per litre at standard fat and SNF
FAT_STEP_VALUE = 0.40    # Rs per 0.1 % of fat
SNF_STEP_VALUE = 0.30    # Rs per 0.1 % of SNF
STANDARD_FAT = 3.5
STANDARD_SNF = 8.5
STEP_SIZE = 0.1
MIN_FAT = 2.0
MAX_FAT = 7.0


def rate_per_litre(fat, snf):
    fat_steps = round((fat - STANDARD_FAT) / STEP_SIZE)
    snf_steps = round((snf - STANDARD_SNF) / STEP_SIZE)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


print("PART 1: constants")
print("BASE_RATE =", BASE_RATE, "| FAT_STEP_VALUE =", FAT_STEP_VALUE, "| SNF_STEP_VALUE =", SNF_STEP_VALUE)
print("Allowed fat range:", MIN_FAT, "to", MAX_FAT)
print("rate_per_litre(4.2, 8.7) =", rate_per_litre(4.2, 8.7))

# PART 2: Python has no true constants, UPPER_CASE is only a convention
print("\nPART 2: no true constants")
original = BASE_RATE
BASE_RATE = 99.0          # Python allows this without any error
print("After BASE_RATE = 99.0, rate_per_litre(3.5, 8.5) =", rate_per_litre(3.5, 8.5))
BASE_RATE = original      # restore it
print("Restored, rate_per_litre(3.5, 8.5) =", rate_per_litre(3.5, 8.5))

# PART 3: Dynamic typing
print("\nPART 3: dynamic typing")
x = 10
print("x =", x, type(x))
x = "ten"
print("x =", x, type(x))
x = 8.5
print("x =", x, type(x))

# PART 4: Multiple assignment and swapping
print("\nPART 4: multiple assignment and swap")
litres, fat, snf = 10, 3.5, 8.5
print("litres, fat, snf =", litres, fat, snf)
a, b = 3.5, 8.5
print("before swap: a =", a, "b =", b)
a, b = b, a
print("after swap : a =", a, "b =", b)

# PART 5: Alternatives - magic numbers and a dictionary
RATE_CARD = {"base": 30.0, "fat": 0.40, "snf": 0.30}


def rate_magic(fat, snf):
    return round(30.00 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30, 2)


def rate_dict(fat, snf):
    return round(RATE_CARD["base"] + round((fat - 3.5) / 0.1) * RATE_CARD["fat"]
                 + round((snf - 8.5) / 0.1) * RATE_CARD["snf"], 2)


print("\nPART 5: alternatives")
print("constants:", rate_per_litre(4.2, 8.7), "| magic:", rate_magic(4.2, 8.7), "| dict:", rate_dict(4.2, 8.7))

N = 200000
t_const = timeit.timeit(lambda: rate_per_litre(4.2, 8.7), number=N)
t_magic = timeit.timeit(lambda: rate_magic(4.2, 8.7), number=N)
t_dict = timeit.timeit(lambda: rate_dict(4.2, 8.7), number=N)
print(f"Time for {N} calls -> constants: {t_const:.4f}s  magic: {t_magic:.4f}s  dict: {t_dict:.4f}s")