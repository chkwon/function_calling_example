import os
import gradio as gr
from openai import OpenAI
from common_tools import process


os.environ["OPENAI_API_KEY"] = (
    "<<Your_API_Key_Here>>"
)
OpenAI.api_key = os.getenv("OPENAI_API_KEY")


def get_fruit_price(fruit_name):
    fruit_prices = {"apple": "1000 KRW", "banana": "500 KRW", "orange": "750 KRW", "mango": "800 KRW"}
    if fruit_name in fruit_prices:
        return fruit_prices[fruit_name]
    else:
        return "No price information for: " + fruit_name


# Initialize conversation with system prompt
MESSAGES = [
    {
        "role": "system",
        "content": (
            "You are a helpful assistant. You can retrieve fruit prices for the user."
        ),
    },
]

# Map available functions with their corresponding implementations
AVAILABLE_FUNCTIONS = {
    "get_fruit_price": get_fruit_price,
}

FUNCTION_DESCRIPTIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_fruit_price",
            "description": "Returns the current price of the specified fruit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fruit_name": {
                        "type": "string",
                        "description": "The name of the fruit to retrieve the price for (e.g., 'apple', 'banana').",
                    }
                },
                "required": ["fruit_name"],
            },
        },
    }
]


# Gradio UI setup
if __name__ == "__main__":
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(label="Fruit Price Chatbot")
        user_textbox = gr.Textbox(label="Input")
        user_textbox.submit(
            lambda user_textbox, chatbot: process(
                user_textbox,
                chatbot,
                MESSAGES,
                FUNCTION_DESCRIPTIONS,
                AVAILABLE_FUNCTIONS,
            ),
            inputs=[user_textbox, chatbot],
            outputs=[user_textbox, chatbot],
        )

    demo.launch(share=False, debug=True)
