# Youth Mental Wellness Companion

## Overview

This is a confidential, AI-powered mental wellness chatbot application specifically designed to support youth mental health. The application provides completely anonymous access without requiring personal information, offering empathetic support through various AI personas (peer, mentor, therapist) and comprehensive self-help tools. Key features include mood tracking, guided journaling with CBT-based prompts, breathing exercises, cognitive behavioral therapy tools, psychoeducation resources, and built-in crisis detection with safety protocols.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with multi-tab interface
- **Layout**: Wide layout with expandable sidebar navigation for wellness tools
- **Components**: Modular component system with separate modules for chat interface, mood tracking, journaling, CBT exercises, breathing exercises, and psychoeducation
- **State Management**: Session-based state management using Streamlit's session state for maintaining user data and conversation history

### Backend Architecture
- **Core Logic**: Python-based application with utility modules for data management, crisis detection, and AI integration
- **AI Integration**: OpenAI GPT-5 integration with persona-based response generation (peer, mentor, therapist personas)
- **Crisis Detection**: Multi-layered crisis detection system combining keyword-based analysis and AI-powered sentiment analysis
- **Data Processing**: Local session-based data management with encryption for sensitive information

### Security & Privacy
- **Anonymous Access**: UUID-based anonymous user identification without requiring personal information
- **Data Encryption**: Cryptography.fernet-based encryption for sensitive user data
- **Session Management**: Ephemeral data storage using session state, no persistent user data storage
- **Crisis Safety**: Built-in crisis detection with automatic resource provision and professional help recommendations

### Data Management
- **Storage Pattern**: Session-based temporary storage with no persistent database
- **Data Types**: Chat history, mood entries, journal entries, CBT records, and crisis events
- **Encryption**: Real-time encryption/decryption of sensitive user inputs and responses
- **Privacy Controls**: Session-based data that is automatically cleared when session ends

## External Dependencies

### AI Services
- **OpenAI API**: GPT-5 model for empathetic response generation, sentiment analysis, and risk assessment
- **Crisis Detection**: AI-powered analysis combined with keyword-based detection for safety monitoring

### Python Libraries
- **Streamlit**: Web application framework and user interface
- **OpenAI**: Official OpenAI Python client for API integration
- **Cryptography**: Data encryption and security (Fernet symmetric encryption)
- **Plotly**: Interactive data visualization for mood tracking and progress charts
- **Pandas**: Data manipulation and analysis for tracking features

### Development Tools
- **UUID**: Anonymous user identification
- **Datetime**: Timestamp management for entries and sessions
- **JSON**: Data serialization for structured information storage
- **Regular Expressions**: Text pattern matching for crisis keyword detection

### Content Libraries
- **CBT Resources**: Evidence-based cognitive behavioral therapy prompts and exercises
- **Crisis Keywords**: Curated keyword database for mental health crisis detection
- **Journal Prompts**: Therapeutic journaling prompts organized by focus areas
- **Mental Health Education**: Psychoeducational content and coping strategies