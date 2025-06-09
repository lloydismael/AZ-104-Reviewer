# AZ-104 Exam Review Application

This interactive web application helps you prepare for the Microsoft Azure Administrator (AZ-104) certification exam with practice questions extracted from the official exam material.

## Features

- **Interactive Quiz Interface**: Test your knowledge with multiple-choice questions from the AZ-104 exam.
- **Multiple Quiz Modes**: Take tests with all questions or choose a random selection of 10, 25, or 50 questions.
- **Progress Tracking**: Monitor your score and progress as you work through the questions.
- **Question Flagging**: Flag difficult questions for later review.
- **Timed Tests**: Practice under timed conditions to simulate the exam environment.
- **Detailed Review**: Review your answers with correct/incorrect indicators and explanations.
- **Result Export**: Save your quiz results for tracking your progress over time.

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- Flask
- PyPDF2 (for parsing question PDFs)
- Pandas (for data processing)

### Installation

1. Clone this repository or download the code.
2. Install the required packages:

```bash
pip install flask PyPDF2 pandas
```

3. Place your PDF file containing AZ-104 questions in the root directory. The PDF should be named `az-104_update may 31 2024.pdf` or update the path in `data/pdf_parser.py`.

4. Run the PDF parser to extract questions:

```bash
cd data
python pdf_parser.py
```

5. Start the application:

```bash
python run.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Usage

1. On the home page, select your quiz mode:
   - All Questions
   - 10 Random Questions
   - 25 Random Questions
   - 50 Random Questions

2. Answer each question by selecting the appropriate option.
3. Use the 'Flag for Review' button to mark questions you want to revisit.
4. Click 'Submit Answer' to check your response and see the correct answer.
5. At the end of the quiz, view your results and export them if desired.
6. Use the 'Review Answers' feature to see detailed feedback for each question.

## Project Structure

```
project_root/
│
├── run.py                       # Application entry point
│
├── app/                         # Flask application directory
│   ├── app.py                   # Main Flask application
│   ├── static/                  # Static files
│   │   ├── css/
│   │   │   └── styles.css       # Application styles
│   │   └── js/
│   │       └── quiz.js          # Quiz functionality
│   └── templates/               # HTML templates
│       ├── index.html           # Homepage
│       └── quiz.html            # Quiz interface
│
└── data/                        # Data processing
    ├── pdf_parser.py            # Script to extract questions from PDF
    └── az104_questions.json     # Extracted questions in JSON format
```

## Customization

To customize the application:

1. **Add new questions**: Modify `az104_questions.json` directly or update the PDF and rerun the parser.
2. **Change styling**: Edit `app/static/css/styles.css` to update the visual design.
3. **Modify quiz behavior**: Update `app/static/js/quiz.js` to change quiz functionality.

## License

This project is free to use for personal educational purposes.

## Acknowledgments

- Created for Azure Administrator (AZ-104) exam review
- Built with Python, Flask, and modern web technologies
