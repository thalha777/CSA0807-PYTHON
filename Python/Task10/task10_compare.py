import random
import sys
import time
from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def make_entries(n):
    """Return n reproducible random entries (litres, fat, snf) with 1 decimal each."""
    rng = random.Random(42)
    return [(rng.randint(10, 3000) / 10, rng.randint(20, 70) / 10, rng.randint(60, 120) / 10)
            for _ in range(n)]


# ---------- float version ----------
def rate_float(fat, snf):
    """Return the rate per litre using float."""
    fs = round((fat - 3.5) / 0.1)
    ss = round((snf - 8.5) / 0.1)
    return round(30.00 + fs * 0.40 + ss * 0.30, 2)


def pays_float(entries):
    """Return the list of float payments, each rounded to 2 decimals."""
    return [round(l * rate_float(f, s), 2) for l, f, s in entries]


def total_float(entries):
    """Add float payments one by one with +=."""
    total = 0.0
    for p in pays_float(entries):
        total += p
    return total


# ---------- Decimal version ----------
def rate_decimal(fat, snf):
    """Return the rate per litre as an exact Decimal (steps counted in whole tenths)."""
    fs = round(fat * 10) - 35
    ss = round(snf * 10) - 85
    return Decimal("30.00") + fs * Decimal("0.40") + ss * Decimal("0.30")


def pay_decimal(l, f, s):
    """Return one payment as Decimal rounded half-up to the paisa."""
    return (Decimal(str(l)) * rate_decimal(f, s)).quantize(CENT, rounding=ROUND_HALF_UP)


def pays_decimal(entries):
    """Return the list of Decimal payments."""
    return [pay_decimal(l, f, s) for l, f, s in entries]


def total_decimal(entries):
    """Total of per-payment rounded Decimal payments (the bank method)."""
    return sum(pays_decimal(entries), Decimal("0"))


def total_decimal_round_once(entries):
    """Add exact unrounded amounts and round only the final total."""
    exact = sum((Decimal(str(l)) * rate_decimal(f, s) for l, f, s in entries), Decimal("0"))
    return exact.quantize(CENT, rounding=ROUND_HALF_UP)


# ---------- Alternative: rate table (dictionary) ----------
def total_with_table(entries):
    """Compute each (fat, snf) rate once, store it in a dict, reuse it."""
    table = {}
    total = Decimal("0")
    for l, f, s in entries:
        key = (round(f * 10), round(s * 10))
        if key not in table:
            table[key] = rate_decimal(f, s)
        total += (Decimal(str(l)) * table[key]).quantize(CENT, rounding=ROUND_HALF_UP)
    return total, table


def timed(func, *args):
    """Return (result, seconds)."""
    start = time.perf_counter()
    result = func(*args)
    return result, time.perf_counter() - start


print("PART 1: float vs Decimal totals (per-payment rounding)")
print(f"{'n':>8} {'float total':>22} {'Decimal total':>16} {'difference':>22} {'float s':>8} {'Dec s':>8}")
data = {}
for n in (300, 6000, 150000):
    entries = make_entries(n)
    data[n] = entries
    tf, sf = timed(total_float, entries)
    td, sd = timed(total_decimal, entries)
    print(f"{n:>8} {tf:>22.10f} {str(td):>16} {tf - float(td):>22.12f} {sf:>8.4f} {sd:>8.4f}")

print("\nPART 2: per-payment float vs Decimal (how many payments differ by a paisa?)")
for n, entries in data.items():
    pf, pd = pays_float(entries), pays_decimal(entries)
    diff = sum(1 for a, b in zip(pf, pd) if Decimal(str(a)) != b)
    print(f"n = {n:>6}: {diff} payments differ")

print("\nPART 3: round each payment vs round only the total")
print(f"{'n':>8} {'sum of rounded':>16} {'round total once':>18} {'difference':>12}")
for n, entries in data.items():
    each, once = total_decimal(entries), total_decimal_round_once(entries)
    print(f"{n:>8} {str(each):>16} {str(once):>18} {str(each - once):>12}")

print("\nPART 4: rate table (dictionary) vs recalculating each time")
print(f"{'n':>8} {'recalc s':>10} {'table s':>10} {'pairs k':>8} {'table bytes':>12} {'same total':>11}")
for n, entries in data.items():
    t1, s1 = timed(total_decimal, entries)
    (t2, table), s2 = timed(total_with_table, entries)
    print(f"{n:>8} {s1:>10.4f} {s2:>10.4f} {len(table):>8} {sys.getsizeof(table):>12} {str(t1 == t2):>11}")