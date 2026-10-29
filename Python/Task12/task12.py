
from decimal import Decimal, ROUND_HALF_UP

PAISE = Decimal("0.01")

# One rate card per season
RATE_CARDS = {
    "normal":  {"base": Decimal("30.00"), "fat_step": Decimal("0.40"), "snf_step": Decimal("0.30")},
    "apr_jun": {"base": Decimal("32.00"), "fat_step": Decimal("0.45"), "snf_step": Decimal("0.30")},
}
BONUS_PER_LITRE = Decimal("0.50")
BONUS_LIMIT = Decimal("500")


def rate_per_litre(fat, snf, season="normal"):
    """Rate per litre; 2-decimal readings give fractional 0.1 steps (paid pro rata)."""
    card = RATE_CARDS[season]
    fat_steps = (Decimal(str(fat)) - Decimal("3.5")) / Decimal("0.1")
    snf_steps = (Decimal(str(snf)) - Decimal("8.5")) / Decimal("0.1")
    rate = card["base"] + fat_steps * card["fat_step"] + snf_steps * card["snf_step"]
    return rate.quantize(PAISE, ROUND_HALF_UP)


def payout(litres, fat, snf, season="normal"):
    """Amount for one delivery, rounded to paise."""
    return (Decimal(str(litres)) * rate_per_litre(fat, snf, season)).quantize(PAISE, ROUND_HALF_UP)


def bonus(total_litres, season):
    """Rs 0.50 per litre if more than 500 litres in ten days (April-June only)."""
    total_litres = Decimal(str(total_litres))
    if season == "apr_jun" and total_litres > BONUS_LIMIT:
        return (total_litres * BONUS_PER_LITRE).quantize(PAISE, ROUND_HALF_UP)
    return Decimal("0.00")


def ten_day_total(entries, season):
    """entries = [(litres, fat, snf), ...] -> (payments, bonus, grand total)."""
    pay = sum((payout(l, f, s, season) for l, f, s in entries), Decimal("0"))
    b = bonus(sum(Decimal(str(e[0])) for e in entries), season)
    return pay, b, pay + b


# ---- Tests ----
assert rate_per_litre(3.5, 8.5, "normal") == Decimal("30.00")      # original still works
assert rate_per_litre(4.2, 8.7, "normal") == Decimal("33.40")
assert rate_per_litre(3.5, 8.5, "apr_jun") == Decimal("32.00")     # new base rate
assert rate_per_litre(4.2, 8.5, "apr_jun") == Decimal("35.15")     # 32 + 7 x 0.45
assert rate_per_litre(4.25, 8.55, "normal") == Decimal("33.15")    # 2-decimal reading
assert bonus(500, "apr_jun") == Decimal("0.00")                    # exactly 500: no bonus
assert bonus(501, "apr_jun") == Decimal("250.50")                  # above 500: bonus
assert bonus(600, "normal") == Decimal("0.00")                     # bonus only Apr-Jun
print("All asserts passed\n")

# ---- Demonstration for both seasons and the bonus ----
print("Rates for both seasons")
for fat, snf in [(3.5, 8.5), (4.2, 8.7), (4.25, 8.55)]:
    print(f"fat {fat} snf {snf}: normal {rate_per_litre(fat, snf, 'normal')}, "
          f"apr_jun {rate_per_litre(fat, snf, 'apr_jun')}")

print("\nTen-day totals")
for litres in (400, 600):
    entries = [(litres / 4, 3.5, 8.5)] * 4
    for season in ("normal", "apr_jun"):
        pay, b, grand = ten_day_total(entries, season)
        print(f"{litres} L {season:8}: payments {pay}, bonus {b}, total {grand}")