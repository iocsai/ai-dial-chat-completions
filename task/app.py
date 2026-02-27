import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    # 1.1. Create DialClient
    dial_client = DialClient(ID)

    # 1.2. Create CustomDialClient
    custom_dial_client = DialClient(ID)

    # 2. Create Conversation object
    conversation = Conversation()

    # 3. Get System prompt from console
    #    or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation messages.
    print("System prompt please or 'enter' to continue with default")
    prompt = input(">_ ").strip()

    if prompt:
        conversation.add_message(Message(Role.SYSTEM, prompt))
        print("System prompt added to conversation.")
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(f"No System prompt provided. Will be used default System prompt: '{DEFAULT_SYSTEM_PROMPT}'")

    # 9. Test it with DialClient and CustomDialClient
    await ai_conversation(conversation, custom_dial_client, stream)
    await ai_conversation(conversation, dial_client, stream)

    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response


async def ai_conversation(conversation: Conversation, custom_dial_client: DialClient, stream: bool):
    # 4. Use infinite cycle (while True) and get yser message from console
    print("Your question: (type 'exit' to quit)")
    while True:
        user_question = input(">_ ").strip()

        # 5. If user message is `exit` then stop the loop
        if user_question.lower() == "exit":
            break

        # 6. Add user message to conversation history (role 'user')
        conversation.add_message(Message(Role.SYSTEM, user_question))

        # 7. If `stream` param is true -> call DialClient#stream_completion()
        #    else -> call DialClient#get_completion()
        print("The secret you were curious about: ")
        if stream:
            ai_answer = await custom_dial_client.stream_completion(conversation.get_messages())
        else:
            ai_answer = custom_dial_client.get_completion(conversation.get_messages())

        # 8. Add generated message to history
        conversation.add_message(ai_answer)


ID = "gpt-4o"


asyncio.run(
    start(True)
)
