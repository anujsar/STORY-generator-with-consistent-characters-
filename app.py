import streamlit as st
import os
from utils.character_manager import save_character, load_characters
from agents.generator import generate_chapter
from agents.reviewer import review_chapter
from utils.epub_exporter import create_epub_file

st.set_page_config(
    page_title="Story Generator AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Imports & Base Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero Title Styling */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #311b92 50%, #4a148c 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(120deg, #a7f3d0, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* Custom Cards */
    .custom-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Character Pill Badges */
    .char-badge {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* Review Box Styling */
    .review-card {
        background-color: #0f172a;
        border-left: 4px solid #a855f7;
        padding: 1rem 1.25rem;
        border-radius: 0 8px 8px 0;
        margin-top: 1rem;
    }

    /* Primary Accent Divider */
    hr {
        border-color: #334155 !important;
        margin: 2rem 0 !important;
    }
</style>
""", unsafe_allow_html=True)


if "story_title" not in st.session_state:
    st.session_state.story_title = ""
if "chapters" not in st.session_state:
    st.session_state.chapters = []


st.markdown("""
<div class="hero-container">
    <div class="hero-title">✨ Story Generator AI</div>
    <div class="hero-subtitle">Draft multi-chapter stories with consistent characters, dynamic plot steering, and AI review agent loops.</div>
</div>
""", unsafe_allow_html=True)


st.sidebar.markdown("## 🎭 Character Registry")
st.sidebar.caption("Define character sheets to enforce trait continuity across all chapters.")

with st.sidebar.form("add_character_form", clear_on_submit=True):
    st.markdown("### ➕ Add / Update Character")
    char_name = st.text_input("Character Name", placeholder="e.g. Captain Vane")
    char_personality = st.text_area("Personality Traits", placeholder="e.g. Courageous, skeptical, highly analytical", height=80)
    char_backstory = st.text_area("Backstory", placeholder="e.g. Former naval strategist who went rogue after...", height=80)
    char_visuals = st.text_area("Visual Traits", placeholder="e.g. Tall, wears an antique bronze watch, scar over left eye", height=80)
    
    submit_char = st.form_submit_button("💾 Save Character Sheet", use_container_width=True)

    if submit_char:
        if char_name.strip():
            save_character(char_name, char_personality, char_backstory, char_visuals)
            st.sidebar.success(f"Successfully saved **{char_name}**!")
            st.rerun()
        else:
            st.sidebar.error("Please provide at least a character name.")

st.sidebar.divider()
st.sidebar.markdown("### 📋 Registered Cast")

existing_chars = load_characters()
if existing_chars:
    for c in existing_chars:
        with st.sidebar.expander(f"👤 {c['name']}"):
            st.markdown(f"<span class='char-badge'>NAME</span> **{c['name']}**", unsafe_allow_html=True)
            st.markdown(f"**Personality:** {c['personality'] if c['personality'] else 'N/A'}")
            st.markdown(f"**Backstory:** {c['backstory'] if c['backstory'] else 'N/A'}")
            st.markdown(f"**Visuals:** {c['visual_traits'] if c['visual_traits'] else 'N/A'}")
else:
    st.sidebar.info("No characters added yet. Use the form above to add your first character.")


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Characters Registered", len(existing_chars), delta="Cast Members")
with col2:
    st.metric("Chapters Generated", len(st.session_state.chapters), delta="Progress")
with col3:
    total_words = sum(len(ch["text"].split()) for ch in st.session_state.chapters)
    st.metric("Total Story Word Count", f"{total_words:,} words")

st.divider()




st.markdown("### ⚙️ Step 1: Story Setup")
setup_col1, setup_col2 = st.columns(2)

with setup_col1:
    story_title_input = st.text_input("📖 Story Title", value=st.session_state.story_title, placeholder="e.g. The Quantum Chronicles")
    if story_title_input:
        st.session_state.story_title = story_title_input

with setup_col2:
    author_name_input = st.text_input("✍️ Author Name", value="MCA Student", placeholder="Your name or pen name")

st.divider()


current_chapter_num = len(st.session_state.chapters) + 1
st.markdown(f"### 🎬 Step 2: Steering & Generation (Chapter {current_chapter_num})")

previous_context = ""
if st.session_state.chapters:
    previous_context = "\n\n".join(
        [f"Chapter {c['chapter_num']}:\n{c['text'][:300]}..." for c in st.session_state.chapters]
    )

plot_direction = st.text_area(
    f"🗺️ Plot Steering Instructions for Chapter {current_chapter_num}:",
    placeholder="Describe what key events, conflicts, or dialogue should occur in this chapter...",
    height=100
)

if st.button(f"🚀 Generate & Review Chapter {current_chapter_num}", type="primary", use_container_width=True):
    if not st.session_state.story_title.strip():
        st.error("⚠️ Please specify a Story Title in Step 1 before generating.")
    elif not plot_direction.strip():
        st.error("⚠️ Please enter a plot direction for this chapter.")
    else:
        with st.status("🧠 Processing Chapter Workflow...", expanded=True) as status:
            st.write("📖 Injecting character sheets and generating text...")
            chapter_text = generate_chapter(
                story_title=st.session_state.story_title,
                chapter_number=current_chapter_num,
                plot_direction=plot_direction,
                previous_summary=previous_context
            )
            
            st.write("🔍 Running Review Agent continuity & consistency check...")
            review_report = review_chapter(chapter_text)
            
            status.update(label="✅ Chapter generated and reviewed successfully!", state="complete", expanded=False)
        
        
        st.session_state.chapters.append({
            "chapter_num": current_chapter_num,
            "plot_direction": plot_direction,
            "text": chapter_text,
            "review": review_report
        })
        st.toast(f"Chapter {current_chapter_num} added!", icon="🎉")
        st.rerun()

st.divider()


st.markdown("### 📜 Step 3: Story Manuscript & Continuity Log")

if st.session_state.chapters:
    for ch in st.session_state.chapters:
        with st.container():
            st.markdown(f"#### 📖 Chapter {ch['chapter_num']}")
            st.caption(f"**Plot Directive:** {ch['plot_direction']}")
            
            
            st.markdown(f"<div class='custom-card'>{ch['text']}</div>", unsafe_allow_html=True)
            
            
            with st.expander(f"🔍 View Review Agent Continuity Report (Chapter {ch['chapter_num']})"):
                st.markdown(f"<div class='review-card'>{ch['review']}</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
    st.divider()
    

    st.markdown("### 📦 Step 4: Export eBook")
    clean_filename = st.session_state.story_title.lower().replace(" ", "_") + ".epub"
    
    export_col1, export_col2 = st.columns([1, 2])
    
    with export_col1:
        if st.button("🔨 Build .epub eBook File", use_container_width=True):
            file_path = create_epub_file(
                title=st.session_state.story_title,
                author=author_name_input,
                chapters=st.session_state.chapters,
                output_filename=clean_filename
            )
            st.success(f"eBook generated at `{file_path}`!")
            
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Download .epub eBook",
                    data=f,
                    file_name=clean_filename,
                    mime="application/epub+zip",
                    use_container_width=True
                )
else:
    st.info("No chapters generated yet. Complete Steps 1 & 2 above to begin writing your story.")