# Humaine Chatbot

An intelligent conversational AI system that learns and adapts to user preferences through reinforcement learning and advanced profiling techniques.

## 🚀 Features

- **Adaptive Learning**: Uses reinforcement learning to improve conversation quality over time
- **User Profiling**: Builds comprehensive user profiles through implicit and explicit feedback
- **Multi-Modal Interaction**: Supports both text-based chat and UI components
- **Real-time Adaptation**: Continuously learns from user interactions and feedback
- **Privacy-Aware**: Respects user privacy settings and data preferences

## 🏗️ Architecture

The system consists of several key components:

- **Core Engine**: Python-based backend with FastAPI
- **RL Agent**: Stable-Baselines3 PPO implementation for policy optimization
- **UI Components**: Stencil-based web components for seamless integration
- **Profiling System**: Advanced user modeling and preference learning
- **Evaluation Framework**: Comprehensive testing and performance analysis

## 📁 Project Structure

```
humaine-chatbot/
├── src/                    # Core Python source code
│   ├── api/               # FastAPI endpoints
│   ├── core/              # Core business logic
│   ├── models/            # Data models and schemas
│   └── utils/             # Utility functions
├── ui/                    # Stencil-based UI components
│   ├── src/
│   │   ├── components/    # Web components
│   │   ├── services/      # Frontend services
│   │   └── trackers/      # User interaction tracking
├── tests/                 # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── scripts/                # Utility scripts
│   ├── demos/             # Demo and example scripts
│   ├── tools/             # Utility tools
│   └── setup/             # Setup scripts
├── evaluation/            # Testing and evaluation framework
├── docs/                  # Documentation
│   ├── guides/            # Setup and integration guides
│   └── summaries/         # Historical summaries and reports
├── data/                  # User profiles and session data
└── main.py                # Application entry point
```

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- Node.js 16+
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd humaine-chatbot
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp config.env.example config.env
   # Edit config.env with your configuration
   ```

4. Run the backend:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the UI directory:
   ```bash
   cd ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Build components:
   ```bash
   npm run build
   ```

4. Start development server:
   ```bash
   npm start
   ```

## 🚀 Usage

### Basic Chat

```python
from src.core.dialogue_manager import DialogueManager

# Initialize the dialogue manager
manager = DialogueManager()

# Start a conversation
response = manager.process_user_input("Hello, how are you?")
print(response)
```

### UI Integration

```html
<!-- Include the chatbot component -->
<script type="module" src="path/to/humaine-chatbot.js"></script>

<!-- Use the component -->
<humaine-chatbot 
  api-base-url="http://localhost:8000"
  character-id="default"
  locale="en">
</humaine-chatbot>
```

## 🔧 Configuration

Key configuration options in `config.env`:

- `OPENAI_API_KEY`: Your OpenAI API key
- `MODEL_NAME`: GPT model to use (default: gpt-4)
- `MAX_TOKENS`: Maximum response length
- `TEMPERATURE`: Response creativity (0.0-1.0)

## 🧪 Testing

Run the test suite:

```bash
# Python tests
pytest tests/

# UI tests
cd ui
npm test
```

## 📊 Evaluation

The evaluation framework provides comprehensive testing:

```bash
cd evaluation
python experiment_runner.py
```

This will run automated tests and generate performance reports.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- Stable-Baselines3 team for RL implementations
- Stencil team for web component framework

## 📞 Support

For questions and support, please open an issue on GitHub or contact the development team.

---

**Note**: This is a research project. Please ensure compliance with relevant privacy and ethical guidelines when deploying in production environments. 