import streamlit as st
from datetime import datetime
from utils.openai_client import OpenAIClient
from data.cbt_prompts import CBT_EXERCISES, COGNITIVE_DISTORTIONS

def render_cbt_exercises():
    """Render CBT exercises and thought record interface"""
    
    st.header("🧠 CBT Exercises")
    st.markdown("Learn and practice Cognitive Behavioral Therapy (CBT) techniques to understand and manage your thoughts and emotions.")
    
    # Initialize OpenAI client
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = OpenAIClient()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Thought Record", "🔍 Identify Patterns", "📚 Learn CBT", "📊 Your Progress"])
    
    with tab1:
        render_thought_record()
    
    with tab2:
        render_pattern_identification()
    
    with tab3:
        render_cbt_education()
    
    with tab4:
        render_cbt_progress()

def render_thought_record():
    """Render the 7-column thought record exercise"""
    
    st.subheader("📋 Thought Record Exercise")
    st.markdown("""
    A thought record helps you examine your thoughts and feelings about a situation. 
    Work through each step to gain perspective and develop more balanced thinking.
    """)
    
    # Step-by-step thought record
    with st.form("thought_record_form"):
        st.markdown("### 1. 📍 Situation")
        situation = st.text_area(
            "What happened? Describe the situation objectively.",
            placeholder="E.g., I got a lower grade than expected on my test",
            height=100
        )
        
        st.markdown("### 2. 😟 Emotions")
        col1, col2 = st.columns(2)
        
        with col1:
            emotions = st.multiselect(
                "What emotions did you feel?",
                ["Anxious", "Sad", "Angry", "Frustrated", "Disappointed", "Ashamed", "Guilty", "Worried", "Other"],
                help="Select all that apply"
            )
        
        with col2:
            intensity_before = st.slider(
                "How intense were these emotions? (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                key="intensity_before"
            )
        
        st.markdown("### 3. 💭 Automatic Thoughts")
        thoughts = st.text_area(
            "What thoughts went through your mind?",
            placeholder="E.g., I'm not smart enough, I'm going to fail this class, Everyone else is better than me",
            height=100
        )
        
        st.markdown("### 4. ✅ Evidence FOR the thought")
        evidence_for = st.text_area(
            "What evidence supports this thought?",
            placeholder="E.g., This was a difficult test, I didn't study as much as I should have",
            height=80
        )
        
        st.markdown("### 5. ❌ Evidence AGAINST the thought")
        evidence_against = st.text_area(
            "What evidence contradicts this thought?",
            placeholder="E.g., I've done well on tests before, One grade doesn't define my intelligence, I can improve with more studying",
            height=80
        )
        
        st.markdown("### 6. ⚖️ Balanced Thought")
        balanced_thought = st.text_area(
            "What's a more balanced, realistic way to think about this?",
            placeholder="E.g., This test was challenging and I didn't prepare as well as I could have, but one grade doesn't mean I'm not capable. I can learn from this and do better next time.",
            height=100
        )
        
        st.markdown("### 7. 😌 New Emotion Rating")
        intensity_after = st.slider(
            "How intense are your emotions now? (1-10)",
            min_value=1,
            max_value=10,
            value=intensity_before,
            key="intensity_after"
        )
        
        # Submit form
        submitted = st.form_submit_button("💾 Save Thought Record", type="primary")
        
        if submitted:
            if situation and thoughts:
                thought_record = {
                    "situation": situation,
                    "emotions": emotions,
                    "thoughts": thoughts,
                    "intensity_before": intensity_before,
                    "evidence_for": evidence_for,
                    "evidence_against": evidence_against,
                    "balanced_thought": balanced_thought,
                    "intensity_after": intensity_after
                }
                
                # Get AI insights
                with st.spinner("Getting AI insights..."):
                    ai_insights = st.session_state.openai_client.generate_cbt_insight(thought_record)
                    thought_record["ai_insights"] = ai_insights
                
                # Save the record
                st.session_state.data_manager.save_cbt_record(thought_record)
                
                st.success("Thought record saved! 📝")
                
                # Show improvement
                improvement = intensity_before - intensity_after
                if improvement > 0:
                    st.balloons()
                    st.success(f"Great work! Your emotional intensity decreased by {improvement} points! 📉")
                
                # Display AI insights
                st.markdown("### 🤖 AI Insights")
                
                if ai_insights.get("cognitive_distortions"):
                    st.write("**Possible cognitive distortions identified:**")
                    for distortion in ai_insights["cognitive_distortions"]:
                        st.write(f"• {distortion}")
                
                if ai_insights.get("balanced_thoughts"):
                    st.write("**Alternative balanced thoughts:**")
                    for thought in ai_insights["balanced_thoughts"]:
                        st.write(f"• {thought}")
                
                if ai_insights.get("coping_strategies"):
                    st.write("**Suggested coping strategies:**")
                    for strategy in ai_insights["coping_strategies"]:
                        st.write(f"• {strategy}")
                
                if ai_insights.get("encouragement"):
                    st.info(ai_insights["encouragement"])
                
            else:
                st.warning("Please fill in at least the situation and thoughts fields.")

def render_pattern_identification():
    """Help users identify cognitive distortions and thought patterns"""
    
    st.subheader("🔍 Identify Thought Patterns")
    st.markdown("Learn to recognize common thinking patterns that might be affecting your mood.")
    
    # Quick thought checker
    st.markdown("### 🔍 Quick Thought Checker")
    
    user_thought = st.text_area(
        "Enter a thought that's been bothering you:",
        placeholder="E.g., Everyone thinks I'm weird, I never do anything right, This always happens to me",
        height=100
    )
    
    if st.button("🔍 Analyze This Thought") and user_thought:
        with st.spinner("Analyzing thought patterns..."):
            # Simple pattern matching for common distortions
            identified_patterns = []
            
            thought_lower = user_thought.lower()
            
            # Check for common distortion patterns
            if any(word in thought_lower for word in ["always", "never", "everyone", "no one", "everything", "nothing"]):
                identified_patterns.append("All-or-Nothing Thinking")
            
            if any(word in thought_lower for word in ["should", "must", "have to", "ought to"]):
                identified_patterns.append("Should Statements")
            
            if any(phrase in thought_lower for phrase in ["i'm a", "i am a", "i'm so", "i am so"]):
                identified_patterns.append("Labeling")
            
            if any(word in thought_lower for word in ["terrible", "awful", "horrible", "disaster", "catastrophe"]):
                identified_patterns.append("Catastrophizing")
            
            if "what if" in thought_lower:
                identified_patterns.append("What-If Thinking")
            
            # Display results
            if identified_patterns:
                st.warning("🎯 **Possible thought patterns identified:**")
                for pattern in identified_patterns:
                    st.write(f"• **{pattern}**")
                    if pattern in COGNITIVE_DISTORTIONS:
                        st.write(f"  *{COGNITIVE_DISTORTIONS[pattern]['description']}*")
                        st.write(f"  💡 **Challenge:** {COGNITIVE_DISTORTIONS[pattern]['challenge']}")
            else:
                st.success("This thought seems relatively balanced! 👍")
            
            # Suggest reframing
            st.markdown("### 🔄 Try Reframing")
            st.info("""
            **Reframing questions to ask yourself:**
            - Is this thought realistic or exaggerated?
            - What evidence supports or contradicts this thought?
            - What would I tell a friend having this thought?
            - How might I think about this in a week or month?
            - What's a more balanced way to view this situation?
            """)
    
    # Common patterns reference
    st.markdown("### 📚 Common Thinking Patterns")
    
    with st.expander("🔍 Learn About Cognitive Distortions"):
        for name, info in COGNITIVE_DISTORTIONS.items():
            st.markdown(f"**{name}**")
            st.write(f"*{info['description']}*")
            st.write(f"**Example:** {info['example']}")
            st.write(f"**How to challenge it:** {info['challenge']}")
            st.write("---")

def render_cbt_education():
    """Educational content about CBT principles and techniques"""
    
    st.subheader("📚 Learn About CBT")
    st.markdown("Understand the principles behind Cognitive Behavioral Therapy and how it can help.")
    
    # CBT overview
    st.markdown("### 🧠 What is CBT?")
    st.info("""
    **Cognitive Behavioral Therapy (CBT)** is based on the idea that our thoughts, feelings, and behaviors are all connected. 
    By changing negative thought patterns, we can improve our emotions and behaviors.
    
    **The CBT Triangle:**
    - 💭 **Thoughts** influence how we feel
    - ❤️ **Feelings** influence how we act  
    - 🎬 **Behaviors** influence how we think
    """)
    
    # Core CBT techniques
    technique_tabs = st.tabs(["🔍 Thought Challenging", "📝 Behavioral Experiments", "🎯 Goal Setting", "🧘 Mindfulness"])
    
    with technique_tabs[0]:
        st.markdown("### 🔍 Thought Challenging")
        st.write("""
        **Purpose:** Question negative or unhelpful thoughts to develop more balanced thinking.
        
        **Steps:**
        1. **Notice** the thought
        2. **Examine** the evidence for and against it
        3. **Consider** alternative perspectives
        4. **Develop** a more balanced thought
        
        **Questions to ask:**
        - Is this thought realistic?
        - What would I tell a friend in this situation?
        - What's the worst/best/most likely outcome?
        - How will this matter in 5 years?
        """)
        
        if st.button("📋 Try a Thought Record"):
            st.info("Go to the 'Thought Record' tab to practice this technique!")
    
    with technique_tabs[1]:
        st.markdown("### 📝 Behavioral Experiments")
        st.write("""
        **Purpose:** Test negative beliefs through real-world experiments.
        
        **Example:**
        - **Belief:** "If I speak up in class, everyone will think I'm stupid"
        - **Experiment:** Ask one question in class and observe reactions
        - **Result:** Learn that most people don't judge as harshly as expected
        
        **How to design an experiment:**
        1. Identify the belief to test
        2. Predict what will happen
        3. Design a small, manageable test
        4. Carry out the experiment
        5. Reflect on the results
        """)
    
    with technique_tabs[2]:
        st.markdown("### 🎯 Goal Setting")
        st.write("""
        **Purpose:** Break down overwhelming problems into manageable steps.
        
        **SMART Goals:**
        - **S**pecific: Clear and well-defined
        - **M**easurable: You can track progress
        - **A**chievable: Realistic and attainable
        - **R**elevant: Important to you
        - **T**ime-bound: Has a deadline
        
        **Example:**
        Instead of "I want to be happier," try:
        "I will practice 10 minutes of mindfulness meditation every morning for the next week."
        """)
    
    with technique_tabs[3]:
        st.markdown("### 🧘 Mindfulness in CBT")
        st.write("""
        **Purpose:** Observe thoughts and feelings without judgment.
        
        **Benefits:**
        - Reduces rumination
        - Increases awareness of thought patterns
        - Helps with emotional regulation
        - Improves focus and attention
        
        **Simple mindfulness techniques:**
        - **5-4-3-2-1 Grounding:** Notice 5 things you see, 4 you hear, 3 you touch, 2 you smell, 1 you taste
        - **Breathing space:** Pause and take 3 mindful breaths
        - **Body scan:** Notice sensations from head to toe
        """)
        
        if st.button("🫁 Try Breathing Exercises"):
            st.info("Check out our 'Breathing & Mindfulness' section for guided exercises!")

def render_cbt_progress():
    """Show user's CBT exercise progress and insights"""
    
    if not st.session_state.cbt_records:
        st.info("📊 Your CBT progress will appear here once you complete some thought records!")
        return
    
    st.subheader("📊 Your CBT Progress")
    
    # Progress metrics
    total_records = len(st.session_state.cbt_records)
    
    # Calculate average improvement
    improvements = []
    for record in st.session_state.cbt_records:
        before = record.get("intensity_before", 5)
        after = record.get("intensity_after", 5)
        improvements.append(before - after)
    
    avg_improvement = sum(improvements) / len(improvements) if improvements else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Thought Records", total_records)
    
    with col2:
        st.metric("Average Improvement", f"{avg_improvement:.1f} points")
    
    with col3:
        successful_records = len([i for i in improvements if i > 0])
        success_rate = (successful_records / total_records * 100) if total_records > 0 else 0
        st.metric("Success Rate", f"{success_rate:.0f}%")
    
    # Recent records
    st.markdown("### 📋 Recent Thought Records")
    
    recent_records = sorted(
        st.session_state.cbt_records,
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )[:5]
    
    for i, record in enumerate(recent_records):
        with st.expander(f"Record {i+1}: {datetime.fromisoformat(record['timestamp']).strftime('%B %d, %Y')}"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Situation:** {record.get('situation', 'N/A')}")
                st.write(f"**Original Thought:** {record.get('thoughts', 'N/A')}")
            
            with col2:
                before = record.get('intensity_before', 0)
                after = record.get('intensity_after', 0)
                improvement = before - after
                
                st.metric("Intensity Before", before)
                st.metric("Intensity After", after, f"{-improvement:+.0f}")
            
            if record.get('balanced_thought'):
                st.write(f"**Balanced Thought:** {record['balanced_thought']}")
            
            # AI insights if available
            if record.get('ai_insights'):
                insights = record['ai_insights']
                if insights.get('encouragement'):
                    st.success(insights['encouragement'])
    
    # Progress visualization
    if len(st.session_state.cbt_records) >= 3:
        st.markdown("### 📈 Improvement Trends")
        
        import plotly.graph_objects as go
        
        dates = [datetime.fromisoformat(r['timestamp']).date() for r in st.session_state.cbt_records]
        improvements = [r.get('intensity_before', 5) - r.get('intensity_after', 5) for r in st.session_state.cbt_records]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=improvements,
            mode='lines+markers',
            name='Emotional Improvement',
            line=dict(color='green', width=2),
            marker=dict(size=8)
        ))
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="No change")
        
        fig.update_layout(
            title="Emotional Improvement Over Time",
            xaxis_title="Date",
            yaxis_title="Improvement (points)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Export option
    if st.button("📊 Export CBT Records"):
        import json
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_records": len(st.session_state.cbt_records),
            "average_improvement": avg_improvement,
            "records": st.session_state.cbt_records
        }
        
        st.download_button(
            label="Download CBT Data",
            data=json.dumps(export_data, indent=2),
            file_name=f"cbt_records_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
