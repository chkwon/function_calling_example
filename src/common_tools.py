from openai import OpenAI

import json 
import markdown2

def call_tool(function_name, arguments, available_functions):
    """
    Call the tool function with given arguments and return its response.
    Handles exceptions and ensures response is a string.
    """
    function = available_functions.get(function_name)
    if not function:
        return f"The tool '{function_name}' is unavailable."

    try:
        # Parse the arguments and call the function
        function_args = json.loads(arguments)
        response = function(**function_args)
        # Convert non-string responses to JSON string
        if not isinstance(response, str):
            response = json.dumps(response, ensure_ascii=False)
    except Exception as e:
        response = f"Error calling {function_name}: {e}"
    return response


def handle_tool_calls(messages, tool_calls, available_functions):
    """
    Processes each tool call from the assistant's message, updates the conversation
    with tool responses.
    """
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = tool_call.function.arguments
        tool_response = call_tool(function_name, arguments, available_functions)

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": tool_response,
            }
        )
    return messages


def postprocess_message(text_message):
    # msg = text_message.replace("\n", "<br>").replace(" .", ".").strip()
    html = markdown2.markdown(text_message)
    return html


def ask_openai(llm_model, messages, user_message, function_descriptions, available_functions):
    """
    Handle interaction with OpenAI's chat model including tool invocation and subsequent responses.
    """
    client = OpenAI()

    # Append user message if provided
    if user_message:
        messages.append({"role": "user", "content": user_message})

    # First call to OpenAI with tool-enabled functions
    response = client.chat.completions.create(
        model=llm_model, messages=messages, tools=function_descriptions, tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # If assistant wants to call tools
    if tool_calls:
        messages.append(response_message)
        messages = handle_tool_calls(messages, tool_calls, available_functions)

        # Second call after tool responses to get final output
        second_response = client.chat.completions.create(
            model=llm_model,
            messages=messages,
        )
        assistant_message = second_response.choices[0].message.content
    else:
        assistant_message = response_message.content

    # Clean up and update messages
    cleaned_text = postprocess_message(assistant_message)

    messages.append({"role": "assistant", "content": assistant_message})

    return messages, cleaned_text


def process(user_message, chat_history, messages, function_descriptions, available_functions):
    """
    Gradio interface handler: interacts with OpenAI and updates chat history.
    """
    updated_messages, ai_message = ask_openai(
        llm_model="gpt-4o-mini",
        messages=messages,
        user_message=user_message,
        function_descriptions=function_descriptions,
        available_functions=available_functions
    )
    # Update chat history with user and assistant messages
    chat_history.append((user_message, ai_message))
    return "", chat_history

