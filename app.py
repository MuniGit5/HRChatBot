"""James Shield HR Assistant - Streamlit app."""

import html
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag import get_answer, build_vector_store

load_dotenv()

# Page config
st.set_page_config(
    page_title="James Shield HR Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Topics with their questions - click topic to see questions, click question to get answer (3 per topic)
TOPICS = {
    "PTO": [
        "How much PTO do I accrue each pay period?",
        "Do unused PTO hours carry over to next year?",
        "How do I request PTO and who needs to approve it?",
        "How much sick leave do I receive and when can I use it?",
    ],
    "Holidays": [
        "Which holidays are paid by the company?",
        "What happens if a holiday falls on a weekend?",
        "Do we get floating holidays, and how do I use them?",
    ],
    "Benefits": [
        "When am I eligible for health insurance benefits?",
        "How do I enroll or make changes to my benefits?",
        "Does the company offer dental and vision coverage?",
    ],
    "New Hire": [
        "How do I request time off as a new employee?",
        "When do my benefits start and how do I enroll?",
        "Who should I contact if I have questions during onboarding?",
    ],
    "Chemical Spill": [
        "What should I do if a chemical spill occurs at work?",
        "Who do I report a chemical spill to?",
        "What safety equipment is required for chemical cleanup?",
    ],
    "Company Vehicle": [
        "Who is eligible for a company vehicle?",
        "What are the rules for using a company vehicle?",
        "What should I do if I'm in an accident in a company vehicle?",
    ],
    "FMLA": [
        "What is FMLA and who is eligible?",
        "How do I request FMLA leave?",
        "How much FMLA leave am I entitled to?",
    ],
    "Escalations": [
        "How do I escalate an HR issue?",
        "Who do I contact for HR escalations?",
        "When should I escalate a concern to HR?",
    ],
    "Workplace Conduct": [
        "What are the workplace conduct expectations?",
        "How do I report harassment or discrimination?",
        "What is the policy on workplace ethics?",
    ],
    "Remote Work": [
        "Am I eligible to work remotely or hybrid?",
        "What are the expected working hours for remote employees?",
        "Does the company reimburse home office equipment?",
    ],
    "Reimbursement": [
        "How do I submit expense reimbursements?",
        "What expenses are reimbursable?",
        "What is the reimbursement process and timeline?",
    ],
}

# FAQ questions - click to search handbook and show answer
FAQS = [
    "What is the procedure if I am going to be late to work?",
    "When am I eligible for benefits?",
    "What happens if I forget to clock in or clock out?",
    "Can I make up missed hours later in the week?",
    "Do I need a doctor's note to return to work?",
    "When am I eligible to start using my vacation time?",
    "How much sick leave do I receive each year?",
    "Do unused vacation or sick days carry over?",
    "What do I do if I'm injured on the job?",
    "How many vacation days do I get?",
    "When does my health insurance coverage begin?",
    "When can I change my insurance plans?",
    "What happens to my benefits if I leave the company?",
    "What holidays do I have off?",
    "What should I do if I witness harassment or discrimination?",
    "How do I report a safety concern?",
    "When are we paid?",
    "When am I eligible for the 401(k)?",
    "Who is eligible to work remotely?",
    "How is my performance evaluated when working from home?",
]

# Custom CSS - professional corporate theme
st.markdown("""
<style>
    /* Main app - clean neutral background */
    .stApp { background-color: #fafafa; }
    
    /* Header area */
    .header-container { 
        padding: 1.5rem 0; 
        border-bottom: 1px solid #e9ecef; 
        margin-bottom: 1.5rem;
    }
    .subtitle { 
        color: #6c757d; 
        font-size: 0.95rem; 
        margin-top: 0.25rem; 
        letter-spacing: 0.02em;
        font-weight: 400;
    }
    .start-here { 
        font-size: 1.125rem; 
        font-weight: 600; 
        text-align: center; 
        margin: 1.25rem 0 0.5rem; 
        color: #212529;
        letter-spacing: 0.02em;
    }
    .choose-prompt { 
        text-align: center; 
        color: #6c757d; 
        margin-bottom: 1.5rem; 
        font-size: 0.9rem;
    }
    
    /* Topic buttons - refined card style */
    [data-testid="stVerticalBlock"] > div > div > button {
        border-radius: 6px !important;
        border: 1px solid #dee2e6 !important;
        background: #ffffff !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stVerticalBlock"] > div > div > button:hover {
        border-color: #2d6a4f !important;
        background: #f8f9fa !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06) !important;
    }
    
    /* Q&A styling - professional cards */
    .qa-question { 
        background: #ffffff; 
        padding: 1.25rem 1.5rem; 
        border-radius: 6px; 
        margin: 0.75rem 0; 
        border: 1px solid #e9ecef;
        border-left: 4px solid #2d6a4f;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .qa-answer { 
        background: #ffffff; 
        padding: 1.25rem 1.5rem; 
        border-radius: 6px; 
        margin: 0.75rem 0; 
        border: 1px solid #e9ecef;
        border-left: 4px solid #40916c;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .qa-label { 
        font-weight: 600; 
        font-size: 0.7rem; 
        color: #2d6a4f; 
        margin-bottom: 0.35rem; 
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Sidebar refinements */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    
    /* Dividers */
    hr { border-color: #e9ecef !important; }
    
    /* Topic question buttons - subtle link style */
    button[kind="secondary"] {
        text-align: left !important;
        font-weight: 500 !important;
        color: #2d6a4f !important;
    }
    button[kind="secondary"]:hover {
        color: #1b4332 !important;
        background: #f8f9fa !important;
    }
</style>
""", unsafe_allow_html=True)


def is_index_built():
    """Check if ChromaDB vector store exists."""
    chroma_path = Path(__file__).parent / "chroma_db"
    return chroma_path.exists() and any(chroma_path.iterdir())


@st.dialog("FAQ Answer", width="medium")
def show_faq_popup(question: str, answer: str):
    st.markdown(f"**Question**")
    st.markdown(question)
    st.markdown("---")
    st.markdown("**Answer**")
    st.write(answer)
    st.markdown("")
    st.caption("_Disclaimer: Answers are based on company policy documents and are for informational purposes only. For official guidance, contact HR._")


def render_sidebar():
    """Render left sidebar with Index, FAQ, Help & scope, HR contact."""
    with st.sidebar:
        st.markdown("### Index")
        built = is_index_built()
        st.caption("Built" if built else "Not built")

        if st.button("Reset chat", use_container_width=True):
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()

        if st.button("Rebuild index", use_container_width=True):
            try:
                with st.spinner("Rebuilding..."):
                    build_vector_store()
                st.toast("Index rebuilt!")
            except Exception as e:
                st.error(str(e))

        st.divider()

        # History - dropdown to view all previous Q&As
        with st.expander("**History**", expanded=False):
            if st.session_state.get("messages"):
                for i in range(0, len(st.session_state.messages), 2):
                    if i + 1 < len(st.session_state.messages):
                        st.markdown(f"**Q:** {st.session_state.messages[i]['content']}")
                        st.write(st.session_state.messages[i + 1]["content"])
                        st.markdown("---")
            else:
                st.caption("_No questions yet. Ask a question to see history._")

        st.divider()

        # FAQ dropdown - expander with questions as clickable links
        st.markdown("### FAQs")
        with st.expander("View all questions", expanded=False):
            for i, faq in enumerate(FAQS):
                if st.button(
                    f"• {faq}",
                    key=f"faq_{i}",
                    use_container_width=True,
                    type="secondary",
                ):
                    with st.spinner("Searching the handbook..."):
                        answer = get_answer(faq)
                    show_faq_popup(faq, answer)

        st.divider()

        with st.expander("**Help & scope**", expanded=False):
            st.markdown("**Can help:** PTO, holidays, benefits, remote work, timekeeping, conduct, safety, onboarding")
            st.markdown("**Cannot help:** Individual pay, reviews, disciplinary, medical, legal, exceptions")

        with st.expander("**HR contact**"):
            st.markdown("[Email: HR@JamesShield.com](mailto:HR@JamesShield.com)")
            st.markdown("HR Hotline: 1-800-555-1234")

        st.divider()
        st.markdown("**Disclaimer**")
        st.caption("_Answers are based on company policy documents and are for informational purposes only. For official guidance, contact HR._")


def main():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "view" not in st.session_state:
        st.session_state.view = "topics"
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = None

    render_sidebar()

    # Main content - logo + heading
    col1, col2 = st.columns([1, 5])
    with col1:
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=90)
    with col2:
        st.markdown(
            '<h1 style="font-size: 1.75rem; font-weight: 600; color: #212529; letter-spacing: 0.02em; margin-bottom: 0;">JAMES SHIELD HR ASSISTANT</h1>',
            unsafe_allow_html=True,
        )
        st.markdown('<p class="subtitle">Policy Q&A from internal HR documents</p>', unsafe_allow_html=True)

    st.markdown('<p class="start-here">Start here</p>', unsafe_allow_html=True)
    st.markdown('<p class="choose-prompt">Choose a topic or type your own question below</p>', unsafe_allow_html=True)

    if st.session_state.view == "topics":
        # Topic buttons - 4 columns (11 topics + Something else)
        cols = st.columns(4)
        topic_items = list(TOPICS.keys()) + ["Something else"]
        for i, topic in enumerate(topic_items):
            with cols[i % 4]:
                if st.button(topic, key=f"topic_{topic}", use_container_width=True):
                    if topic == "Something else":
                        st.session_state.show_chat_hint = True
                    else:
                        st.session_state.selected_topic = topic
                        st.session_state.view = "questions"
                    st.rerun()
    else:
        # Questions view - show selected topic's questions
        topic = st.session_state.selected_topic
        if topic and topic in TOPICS:
            if st.button("← Back to Topics"):
                st.session_state.view = "topics"
                st.session_state.selected_topic = None
                st.rerun()

            st.markdown(f"### {topic}")
            st.caption("Click a question to get the answer from the handbook.")
            for i, q in enumerate(TOPICS[topic]):
                if st.button(q, key=f"q_{topic}_{i}", use_container_width=True, type="secondary"):
                    with st.spinner("Searching the handbook..."):
                        answer = get_answer(q)
                    st.session_state.messages.append({"role": "user", "content": q})
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    st.rerun()

    if st.session_state.get("show_chat_hint"):
        st.info("Type your question in the chat input below.")

    st.markdown("---")

    # Latest Q&A only - no scrolling for new questions
    if st.session_state.messages:
        last_q = st.session_state.messages[-2]["content"]
        last_a = st.session_state.messages[-1]["content"]
        q_content = html.escape(last_q).replace("\n", "<br>")
        a_content = html.escape(last_a).replace("\n", "<br>")
        st.markdown(
            f'<div class="qa-question"><div class="qa-label">QUESTION</div>{q_content}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="qa-answer"><div class="qa-label">ANSWER</div>{a_content}</div>',
            unsafe_allow_html=True,
        )
        st.caption("_Disclaimer: Answers are based on company policy documents and are for informational purposes only. For official guidance, contact HR._")

    # Chat input at bottom
    if prompt := st.chat_input("Ask an HR policy question..."):
        st.session_state.show_chat_hint = False
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Searching the handbook..."):
            answer = get_answer(prompt)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


if __name__ == "__main__":
    main()
