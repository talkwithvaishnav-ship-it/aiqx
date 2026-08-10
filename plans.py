if deposit >= 1000:
    plan = "Elite"
elif deposit >= 500:
    plan = "Ultra"
elif deposit >= 200:
    plan = "Premium"
elif deposit >= 100:
    plan = "Pro"
elif deposit >= 30:
    plan = "Core"
else:
    plan = None