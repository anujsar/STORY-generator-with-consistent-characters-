import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from utils.character_manager import format_character_sheet_for_prompt

load_dotenv()

def review_chapter(chapter_text: str) -> str:
    """
    Reviews a chapter draft for continuity errors, character inconsistencies, and plot gaps.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    character_context = format_character_sheet_for_prompt()
    
    system_prompt = (
        "You are an expert literary editor and continuity reviewer.\n\n"
        "=== REGISTERED CHARACTERS ===\n"
        "{character_context}\n"
        "=============================\n\n"
        "Your role is to inspect the chapter text and identify any continuity errors, "
        "character trait deviations, or plot logic inconsistencies. "
        "If no issues are found, state that the chapter passes review with no errors."
    )
    
    user_prompt = (
        "Review the following chapter draft:\n\n"
        "{chapter_text}\n\n"
        "Provide a clear feedback report on:\n"
        "1. Continuity & Character Trait Consistency\n"
        "2. Plot Logic & Narrative Flow\n"
        "3. Specific improvement recommendations (if any)"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "character_context": character_context,
        "chapter_text": chapter_text
    })
    
    return response