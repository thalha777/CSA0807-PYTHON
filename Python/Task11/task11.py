
import json
import random
import time
from decimal import Decimal, ROUND_HALF_UP

# Rate card is read from a file (alternative concept); created on first run
RATES = {"base": "30.00", "fat_step": "0.40", "snf_step": "0.30"}
with open("rate_card.json", "w") as f:
    json.dump(RATES, f)

t = time.perf_counter()
with open("rate_card.json") as f:
    card = {k: Decimal(v) for k, v in json.load(f).items()}
print(f"Rate card load time: {(time.perf_counter() - t) * 1e6:.1f} microseconds\n")

PAISE = Decimal("0.01")


def steps(value, standard):
    """Whole 0.1 steps from the standard value."""
    return ((value - Decimal(standard)) / Decimal("0.1")).quantize(Decimal("1"), ROUND_HALF_UP)


def payout(litres, fat, snf):
    """Rate x litres, rounded to paise."""
    fat, snf, litres = Decimal(str(fat)), Decimal(str(snf)), Decimal(str(litres))
    rate = card["base"] + steps(fat, "3.5") * card["fat_step"] + steps(snf, "8.5") * card["snf_step"]
    return (litres * rate).quantize(PAISE, ROUND_HALF_UP)


def payout_float(litres, fat, snf):
    rate = 30.0 + round((fat - 3.5) / 0.1) * 0.40 + round((snf - 8.5) / 0.1) * 0.30
    return litres * rate


# Quick correctness checks
assert payout(10, 3.5, 8.5) == Decimal("300.00")
assert payout(8.5, 4.2, 8.7) == Decimal("283.90")
assert payout(12, 3.1, 8.3) == Decimal("333.60")

# Experiment for 300, 6000 and 150000 payments
random.seed(1)
for n in (300, 6000, 150000):
    data = [(random.randint(100, 6000) / 100, random.randint(20, 70) / 10,
             random.randint(70, 100) / 10) for _ in range(n)]

    t = time.perf_counter()
    each = sum(payout(*e) for e in data)                       # round each payment
    t_dec = time.perf_counter() - t

    only_total = sum(Decimal(str(l)) * (payout(1, f, s)) for l, f, s in data).quantize(PAISE)
    t = time.perf_counter()
    flt = sum(payout_float(*e) for e in data)                  # plain float
    t_flt = time.perf_counter() - t

    print(f"n = {n}")
    print(f"  Decimal (round each) : {each}  time {t_dec:.4f} s")
    print(f"  Decimal (round total): {only_total}  diff {only_total - each}")
    print(f"  float                : {flt:.3f}  time {t_flt:.4f} s  diff {Decimal(flt) - each:.2f}")