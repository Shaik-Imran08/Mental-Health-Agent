import streamlit as st
from utils.openai_client import OpenAIClient
from utils.crisis_detection import CrisisDetector

def render_chat_interface():
    """Render the main chat interface with crisis detection"""
    
    st.header("💬 Chat Support")
    st.markdown("Choose your support style and start a conversation. Remember, this is a safe, anonymous space.")
    
    # Initialize components
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = OpenAIClient()
    
    if 'crisis_detector' not in st.session_state:
        st.session_state.crisis_detector = CrisisDetector()
    
    # Persona selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        peer_selected = st.button("👥 Peer Support", 
                                help="Chat with someone who understands what it's like to be your age")
    with col2:
        mentor_selected = st.button("🌟 Mentor", 
                                  help="Get guidance from a wise mentor figure")
    with col3:
        therapist_selected = st.button("🧑‍⚕️ Therapist", 
                                     help="Professional-style support with therapeutic techniques")
    
    # Set persona based on selection
    if peer_selected:
        st.session_state.current_persona = "peer"
    elif mentor_selected:
        st.session_state.current_persona = "mentor" 
    elif therapist_selected:
        st.session_state.current_persona = "therapist"
    elif 'current_persona' not in st.session_state:
        st.session_state.current_persona = "therapist"  # Default
    
    # Display current persona
    persona_emojis = {"peer": "👥", "mentor": "🌟", "therapist": "🧑‍⚕️"}
    persona_names = {"peer": "Peer Support", "mentor": "Mentor", "therapist": "Therapist"}
    
    st.info(f"Current support style: {persona_emojis[st.session_state.current_persona]} {persona_names[st.session_state.current_persona]}")
    
    # Chat history display
    st.subheader("💭 Conversation")
    
    # Create container for chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Show risk level indicator if present
                    if message.get("risk_level") and message["risk_level"] != "low":
                        risk_colors = {
                            "moderate": "🟡",
                            "high": "🟠", 
                            "critical": "🔴"
                        }
                        st.caption(f"{risk_colors.get(message['risk_level'], '')} Support level: {message['risk_level']}")
    
    # Chat input
    st.subheader("✍️ What's on your mind?")
    
    # Text input for user message
    user_input = st.text_area(
        "Share your thoughts, feelings, or what you're going through...",
        placeholder="I've been feeling anxious about...",
        height=100,
        key="chat_input"
    )
    
    # Send button
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        send_button = st.button("💬 Send", type="primary")
    
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Process user input
    if send_button and user_input.strip():
        # Save user message
        st.session_state.data_manager.save_chat_message("user", user_input)
        
        # Crisis detection
        risk_assessment = st.session_state.crisis_detector.analyze_text_for_crisis(user_input)
        
        # Trigger crisis intervention if needed
        crisis_detected = st.session_state.crisis_detector.trigger_crisis_intervention(risk_assessment)
        
        # Generate AI response
        conversation_history = st.session_state.data_manager.get_conversation_history()
        
        try:
            ai_response = st.session_state.openai_client.get_empathetic_response(
                user_input, 
                st.session_state.current_persona,
                conversation_history
            )
            
            # Add crisis follow-up if needed
            if crisis_detected:
                follow_up = st.session_state.crisis_detector.get_crisis_follow_up_message(
                    risk_assessment["final_risk_level"]
                )
                if ai_response:
                    ai_response = ai_response + f"\n\n{follow_up}"
                else:
                    ai_response = follow_up
            
            # Save AI response with risk level
            st.session_state.data_manager.save_chat_message(
                "assistant", 
                ai_response, 
                st.session_state.current_persona,
                risk_assessment["final_risk_level"]
            )
            
        except Exception as e:
            error_response = """
            I'm having trouble connecting right now. Here are some things you can try:
            
            🔄 Refresh the page and try again
            🫁 Try our breathing exercises
            📝 Write in the journal section
            🆘 If this is urgent, please call 988 or text HOME to 741741
            """
            
            st.session_state.data_manager.save_chat_message("assistant", error_response)
        
        # Clear input and refresh
        st.rerun()
    
    # Quick response buttons
    if not st.session_state.chat_history:
        st.subheader("🚀 Get started with...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("😟 I'm feeling anxious"):
                starter_message = "I've been feeling really anxious lately and I'm not sure how to deal with it."
                st.session_state.data_manager.save_chat_message("user", starter_message)
                st.rerun()
            
            if st.button("😢 I'm feeling sad"):
                starter_message = "I've been feeling sad and down recently. I could use some support."
                st.session_state.data_manager.save_chat_message("user", starter_message)
                st.rerun()
        
        with col2:
            if st.button("😤 I'm stressed about school"):
                starter_message = "School has been really stressful and overwhelming lately."
                st.session_state.data_manager.save_chat_message("user", starter_message)
                st.rerun()
            
            if st.button("🤷 I'm not sure what I'm feeling"):
                starter_message = "I'm going through something but I'm not sure exactly what I'm feeling or how to describe it."
                st.session_state.data_manager.save_chat_message("user", starter_message)
                st.rerun()
    
    # Chat tips
    with st.expander("💡 Tips for getting the most out of chat support"):
        st.markdown("""
        **Remember:**
        - 🔒 This is completely anonymous and private
        - 💭 Share as much or as little as you're comfortable with
        - 🔄 You can switch support styles anytime
        - 🆘 Crisis resources are always available if you need immediate help
        - 🧘 This is a judgment-free space for you to explore your feelings
        
        **Try sharing:**
        - What you're feeling right now
        - What's been on your mind lately
        - Situations that are stressing you out
        - Questions about managing emotions
        - Anything that feels safe to share
        """)
