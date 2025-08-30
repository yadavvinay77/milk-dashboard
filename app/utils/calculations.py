def calc_amount(quantity, sample_weight, rate):
    try:
        return round(float(quantity) * float(sample_weight) * float(rate), 2)
    except Exception:
        return 0.0

def milk_balance(entries):
    # Credits = deposits by customer, Debits = withdrawals by customer or debit entries
    credit = sum(e.amount for e in entries if (e.status or "").lower() == "credit")
    debit = sum(e.amount for e in entries if (e.status or "").lower() == "debit")
    # 'Paid' is recorded but excluded from running balance
    return round(credit - debit, 2)