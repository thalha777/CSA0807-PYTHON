import math
import time

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30
MIN_FAT, MAX_FAT = 2.0, 7.0
MIN_SNF, MAX_SNF = 6.0, 12.0
MAX_LITRES = 500


def rate_per_litre(fat, snf):
    """Return the price per litre for the given fat % and SNF %."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    return round(BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE, 2)


def payout(litres, fat, snf):
    """Return the amount payable for one entry."""
    return round(litres * rate_per_litre(fat, snf), 2)


def check_entry(litres_text, fat_text, snf_text):
    """Validate the clerk's text. Return ((litres, fat, snf), 'OK') or (None, reason)."""
    values = []
    for name, text in [("litres", litres_text), ("fat", fat_text), ("snf", snf_text)]:
        try:
            value = float(text)
        except ValueError:
            return None, f"{name} is not a number"
        if not math.isfinite(value):
            return None, f"{name} is not a finite number"
        values.append(value)
    litres, fat, snf = values
    if litres <= 0 or litres > MAX_LITRES:
        return None, f"litres must be above 0 and up to {MAX_LITRES}"
    if not MIN_FAT <= fat <= MAX_FAT:
        return None, f"fat must be between {MIN_FAT} and {MAX_FAT}"
    if not MIN_SNF <= snf <= MAX_SNF:
        return None, f"snf must be between {MIN_SNF} and {MAX_SNF}"
    return (litres, fat, snf), "OK"


def ten_day_total(entries):
    """Return the total payable for a list of (litres, fat, snf) tuples."""
    return round(sum(payout(l, f, s) for l, f, s in entries), 2)


# Test cases: (description, litres, fat, snf, expected rate, expected pay)
VALID_CASES = [
    ("Standard milk",        10,  3.5, 8.5, 30.00, 300.00),
    ("Fat above standard",   10,  4.2, 8.5, 32.80, 328.00),
    ("Fat below standard",   10,  3.1, 8.5, 28.40, 284.00),
    ("SNF above standard",   10,  3.5, 8.9, 31.20, 312.00),
    ("SNF below standard",   10,  3.5, 8.1, 28.80, 288.00),
    ("Lowest fat 2.0",       10,  2.0, 8.5, 24.00, 240.00),
    ("Highest fat 7.0",      10,  7.0, 8.5, 44.00, 440.00),
    ("Fat and SNF above",   8.5,  4.2, 8.7, 33.40, 283.90),
    ("Fat and SNF below",    12,  3.1, 8.3, 27.80, 333.60),
]

INVALID_CASES = [
    ("Text for litres",  "abc", "3.5", "8.5"),
    ("Comma decimal",    "10",  "3,5", "8.5"),
    ("Negative litres",  "-5",  "3.5", "8.5"),
    ("Zero litres",      "0",   "3.5", "8.5"),
    ("Fat above 7.0",    "10",  "7.5", "8.5"),
    ("Fat below 2.0",    "10",  "1.9", "8.5"),
]

# 5 entries whose total was calculated by hand:
# 300.00 + 328.00 + 284.00 + 283.90 + 333.60 = 1529.50
HAND_ENTRIES = [(10, 3.5, 8.5), (10, 4.2, 8.5), (10, 3.1, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]
HAND_TOTAL = 1529.50


def run_tests():
    """Run every test with assert. Stops with AssertionError if any test fails."""
    for desc, litres, fat, snf, exp_rate, exp_pay in VALID_CASES:
        assert rate_per_litre(fat, snf) == exp_rate, desc + " (rate)"
        assert payout(litres, fat, snf) == exp_pay, desc + " (pay)"
    for desc, a, b, c in INVALID_CASES:
        values, message = check_entry(a, b, c)
        assert values is None, desc
    assert check_entry("10", "3.5", "8.5")[0] == (10.0, 3.5, 8.5)
    assert ten_day_total(HAND_ENTRIES) == HAND_TOTAL
    return True


# PART 1: table of valid entries
print("PART 1: valid and boundary entries")
print(f"{'Case':20} {'Exp rate':>8} {'Act rate':>8} {'Exp pay':>8} {'Act pay':>8}  Result")
for desc, litres, fat, snf, exp_rate, exp_pay in VALID_CASES:
    act_rate, act_pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
    result = "PASS" if (act_rate == exp_rate and act_pay == exp_pay) else "FAIL"
    print(f"{desc:20} {exp_rate:8.2f} {act_rate:8.2f} {exp_pay:8.2f} {act_pay:8.2f}  {result}")

# PART 2: table of invalid entries
print("\nPART 2: invalid entries (all must be rejected)")
print(f"{'Case':18} {'Input':22} Result")
for desc, a, b, c in INVALID_CASES:
    values, message = check_entry(a, b, c)
    result = "PASS (rejected: " + message + ")" if values is None else "FAIL (accepted)"
    print(f"{desc:18} {str((a, b, c)):22} {result}")

# PART 3: hand-calculated total
print("\nPART 3: five entries with hand-calculated total")
actual_total = ten_day_total(HAND_ENTRIES)
print("Expected (by hand):", f"{HAND_TOTAL:.2f}", "| Actual:", f"{actual_total:.2f}",
      "| PASS" if actual_total == HAND_TOTAL else "| FAIL")

# PART 4: assert-based test function and its running time
print("\nPART 4: automatic tests with assert")
start = time.perf_counter()
for _ in range(1000):
    run_tests()
elapsed = time.perf_counter() - start
print("All asserts passed. Time for 1000 complete reruns:", f"{elapsed:.4f}s",
      f"({elapsed / 1000 * 1000:.3f} ms per rerun)")