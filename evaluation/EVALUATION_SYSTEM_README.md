# HumAIne Chatbot Evaluation System

This evaluation system provides comprehensive testing of the HumAIne chatbot's personalization capabilities using virtual personas and conversation simulation.

## 🎯 Overview

The evaluation system consists of three main components:

1. **Virtual Personas Generator** - Creates 50 diverse virtual personas with detailed backstories
2. **Conversation Simulator** - Simulates conversations between personas and the chatbot
3. **Comprehensive Evaluator** - Orchestrates the entire evaluation process and generates reports

## 🚀 Quick Start

### Prerequisites

1. **HumAIne Backend Running**: Ensure your chatbot backend is running on `http://localhost:8000`
2. **OpenAI API Key**: Set `OPENAI_API_KEY` in your `.env` file
3. **Python Dependencies**: Install required packages

### Installation

```bash
# Navigate to evaluation directory
cd evaluation

# Install dependencies
pip install -r evaluation_requirements.txt
```

### Run Evaluation

```bash
# Run the complete evaluation
python run_evaluation.py
```

## 📋 What the System Does

### 1. Virtual Persona Generation
- **Creates 50 diverse personas** with realistic demographics
- **Varied characteristics**: Age, education, occupation, expertise, communication style
- **Detailed backstories**: Each persona has a complete background and personality
- **Diversity scoring**: Ensures representation across different user types

### 2. Conversation Simulation
- **LLM-powered personas**: Uses GPT-4 to generate natural questions and responses
- **Topic variety**: 10 different conversation topics (career, technology, finance, etc.)
- **Session management**: 8-15 questions per session with realistic timing
- **API integration**: Direct calls to your HumAIne chatbot backend

### 3. Metrics Collection
- **Satisfaction scoring**: Multi-factor analysis (relevance, personalization, expertise alignment)
- **Performance metrics**: Response time, message efficiency, engagement depth
- **Quality assessment**: Relevance, personalization, style matching
- **Conversation flow**: Natural progression and interaction patterns

### 4. Comprehensive Analysis
- **Statistical analysis**: Mean, median, standard deviation of all metrics
- **Demographic breakdown**: Performance across different persona types
- **Topic analysis**: Satisfaction and performance by conversation topic
- **Diversity assessment**: Coverage and representation analysis

## 📊 Generated Outputs

### Data Files
- `virtual_personas_[timestamp].json` - All generated personas
- `conversation_summary_[timestamp].json` - Summary of all conversations
- `evaluation_analysis_[timestamp].json` - Detailed analysis results
- `comprehensive_evaluation_results_[timestamp].json` - Complete evaluation data

### Reports
- `executive_summary_[timestamp].md` - High-level findings and recommendations
- `technical_analysis_[timestamp].md` - Technical methodology and architecture
- `persona_analysis_[timestamp].md` - Detailed persona breakdown and diversity analysis
- `performance_metrics_[timestamp].md` - Performance analysis and insights

### Visualizations
- `satisfaction_distribution_[timestamp].png` - User satisfaction histogram
- `persona_demographics_[timestamp].png` - Demographics pie charts and distributions
- `performance_dashboard_[timestamp].png` - Performance metrics dashboard

## 🔧 Configuration

### Evaluation Settings
The system can be configured in `comprehensive_evaluator.py`:

```python
self.config = {
    'total_personas': 50,           # Total personas to generate
    'test_personas': 10,            # Personas to test with (to save API calls)
    'min_questions_per_session': 8, # Minimum questions per session
    'max_questions_per_session': 15,# Maximum questions per session
    'session_delay': 1.0,           # Delay between sessions (seconds)
    'evaluation_topics': [...]       # List of conversation topics
}
```

### API Configuration
- **Backend URL**: Defaults to `http://localhost:8000`
- **OpenAI Model**: Uses GPT-4 for persona generation and simulation
- **Rate Limiting**: Built-in delays to avoid API rate limits

## 📈 Understanding Results

### Satisfaction Scores
- **0.8-1.0**: High satisfaction (excellent personalization)
- **0.6-0.8**: Medium satisfaction (good personalization)
- **0.0-0.6**: Low satisfaction (needs improvement)

### Key Metrics
- **Response Relevance**: How well answers match questions
- **Personalization Level**: How much responses are tailored to personas
- **Expertise Alignment**: How well responses match persona's domain knowledge
- **Style Match**: How well communication style matches persona preferences

### Diversity Score
- **0.8-1.0**: Excellent diversity coverage
- **0.6-0.8**: Good diversity coverage
- **0.0-0.6**: Limited diversity coverage

## 🧪 Testing Scenarios

### Default Topics
1. Career Development and Growth
2. Technology Trends and Innovation
3. Personal Finance and Investment
4. Health and Wellness
5. Education and Learning
6. Travel and Culture
7. Professional Networking
8. Work-Life Balance
9. Creative Projects and Hobbies
10. Environmental Sustainability

### Persona Types
- **Age Groups**: 18-25, 26-35, 36-45, 46-55, 56-65, 65+
- **Education Levels**: High School to PhD
- **Occupations**: Technology, Healthcare, Education, Finance, Marketing, etc.
- **Expertise Domains**: AI, Data Science, Healthcare, Finance, Engineering, etc.

## 🔍 Troubleshooting

### Common Issues

1. **Backend Not Running**
   ```
   ❌ HumAIne backend is not running
   Please start it first with: docker-compose up -d
   ```

2. **Missing Dependencies**
   ```
   ❌ Missing required packages
   Install them with: pip install -r evaluation_requirements.txt
   ```

3. **API Key Issues**
   ```
   ❌ OPENAI_API_KEY not found in environment
   Please set it in your .env file
   ```

4. **Rate Limiting**
   - The system includes built-in delays
   - If you hit rate limits, increase `session_delay` in config

### Performance Tips

- **Reduce test personas**: Set `test_personas` to 5-10 for faster testing
- **Limit questions**: Reduce `max_questions_per_session` for quicker sessions
- **Batch processing**: Run during off-peak hours to avoid API congestion

## 📚 Advanced Usage

### Custom Persona Generation
```python
from virtual_personas_generator import VirtualPersonaGenerator

generator = VirtualPersonaGenerator()
custom_personas = generator.generate_all_personas(25)  # Generate 25 personas
```

### Custom Conversation Simulation
```python
from conversation_simulator import ConversationSimulator

simulator = ConversationSimulator("http://your-api-url:8000")
session = await simulator.run_conversation_session(persona, "Custom Topic")
```

### Standalone Analysis
```python
from comprehensive_evaluator import ComprehensiveEvaluator

evaluator = ComprehensiveEvaluator()
analysis = evaluator.analyze_evaluation_results(personas, conversations)
```

## 🎯 Use Cases

### Research and Development
- **A/B Testing**: Compare different personalization algorithms
- **Performance Benchmarking**: Measure chatbot effectiveness
- **User Experience Research**: Understand user satisfaction patterns

### Quality Assurance
- **Regression Testing**: Ensure updates don't break personalization
- **Scalability Testing**: Test with large numbers of virtual users
- **Edge Case Discovery**: Find unusual persona combinations

### Business Intelligence
- **User Segmentation**: Understand different user types
- **Content Optimization**: Identify which topics need improvement
- **ROI Analysis**: Measure personalization impact

## 📞 Support

For issues or questions about the evaluation system:

1. Check the troubleshooting section above
2. Review the generated logs and error messages
3. Verify your backend is running and accessible
4. Ensure all environment variables are set correctly

## 🔄 Updates and Maintenance

The evaluation system is designed to be:
- **Modular**: Easy to modify individual components
- **Extensible**: Simple to add new metrics or analysis types
- **Maintainable**: Clear separation of concerns and documentation
- **Versioned**: All outputs include timestamps and version information

---

*This evaluation system provides comprehensive testing of your HumAIne chatbot's personalization capabilities, helping you understand and improve user satisfaction across diverse user types and conversation topics.*

