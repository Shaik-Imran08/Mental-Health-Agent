import streamlit as st
from datetime import datetime
from utils.openai_client import OpenAIClient
from data.journal_prompts import JOURNAL_PROMPTS, CBT_PROMPTS

def render_journal_prompts():
    """Render guided journaling interface with CBT-based prompts"""
    
    st.header("📝 Guided Journaling")
    st.markdown("Explore your thoughts and feelings through guided reflection. Journaling can help you process emotions and gain insights.")
    
    # Initialize OpenAI client
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = OpenAIClient()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["✍️ New Entry", "📚 Your Entries", "🤖 AI-Personalized"])
    
    with tab1:
        render_new_journal_entry()
    
    with tab2:
        render_journal_history()
    
    with tab3:
        render_ai_personalized_prompts()

def render_new_journal_entry():
    """Render interface for creating new journal entry"""
    
    st.subheader("Choose Your Journaling Focus")
    
    # Focus area selection
    focus_areas = {
        "🎭 Emotional Awareness": "emotional_awareness",
        "🧠 Thought Patterns": "thought_patterns", 
        "🙏 Gratitude & Positivity": "gratitude",
        "💪 Coping & Resilience": "coping_skills",
        "🎯 Goals & Growth": "goals",
        "👥 Relationships": "relationships",
        "🌅 Daily Reflection": "daily_reflection"
    }
    
    selected_focus = st.selectbox(
        "What would you like to focus on today?",
        options=list(focus_areas.keys())
    )
    
    focus_key = focus_areas[selected_focus]
    
    # Get prompts for selected focus area
    available_prompts = JOURNAL_PROMPTS.get(focus_key, [])
    cbt_prompts = CBT_PROMPTS.get(focus_key, [])
    
    # Combine and select prompt
    all_prompts = available_prompts + cbt_prompts
    
    if all_prompts:
        # Random prompt selection or user choice
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_prompt = st.selectbox(
                "Choose a prompt or get a random one:",
                options=["🎲 Surprise me with a random prompt"] + all_prompts
            )
        
        with col2:
            if st.button("🔄 New Random Prompt"):
                import random
                selected_prompt = random.choice(all_prompts)
                st.rerun()
    else:
        selected_prompt = "What's on your mind today? Write about anything that feels important to you right now."
    
    # Display the prompt
    if selected_prompt.startswith("🎲"):
        import random
        actual_prompt = random.choice(all_prompts) if all_prompts else "What are you grateful for today?"
    else:
        actual_prompt = selected_prompt
    
    st.markdown("### 💭 Your Prompt")
    st.info(f"**{actual_prompt}**")
    
    # Pre-writing mood check
    st.subheader("How are you feeling before writing?")
    
    col1, col2 = st.columns(2)
    with col1:
        mood_before = st.slider(
            "Mood before writing (1-10)",
            min_value=1,
            max_value=10,
            value=5,
            key="mood_before"
        )
    
    with col2:
        emotional_state = st.selectbox(
            "Primary emotion right now:",
            ["Calm", "Anxious", "Sad", "Happy", "Frustrated", "Confused", "Motivated", "Tired", "Other"]
        )
    
    # Writing area
    st.subheader("✍️ Your Reflection")
    
    journal_content = st.text_area(
        "Write your thoughts here...",
        placeholder="Take your time and write whatever comes to mind. There's no right or wrong way to respond to the prompt.",
        height=300,
        key="journal_content"
    )
    
    # Follow-up questions
    insights = ""
    if journal_content:
        st.subheader("🤔 Follow-up Reflection")
        
        follow_up_prompts = [
            "What emotions came up while writing this?",
            "What insights or patterns do you notice?",
            "How might you apply this reflection to your daily life?",
            "What would you tell a friend in a similar situation?"
        ]
        
        insights = st.text_area(
            "Optional: Reflect on these questions:",
            placeholder="\n".join(f"• {prompt}" for prompt in follow_up_prompts),
            height=150,
            key="insights"
        )
    
    # Post-writing mood check
    st.subheader("How are you feeling after writing?")
    
    mood_after = st.slider(
        "Mood after writing (1-10)",
        min_value=1,
        max_value=10,
        value=mood_before,
        key="mood_after"
    )
    
    # Save entry
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("💾 Save Entry", type="primary"):
            if journal_content.strip():
                entry_data = {
                    "prompt": actual_prompt,
                    "content": journal_content,
                    "focus_area": focus_key,
                    "mood_before": mood_before,
                    "mood_after": mood_after,
                    "emotional_state": emotional_state,
                    "insights": insights if journal_content else ""
                }
                
                st.session_state.data_manager.save_journal_entry(entry_data)
                st.success("Journal entry saved! 📖")
                
                # Show mood change if significant
                mood_change = mood_after - mood_before
                if mood_change > 1:
                    st.balloons()
                    st.success(f"Great! Your mood improved by {mood_change} points through journaling! 📈")
                elif mood_change < -1:
                    st.info("Writing can sometimes bring up difficult emotions. That's okay and part of the healing process. 💙")
                
            else:
                st.warning("Please write something before saving.")
    
    with col2:
        if st.button("🗑️ Clear"):
            st.rerun()

def render_journal_history():
    """Display previous journal entries"""
    
    if not st.session_state.journal_entries:
        st.info("📝 Your journal entries will appear here once you start writing!")
        return
    
    st.subheader("📚 Your Journal History")
    
    # Sort entries by date (newest first)
    sorted_entries = sorted(
        st.session_state.journal_entries, 
        key=lambda x: x["timestamp"], 
        reverse=True
    )
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        focus_filter = st.selectbox(
            "Filter by focus area:",
            ["All"] + list(set(entry.get("focus_area", "general") for entry in sorted_entries))
        )
    
    with col2:
        date_range = st.selectbox(
            "Time period:",
            ["All time", "Last 7 days", "Last 30 days", "Last 3 months"]
        )
    
    # Apply filters
    filtered_entries = sorted_entries
    
    if focus_filter != "All":
        filtered_entries = [e for e in filtered_entries if e.get("focus_area") == focus_filter]
    
    if date_range != "All time":
        from datetime import timedelta
        days_map = {"Last 7 days": 7, "Last 30 days": 30, "Last 3 months": 90}
        cutoff = datetime.now() - timedelta(days=days_map[date_range])
        filtered_entries = [
            e for e in filtered_entries 
            if datetime.fromisoformat(e["timestamp"]) >= cutoff
        ]
    
    # Display entries
    for entry in filtered_entries:
        with st.expander(
            f"📝 {datetime.fromisoformat(entry['timestamp']).strftime('%B %d, %Y at %I:%M %p')} - {entry.get('focus_area', 'general').replace('_', ' ').title()}"
        ):
            # Prompt
            st.markdown(f"**Prompt:** {entry.get('prompt', 'Free writing')}")
            
            # Mood change
            mood_before = entry.get('mood_before', 0)
            mood_after = entry.get('mood_after', 0)
            mood_change = mood_after - mood_before
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mood Before", mood_before)
            with col2:
                st.metric("Mood After", mood_after, f"{mood_change:+d}")
            with col3:
                emotional_state = entry.get('emotional_state', 'Not recorded')
                st.write(f"**Emotional State:** {emotional_state}")
            
            # Content
            st.markdown("**Your Writing:**")
            st.write(entry.get('content', ''))
            
            # Insights
            if entry.get('insights'):
                st.markdown("**Your Insights:**")
                st.write(entry.get('insights'))
            
            # Delete option
            if st.button(f"🗑️ Delete Entry", key=f"delete_{entry.get('id', 0)}"):
                st.session_state.journal_entries = [
                    e for e in st.session_state.journal_entries 
                    if e.get('id') != entry.get('id')
                ]
                st.rerun()
    
    # Export option
    if st.button("📊 Export Journal Entries"):
        import json
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_entries": len(st.session_state.journal_entries),
            "entries": st.session_state.journal_entries
        }
        
        st.download_button(
            label="Download Journal Data",
            data=json.dumps(export_data, indent=2),
            file_name=f"journal_entries_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

def render_ai_personalized_prompts():
    """Generate AI-personalized journal prompts based on user data"""
    
    st.subheader("🤖 AI-Personalized Prompts")
    st.markdown("Get journal prompts tailored to your recent mood patterns and entries.")
    
    # Check if we have enough data
    if len(st.session_state.mood_entries) < 2 and len(st.session_state.journal_entries) < 1:
        st.info("""
        🔄 **Not enough data yet!**
        
        To get personalized prompts, try:
        - Log a few mood entries in the Mood Tracker
        - Write at least one journal entry
        - Use the chat support feature
        
        This helps the AI understand your patterns and create better prompts for you.
        """)
        return
    
    # Generate personalized prompt
    if st.button("✨ Generate Personalized Prompt", type="primary"):
        with st.spinner("Creating your personalized prompt..."):
            
            # Gather user data for context
            recent_moods = st.session_state.data_manager.get_recent_mood_data(7)
            recent_themes = st.session_state.data_manager.get_journal_themes()
            
            mood_context = {
                "recent_average": sum(m["overall_mood"] for m in recent_moods) / len(recent_moods) if recent_moods else 5,
                "common_emotions": [m.get("emotions", []) for m in recent_moods],
                "triggers": [m.get("triggers", []) for m in recent_moods]
            }
            
            # Generate AI prompt
            try:
                personalized_prompt = st.session_state.openai_client.generate_personalized_journal_prompt(
                    mood_context, 
                    recent_themes[:3]  # Top 3 themes
                )
                
                st.success("✨ Your Personalized Prompt")
                st.info(f"**{personalized_prompt['prompt']}**")
                
                # Follow-up questions
                if personalized_prompt.get('follow_up_questions'):
                    st.markdown("**Consider these follow-up questions:**")
                    for i, question in enumerate(personalized_prompt['follow_up_questions'], 1):
                        st.write(f"{i}. {question}")
                
                # Focus area
                focus_area = personalized_prompt.get('focus_area', 'general')
                st.caption(f"Focus area: {focus_area.replace('_', ' ').title()}")
                
                # Option to use this prompt
                if st.button("📝 Use This Prompt"):
                    st.session_state.ai_generated_prompt = personalized_prompt['prompt']
                    st.session_state.ai_focus_area = focus_area
                    st.info("Prompt saved! Go to 'New Entry' tab to use it.")
                
            except Exception as e:
                st.error("Unable to generate personalized prompt right now. Try one of the pre-written prompts instead!")
    
    # Show recent patterns that inform personalization
    st.subheader("📊 Patterns We Noticed")
    
    if st.session_state.mood_entries:
        recent_moods = st.session_state.data_manager.get_recent_mood_data(7)
        if recent_moods:
            avg_mood = sum(m["overall_mood"] for m in recent_moods) / len(recent_moods)
            
            if avg_mood < 4:
                st.write("💙 You've been experiencing some lower moods lately. Prompts will focus on self-compassion and coping strategies.")
            elif avg_mood > 7:
                st.write("😊 You've been in good spirits! Prompts will help you reflect on what's working well and build resilience.")
            else:
                st.write("⚖️ Your mood has been moderate. Prompts will help you explore balance and identify what supports your wellbeing.")
    
    if st.session_state.journal_entries:
        themes = st.session_state.data_manager.get_journal_themes()
        if themes:
            top_theme = themes[0][0].replace('_', ' ').title()
            st.write(f"📝 You've been writing a lot about {top_theme}. Prompts may explore this area further or suggest new perspectives.")
    
    # Tips for better personalization
    with st.expander("💡 Tips for Better Personalized Prompts"):
        st.markdown("""
        **To get the most relevant prompts:**
        
        🎯 **Be consistent**: Regular mood logging and journaling helps the AI understand your patterns
        
        📊 **Track variety**: Log different types of emotions and experiences for diverse prompts
        
        💭 **Be honest**: Authentic entries lead to more helpful prompts
        
        🔄 **Give feedback**: Use or skip prompts to help the system learn your preferences
        
        ⏰ **Use regularly**: The more data over time, the better the personalization becomes
        """)
