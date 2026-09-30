CATALOG = {
    "home": [
        ("Lighting", "Warm LED ceiling light", 899, "Amazon", "https://www.amazon.in/s?k=warm+led+ceiling+light"),
        ("Lighting", "Minimal pendant light", 1499, "IKEA", "https://www.ikea.com/in/en/search/?q=pendant%20light"),
        ("Furniture", "Compact side table", 2499, "IKEA", "https://www.ikea.com/in/en/search/?q=side%20table"),
        ("Furniture", "6-seater dining table", 9999, "Amazon", "https://www.amazon.in/s?k=6+seater+dining+table"),
        ("Decor", "Framed wall art set", 1299, "Flipkart", "https://www.flipkart.com/search?q=wall+art"),
        ("Decor", "Indoor artificial plant", 699, "Amazon", "https://www.amazon.in/s?k=artificial+indoor+plant"),
        ("Storage", "Fabric storage organizer", 499, "Flipkart", "https://www.flipkart.com/search?q=storage+organizer"),
    ],
    "party": [
        ("Food", "Budget-friendly catering search", 0, "Zomato", "https://www.zomato.com/"),
        ("Food", "Restaurant and catering search", 0, "Swiggy", "https://www.swiggy.com/"),
        ("Venue", "Hotel and stay search", 0, "OYO", "https://www.oyorooms.com/"),
        ("Decor", "Balloon decoration package", 2500, "Local vendor estimate", "https://www.google.com/search?q=balloon+decoration+near+me"),
        ("Entertainment", "Speaker/music setup estimate", 2000, "Local vendor estimate", "https://www.google.com/search?q=party+speaker+rental+near+me"),
    ],
    "jewelry": [
        ("Earrings", "Minimal gold-tone drop earrings", 799, "Amazon", "https://www.amazon.in/s?k=gold+tone+drop+earrings"),
        ("Necklace", "Delicate pendant necklace", 999, "Flipkart", "https://www.flipkart.com/search?q=pendant+necklace"),
        ("Bangles", "Classic bangles set", 699, "Amazon", "https://www.amazon.in/s?k=bangles+set"),
        ("Jewelry set", "Occasion jewelry combo", 1499, "Flipkart", "https://www.flipkart.com/search?q=jewellery+set"),
    ],
}

def candidates(planner: str, budget: float):
    rows = CATALOG[planner]
    if planner == "party":
        return rows
    return [r for r in rows if r[2] <= budget * 0.7] or rows[:4]
