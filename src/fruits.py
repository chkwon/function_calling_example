FRUIT_FUNCTION_DESCRIPTION = {
    "type": "function",
    "function": {
        "name": "get_fruit_price",
        "description": "Returns the current price of the specified fruit.",
        "parameters": {
            "type": "object",
            "properties": {
                "fruit_name": {
                    "type": "string",
                    "description": "The name of the fruit to retrieve the price for (e.g., '사과', '바나나').",
                }
            },
            "required": ["fruit_name"],
        },
    },
}


def get_fruit_price(fruit_name):
    fruit_prices = {"apple": "1000", "banana": "500", "orange": "750", "mango": "800"}
    if fruit_name in fruit_prices:
        return fruit_prices[fruit_name]
    else:
        return "No price information for: " + fruit_name
