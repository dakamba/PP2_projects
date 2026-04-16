import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Product block regex
pattern = re.compile(
    r'\d+\.\s*\n'                       # item number
    r'(.+?)\n'                          # product name
    r'([\d,]+)\s*x\s*([\d\s]+,\d{2})\n' # quantity x price
    r'([\d\s]+,\d{2})',                 # total
    re.S
)

products = []

for match in pattern.finditer(text):
    name = match.group(1).strip()
    quantity = float(match.group(2).replace(',', '.'))
    price = float(match.group(3).replace(' ', '').replace(',', '.'))
    total = float(match.group(4).replace(' ', '').replace(',', '.'))

    products.append({
        "name": name,
        "quantity": quantity,
        "price": price,
        "total": total
    })

# Total receipt amount
total_pattern = re.search(r'ИТОГО:\s*\n?([\d\s]+,\d{2})', text)
total_amount = None
if total_pattern:
    total_amount = float(total_pattern.group(1).replace(' ', '').replace(',', '.'))

# Date and time
datetime_pattern = re.search(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})', text)
date, time = (datetime_pattern.group(1), datetime_pattern.group(2)) if datetime_pattern else (None, None)

# Payment method
payment_pattern = re.search(r'Банковская карта', text, re.IGNORECASE)
payment_method = payment_pattern.group(0) if payment_pattern else None

parsed_receipt = {
    "products": products,
    "total_amount": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(parsed_receipt, indent=4, ensure_ascii=False))
