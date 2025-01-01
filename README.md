# AI AGENT

## Overview
**AI AGENT** is a web application that leverages a fine-tuned GPT-2 model to provide intelligent and concise responses to user queries. The project demonstrates the integration of natural language processing with a user-friendly web interface. It is deployed using **AWS ECS** for scalable and reliable cloud-based execution.

---

## Features
- Fine-tuned GPT-2 model for contextual and relevant responses.
- Flask API with endpoints for prediction.
- Dockerized application for seamless deployment.
- Deployed on AWS ECS for high availability.

---

## Installation

### Prerequisites
- Python 3.9+
- Docker (optional, for containerized deployment)

### Steps to Set Up Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-agent.git
   cd ai-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the fine-tuned model is placed in the `fine_tuned_model/` directory.

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at `http://127.0.0.1:5000`.

---

## Running with Docker
1. Build the Docker image:
   ```bash
   docker build -t ai-agent .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 5000:5000 ai-agent
   ```

3. Access the application at `http://localhost:5000`.

---

## API Endpoints
### **`/predict`** (POST)
- **Description**: Generate a response for the provided query.
- **Request Body**:
  ```json
  {
    "question": "Your question here"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Generated response"
  }
  ```

### **Example**
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"question": ""}'
```

---

## Deployment on AWS ECS
- The application is containerized using Docker and deployed on AWS ECS for scalability.
- Ensure the **Dockerfile** and **fine_tuned_model/** are part of the build process.

---

## Fine-Tuning Process
The GPT-2 model was fine-tuned using a custom dataset containing question-answer pairs. Below are the key steps:
1. **Data Preparation**:
   - A cleaned dataset was converted from Excel to CSV.
   - Loaded using `datasets` library and tokenized using `GPT2Tokenizer`.

2. **Training**:
   - Used the Hugging Face `Trainer` API with the following parameters:
     - **Learning Rate**: 3e-5
     - **Batch Size**: 4 (train), 8 (eval)
     - **Epochs**: 6
   - Regular evaluations were conducted at the end of each epoch.

3. **Model Saving**:
   - The fine-tuned model and tokenizer were saved in `fine_tuned_model/`.

---

## Project Structure
```
ai-agent/
├── app.py                # Main Flask application
├── requirements.txt      # Dependencies
├── fine_tuned_model/     # Fine-tuned GPT-2 model
├── Dockerfile            # Docker configuration
├── templates/
│   └── index.html        # Frontend template
└── README.md             # Project documentation
```

---

## Technologies Used
- **Flask**: Web framework.
- **PyTorch**: For model training and inference.
- **Transformers**: Hugging Face library for NLP.
- **AWS ECS**: Cloud deployment.
- **Docker**: Containerization.

---

## Future Enhancements
- Integrate additional NLP capabilities, such as summarization or sentiment analysis.
- Expand API endpoints for more diverse functionalities.
- Deploy a frontend interface for a better user experience.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For inquiries or contributions, please reach out to:
- **Email**: sarathk1307@gmail.com
- **GitHub**: https://github.com/saisarath13/
```

