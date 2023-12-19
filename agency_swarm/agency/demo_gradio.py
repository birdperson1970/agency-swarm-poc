  

from agency_swarm.agency.agency import Agency


def demo_gradio(agency: Agency, height=600):
    """
    Launches a Gradio-based demo interface for the agency chatbot.

    Parameters:
    height (int, optional): The height of the chatbot widget in the Gradio interface. Default is 600.

    This method sets up and runs a Gradio interface, allowing users to interact with the agency's chatbot. It includes a text input for the user's messages and a chatbot interface for displaying the conversation. The method handles user input and chatbot responses, updating the interface dynamically.
    """
    try:
        import gradio as gr
    except ImportError:
        raise Exception("Please install gradio: pip install gradio")

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot(height=height)
        msg = gr.Textbox()

        def user(user_message, history):
            # Append the user message with a placeholder for bot response
            user_message = "👤 User: " + user_message.strip()
            return "", history + [[user_message, None]]

        def bot(history):
            # Replace this with your actual chatbot logic
            gen = agency.get_completion(message=history[-1][0])

            try:
                # Yield each message from the generator
                for bot_message in gen:
                    if bot_message.sender_name.lower() == "user":
                        continue

                    message = bot_message.get_sender_emoji() + " " + bot_message.get_formatted_content()

                    history.append((None, message))
                    yield history
            except StopIteration:
                # Handle the end of the conversation if necessary
                pass

        # Chain the events
        msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )

        # Enable queuing for streaming intermediate outputs
        demo.queue()

    # Launch the demo
    demo.launch()