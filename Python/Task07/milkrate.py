"""Rate card of the village milk co-operative (used as a module)."""

import sys

BASE_RATE = 30.00       
FAT_STEP_VALUE = 0.40   
SNF_STEP_VALUE = 0.30   


def rate_per_litre(fat, snf):
    
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return round(rate, 2)


def payout(litres, fat, snf):
    
    return round(litres * rate_per_litre(fat, snf), 2)


if __name__ == "__main__":
    
    print("PART 1: running milkrate.py directly")
    print("__name__ is:", __name__)
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate, pay = rate_per_litre(fat, snf), payout(litres, fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {pay:8.2f}")

    
    print("\nimporting milkrate as a module")
    import milkrate                      
    from milkrate import payout as p     
    import milkrate as mr                

    print("Imported module __name__ is:", milkrate.__name__)
    print("(No table was printed above, because __name__ != '__main__' on import)")
    print("milkrate.payout(10, 3.5, 8.5) =", milkrate.payout(10, 3.5, 8.5))
    print("p(10, 3.5, 8.5)               =", p(10, 3.5, 8.5))
    print("mr.payout(10, 3.5, 8.5)       =", mr.payout(10, 3.5, 8.5))


    print("\nmodule search")
    print("'milkrate' in sys.modules:", "milkrate" in sys.modules)
    print("First place searched (sys.path[0]):", sys.path[0])