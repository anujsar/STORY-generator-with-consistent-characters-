import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.character_manager import format_character_sheet_for_prompt

load_dotenv()

def generate_chapter(story_title: str, chapter_number: int, plot_direction: str, previous_summary: str = "") -> str:
    """
    Generates a story chapter given the character registry, previous story context,
    and user plot direction.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
    
    character_context = format_character_sheet_for_prompt()
    
    system_prompt = (
        "You are an expert fiction author. Your task is to write Chapter {chapter_number} for the story titled '{story_title}'.\n\n"
        "=== CHARACTER REGISTRY ===\n"
        "{character_context}\n"
        "=========================\n\n"
        "STRICT CHARACTER CONSISTENCY RULES:\n"
        "1. Maintain character personality, backstory, and visual traits accurately.\n"
        "2. Do not introduce character contradictions.\n"
        "3. Keep tone engaging, descriptive, and well-paced."
    )
    
    user_prompt = (
        "Previous Story Context:\n{previous_summary}\n\n"
        "Plot Direction for Chapter {chapter_number}:\n{plot_direction}\n\n"
        "Write the full chapter text now:"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "story_title": story_title,
        "chapter_number": chapter_number,
        "character_context": character_context,
        "previous_summary": previous_summary if previous_summary else "This is the start of the story.",
        "plot_direction": plot_direction
    })
    
    return response