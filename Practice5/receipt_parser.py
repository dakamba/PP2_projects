import re
import json

# Load the raw receipt
with open('raw.txt', 'r', encoding='utf-8') as file:
    receipt_text = file.read()

# 1️⃣ Extract all prices (handle spaces and comma as decimal)
price_pattern = re.compile(r'(\d{1,3}(?: \d{3})*,\d{2})')
prices_raw = price_pattern.findall(receipt_text)
# Convert to float
prices = [float(p.replace(' ', '').replace(',', '.')) for p in prices_raw]

# 2️⃣ Extract product names
# Product lines start with a number + dot + name, then quantity x price
product_pattern = re.compile(r'\d+\.\s+(.+?)\n\d+,\d+ x \d{1,3}(?: \d{3})*,\d{2}', re.MULTILINE)
products = product_pattern.findall(receipt_text)

# 3️⃣ Calculate total amount
total_amount = sum(prices)

# 4️⃣ Extract date and time
datetime_pattern = re.compile(r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})')
datetime_match = datetime_pattern.search(receipt_text)
date, time = (datetime_match.group(1), datetime_match.group(2)) if datetime_match else (None, None)

# 5️⃣ Extract payment method
payment_pattern = re.compile(r'Банковская карта|CASH|CREDIT|DEBIT', re.IGNORECASE)
payment_match = payment_pattern.search(receipt_text)
payment_method = payment_match.group(0) if payment_match else None

# 6️⃣ Structured output
parsed_receipt = {
    "products": products,
    "prices": prices,
    "total_amount": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

# Print formatted JSON
print(json.dumps(parsed_receipt, indent=4, ensure_ascii=False))
