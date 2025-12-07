# AcademIQ - Intelligent Physics Tutor

AcademIQ is a premium, AI-powered educational web application designed to teach physics concepts to students of varying age in Kannada language. It leverages the **Google Agent Development Kit (ADK)** patterns and **Gemini Models** to provide personalized, age-adaptive learning experiences.

## 🚀 Features

*   **Age-Adaptive Learning**: Content is dynamically simplified or deepened based on the student's age.
*   **Multi-Agent Intelligence**: A system of specialized AI agents collaborates to deliver content.
*   **Visual Learning**: Dynamic, AI-generated diagrams help visualize abstract concepts.
*   **Kannada Language Support**: High-quality explanations and feedback in Kannada, with Text-to-Speech support.
*   **Interactive Practice**: 5-question adaptive quizzes with instant feedback.
*   **Premium UI**: Glassmorphism design with smooth animations for an engaging user experience.

## 🤖 Multi-Agent Architecture

AcademIQ is built on a robust multi-agent system where specialized agents collaborate to fulfill user requests using Google ADK patterns.

### 1. Coordinator Agent (`PhysicsTutor`)
*   **Role**: The Orchestrator.
*   **Description**: Manages the user session and delegates tasks to specialized sub-agents. It acts as the single point of entry for the application backend, initializing the system and routing requests.

### 2. Concept Agent
*   **Role**: The Teacher.
*   **Description**: Analyzes user questions to identify the core physics topic. It generates age-appropriate explanations, real-life examples, formulas, and translates key concepts into Kannada using Gemini models.

### 3. Image Agent
*   **Role**: The Artist.
*   **Description**: Generates precise, context-aware prompts for the image generation API. It ensures diagrams are educational and visually relevant to the specific physics topic.

### 4. Quiz Agent
*   **Role**: The Examiner.
*   **Description**: Creates a set of 5 multiple-choice questions tailored to the user's age. It provides specific feedback (praise/hints) in Kannada for each option.

## 🛠️ Technology Stack

*   **Backend**: Python, Flask
*   **AI Core**: Google Gen AI SDK (Gemini Models), Google ADK Patterns
*   **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript
*   **Image Generation**: Pollinations.ai API
*   **Audio**: Web Speech API (Text-to-Speech)

## 📦 Components

*   **`app.py`**: The Flask application server handling routes and session management.
*   **`agents/physics_tutor.py`**: Contains the class definitions for the Coordinator and all Sub-Agents (ConceptAgent, ImageAgent, QuizAgent).
*   **`templates/`**: Jinja2 HTML templates for the UI (Ask, Understanding, Explanation, Diagram, Practice, Chat).
*   **`static/style.css`**: reliable, premium styling definitions.

## 🏃‍♂️ How to Run

1.  **Install Dependencies**:
    ```bash
    pip install flask google-genai
    ```
2.  **Set API Key**:
    Ensure your `GOOGLE_API_KEY` is set in your environment or `app.py`.
3.  **Run the App**:
    ```bash
    python app.py
    ```
4.  **Access**:
    Open `http://localhost:5001` in your browser.
