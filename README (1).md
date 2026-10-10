An AI-powered multi-agent application built with **Streamlit**, **LangChain**, and **OpenAI**. The application generates long-form stories chapter by chapter while maintaining character trait consistency and plot coherence using a structured memory system and an automated continuity review loop.

---



- **Structured Character Registry:** Store character sheets (personality, backstory, visual traits) as structured JSON data.
- **Dynamic Prompt Injection:** Automatically injects registered character traits into chapter generation prompts.
- **Interactive Plot Steering:** Allows users to define plot directions at chapter boundaries.
- **Automated Review Agent Loop:** An editor agent inspects each chapter draft for character deviations, continuity errors, and narrative gaps.
- **eBook Export:** Compiles completed multi-chapter story drafts into formatted `.epub` files.
- **Modern UI:** Responsive dashboard featuring real-time word counters, character badges, and custom dark mode styling.

---

- **Frontend & UI:** Streamlit[cite: 1]
- **LLM Orchestration:** LangChain, LangChain-OpenAI[cite: 1]
- **AI Models:** OpenAI `gpt-4o-mini`[cite: 1]
- **eBook Compilation:** `ebooklib`[cite: 1]
- **Environment Management:** `python-dotenv`

---


```text
story_generator/
│
├── app.py                 # Streamlit web application & UI layout
├── requirements.txt       # Project dependencies
├── .env                   # Environment variable configuration (API keys)
├── .gitignore             # File exclusion rules for Git
├── README.md              # Project documentation
│
├── data/
│   └── characters.json    # Structured JSON storage for character profiles
│
├── agents/
│   ├── generator.py       # Chapter writing agent with trait injection
│   └── reviewer.py        # Continuity and trait verification agent
│
├── utils/
│   ├── character_manager.py # JSON read/write and prompt formatting utilities
│   └── epub_exporter.py   # EPUB compilation logic
│
└── outputs/               # Directory for exported .epub eBook files