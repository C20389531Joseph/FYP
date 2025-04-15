# FYP
Final Year Project


# 📝 Essay Grader App

A web-based application for grading student essays using advanced NLP models (LSTM & BERT), with automated feedback generation powered by GPT-2.

---

## 🚀 Features

- ✅ Upload essays in `.docx` or `.txt` format
- 🤖 Dual-model grading:
  - **LSTM**: Evaluates using sequential text modeling
  - **BERT**: Context-aware deep learning classification
- 🧠 AI-generated feedback using GPT-2
- 📂 Multi-year model support (2023, 2024, SampleQuestions)
- 🌐 Clean Flask-based web interface

---

## 🛠️ Setup Instructions

### 🔧 Requirements

- Python 3.8+
- TensorFlow
- PyTorch
- HuggingFace Transformers
- Flask
- python-docx
- PyMuPDF (for optional PDF support)
- OpenAI API (optional, for GPT-2 feedback)

### 📦 Installation

```bash
# Clone the repo
git clone https://github.com/C20389531Joseph/FYP
cd essay-grader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Running the App

```bash
# From the root directory
python run.py
```

Visit: [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📁 Project Structure

```
essay_grader/
├── app/
│   ├── __init__.py            # Flask app factory
│   ├── controllers.py         # Web routes and logic
│   ├── models.py              # LSTM loading and grading
│   ├── modules_BERT.py        # BERT loading and grading
├── uploads/                   # Uploaded essay storage
├── static/exams/              # Stored exam questions by year
├── run.py                     # Flask entry point
```

---

## 🧠 How It Works

1. User uploads an essay and selects the model year.
2. Text is extracted from the uploaded file.
3. Essay is graded by both:
   - **LSTM model** (via `models.py`)
   - **BERT model** (via `modules_BERT.py`)
4. Optionally, GPT-2 generates personalized feedback.
5. Scores and feedback are shown on the web interface.

---

## ⚙️ Configurable Parts

- `MODEL_PATHS` and `TOKENIZER_PATHS` in `models.py` / `modules_BERT.py` can be updated for your custom models.
- Grading scale is defined via `MAX_SCORES_BY_YEAR`.
- GPT-2 generation is done using HuggingFace’s `pipeline`.

---

## 📚 Dependencies

- `Flask`
- `TensorFlow`
- `torch`
- `transformers`
- `python-docx`
- `PyMuPDF` (optional PDF support)
- `openai` (if integrating GPT)

---

## 📜 License

This project is for academic and research use only. Please cite or credit appropriately if reused.
