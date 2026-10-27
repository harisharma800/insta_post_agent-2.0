from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()


def get_google_output(input_prompt):

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        temperature=0.5,
    )

    # First prompt: Generate quote
    prompt1 = ChatPromptTemplate.from_messages([
        (
            "system",
            "Write a motivational quote in Hindi for someone "
            "struggling to find their purpose in life. "
            "Use 10-30 words."
        ),
        ("human", "{input}"),
    ])

    # Second prompt: Improve quote
    prompt2 = ChatPromptTemplate.from_messages([
        (
            "system",
            "Improve this Hindi motivational quote. "
            "Correct errors and make it powerful and inspiring. "
            "Keep it between 10 and 30 words. Return only the quote."
        ),
        ("human", "{quote}"),
    ])

    # Create chains
    chain1 = prompt1 | llm | StrOutputParser()
    chain2 = prompt2 | llm | StrOutputParser()

    # Execute chains
    response1 = chain1.invoke({"input": input_prompt})
    response2 = chain2.invoke({"quote": response1})

    print("Run successfully")
    return response2


