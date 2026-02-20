
import re

def parse_text_attributes(query: str):
    query = query.lower()

    brand = None
    category = None
    color = None
    style = None

    brand_keywords = ["nike","puma","adidas","gucci","zara","h&m","uniqlo"]
    category_keywords = ["shoes","tshirt","shirt","hoodie","jacket","dress","pants","jeans","bag"]
    color_keywords = ["black","white","blue","red","green","beige","brown","gray","pink","yellow"]
    style_keywords = ["casual","formal","sports","street","party","vintage","retro","oversized"]

    for b in brand_keywords:
        if b in query: brand = b

    for c in category_keywords:
        if c in query: category = c

    for col in color_keywords:
        if col in query: color = col

    for s in style_keywords:
        if s in query: style = s

    return {
        "brand": brand,
        "category": category,
        "color": color,
        "style": style
    }
