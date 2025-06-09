document.addEventListener('DOMContentLoaded', function() {
    // Quiz state
    const state = {
        questions: [],
        currentQuestionIndex: 0,
        score: 0,
        answers: [],
        selectedOption: null,
        quizStarted: false,
        quizEnded: false,
        startTime: null,
        endTime: null,
        progressData: {
            correct: 0,
            incorrect: 0,
            skipped: 0,
            remaining: 0
        }
    };
      // DOM Elements
    const elements = {
        questionContainer: document.getElementById('question-container'),
        resultsContainer: document.getElementById('results-container'),
        reviewContainer: document.getElementById('review-container'),
        currentQuestion: document.getElementById('current-question'),
        totalQuestions: document.getElementById('total-questions'),
        scoreElement: document.getElementById('score'),
        questionId: document.getElementById('question-id'),
        questionText: document.getElementById('question-text'),
        optionsContainer: document.getElementById('options-container'),
        feedback: document.getElementById('feedback'),
        feedbackText: document.getElementById('feedback-text'),
        explanation: document.getElementById('explanation'),
        submitBtn: document.getElementById('submit-btn'),
        nextBtn: document.getElementById('next-btn'),
        finalScore: document.getElementById('final-score'),
        finalTotal: document.getElementById('final-total'),
        reviewBtn: document.getElementById('review-btn'),
        reviewList: document.getElementById('review-list'),
        timeTaken: document.getElementById('time-taken'),
        timer: document.getElementById('timer'),
        progressBar: document.getElementById('progress-bar')
    };
    
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode') || 'all';
    const limit = urlParams.get('limit') ? parseInt(urlParams.get('limit')) : null;
    
    // Timer variables
    let timerInterval;
    
    // Initialize the quiz
    function initQuiz() {
        // Fetch questions based on mode
        let url = '/api/questions';
        if (mode === 'random' && limit) {
            url += `?limit=${limit}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                state.questions = data;
                updateQuizStatus();
                loadQuestion();
                startTimer();
                state.quizStarted = true;
                state.startTime = new Date();
            })
            .catch(error => {
                console.error('Error loading questions:', error);
                alert('Failed to load questions. Please try again.');
            });
    }
      // Update quiz status (question count, score)
    function updateQuizStatus() {
        elements.currentQuestion.textContent = state.currentQuestionIndex + 1;
        elements.totalQuestions.textContent = state.questions.length;
        elements.scoreElement.textContent = state.score;
        
        // Update progress data
        state.progressData.remaining = state.questions.length - state.answers.length;
        state.progressData.correct = state.score;
        state.progressData.incorrect = state.answers.length - state.score;
        
        // Update progress bar if we've added one
        if (elements.progressBar) {
            const progressPercent = (state.currentQuestionIndex / state.questions.length) * 100;
            elements.progressBar.style.width = `${progressPercent}%`;
        }
    }
      // Load the current question
    function loadQuestion() {
        const question = state.questions[state.currentQuestionIndex];
        
        // Reset state for this question
        state.selectedOption = null;
        hideElement(elements.feedback);
        hideElement(elements.nextBtn);
        showElement(elements.submitBtn);
        
        // Update question display
        elements.questionId.textContent = question.id;
        elements.questionText.textContent = question.question;
        
        // Clear previous options
        elements.optionsContainer.innerHTML = '';
        
        // Add new options
        for (const [letter, text] of Object.entries(question.options)) {
            const optionElement = document.createElement('div');
            optionElement.classList.add('option');
            optionElement.dataset.option = letter;
            
            optionElement.innerHTML = `
                <div class="option-letter">${letter}</div>
                <div class="option-text">${text}</div>
            `;
            
            optionElement.addEventListener('click', () => selectOption(optionElement, letter));
            
            elements.optionsContainer.appendChild(optionElement);
        }
        
        // Add bookmark/flag button
        if (!elements.flagBtn) {
            const flagBtn = document.createElement('button');
            flagBtn.id = 'flag-btn';
            flagBtn.classList.add('btn', 'tertiary', 'flag-btn');
            flagBtn.innerHTML = '🚩 Flag for review';
            flagBtn.addEventListener('click', toggleFlagQuestion);
            
            // Add to actions area
            document.querySelector('.actions').prepend(flagBtn);
            elements.flagBtn = flagBtn;
        }
        
        // Update flag button state
        const questionIsFlaged = question.flagged || false;
        elements.flagBtn.classList.toggle('active', questionIsFlaged);
        elements.flagBtn.innerHTML = questionIsFlaged ? '🚩 Unflag question' : '🚩 Flag for review';
    }
    
    // Toggle flag on current question
    function toggleFlagQuestion() {
        const question = state.questions[state.currentQuestionIndex];
        question.flagged = !question.flagged;
        
        // Update button appearance
        const isFlagged = question.flagged;
        elements.flagBtn.classList.toggle('active', isFlagged);
        elements.flagBtn.innerHTML = isFlagged ? '🚩 Unflag question' : '🚩 Flag for review';
    }
    
    // Handle option selection
    function selectOption(optionElement, letter) {
        // Clear previous selection
        const options = elements.optionsContainer.querySelectorAll('.option');
        options.forEach(opt => opt.classList.remove('selected'));
        
        // Mark this option as selected
        optionElement.classList.add('selected');
        state.selectedOption = letter;
    }
    
    // Handle answer submission
    function submitAnswer() {
        if (!state.selectedOption) {
            alert('Please select an option');
            return;
        }
        
        const currentQuestion = state.questions[state.currentQuestionIndex];
        const isCorrect = state.selectedOption === currentQuestion.correct_answer;
        
        // Save the answer
        state.answers.push({
            questionId: currentQuestion.id,
            question: currentQuestion.question,
            options: currentQuestion.options,
            selectedOption: state.selectedOption,
            correctOption: currentQuestion.correct_answer,
            isCorrect: isCorrect
        });
        
        // Update score if correct
        if (isCorrect) {
            state.score++;
            elements.scoreElement.textContent = state.score;
        }
        
        // Show feedback
        showFeedback(isCorrect);
        
        // Highlight the correct/incorrect answers
        highlightAnswers();
        
        // Switch buttons
        hideElement(elements.submitBtn);
        showElement(elements.nextBtn);
    }
    
    // Show feedback based on answer correctness
    function showFeedback(isCorrect) {
        elements.feedback.classList.remove('correct', 'incorrect');
        elements.feedback.classList.add(isCorrect ? 'correct' : 'incorrect');
        
        elements.feedbackText.textContent = isCorrect 
            ? 'Correct! Well done.' 
            : `Incorrect. The correct answer is ${state.questions[state.currentQuestionIndex].correct_answer}.`;
        
        showElement(elements.feedback);
    }
    
    // Highlight the correct and incorrect answers
    function highlightAnswers() {
        const options = elements.optionsContainer.querySelectorAll('.option');
        const currentQuestion = state.questions[state.currentQuestionIndex];
        
        options.forEach(option => {
            const letter = option.dataset.option;
            
            if (letter === currentQuestion.correct_answer) {
                option.classList.add('correct');
            } else if (letter === state.selectedOption && state.selectedOption !== currentQuestion.correct_answer) {
                option.classList.add('incorrect');
            }
        });
    }
    
    // Move to the next question
    function nextQuestion() {
        state.currentQuestionIndex++;
        
        if (state.currentQuestionIndex >= state.questions.length) {
            endQuiz();
        } else {
            updateQuizStatus();
            loadQuestion();
        }
    }
    
    // End the quiz and show results
    function endQuiz() {
        state.quizEnded = true;
        state.endTime = new Date();
        
        // Stop the timer
        clearInterval(timerInterval);
        
        // Calculate time taken
        const timeDiff = state.endTime - state.startTime; // in milliseconds
        const minutes = Math.floor(timeDiff / 60000);
        const seconds = ((timeDiff % 60000) / 1000).toFixed(0);
        const formattedTime = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update results
        elements.finalScore.textContent = state.score;
        elements.finalTotal.textContent = state.questions.length;
        elements.timeTaken.textContent = formattedTime;
        
        // Show results container
        hideElement(elements.questionContainer);
        showElement(elements.resultsContainer);
    }
      // Show the review screen
    function showReview() {
        hideElement(elements.resultsContainer);
        showElement(elements.reviewContainer);
        
        // Clear previous review
        elements.reviewList.innerHTML = '';
        
        // Count flagged questions
        const flaggedQuestions = state.questions.filter(q => q.flagged).length;
        
        // Add a flagged questions section if there are any
        if (flaggedQuestions > 0) {
            const flaggedSection = document.createElement('div');
            flaggedSection.classList.add('review-section');
            flaggedSection.innerHTML = `
                <h3>Flagged Questions (${flaggedQuestions})</h3>
            `;
            elements.reviewList.appendChild(flaggedSection);
            
            // Add flagged questions
            state.questions.forEach((question, index) => {
                if (!question.flagged) return;
                
                // Find the corresponding answer if it exists
                const answer = state.answers.find(a => a.questionId === question.id);
                const isAnswered = !!answer;
                
                const reviewItem = document.createElement('div');
                reviewItem.classList.add('review-item', 'flagged');
                if (isAnswered) {
                    reviewItem.classList.add(answer.isCorrect ? 'correct' : 'incorrect');
                }
                
                reviewItem.innerHTML = `
                    <div class="question-number">Question ${index + 1} (ID: ${question.id}) ${isAnswered ? '' : '- Not answered'}</div>
                    <div class="question-text">${question.question}</div>
                    <div class="options-review">
                        ${Object.entries(question.options).map(([letter, text]) => `
                            <div class="option ${isAnswered && letter === question.correct_answer ? 'correct' : ''} ${isAnswered && letter === answer.selectedOption && letter !== question.correct_answer ? 'incorrect' : ''}">
                                <div class="option-letter">${letter}</div>
                                <div class="option-text">${text}</div>
                            </div>
                        `).join('')}
                    </div>
                    ${isAnswered ? `
                        <div class="review-answer">
                            Your answer: ${answer.selectedOption} - ${answer.isCorrect ? 'Correct' : 'Incorrect'}
                            ${!answer.isCorrect ? `<p>Correct answer: ${answer.correctOption}</p>` : ''}
                        </div>
                    ` : `
                        <div class="review-answer">
                            <p>Correct answer: ${question.correct_answer}</p>
                        </div>
                    `}
                `;
                
                elements.reviewList.appendChild(reviewItem);
            });
        }
        
        // Add a section for all questions
        const allQuestionsSection = document.createElement('div');
        allQuestionsSection.classList.add('review-section');
        allQuestionsSection.innerHTML = `
            <h3>All Answered Questions (${state.answers.length})</h3>
        `;
        elements.reviewList.appendChild(allQuestionsSection);
        
        // Add each answered question to the review list
        state.answers.forEach((answer, index) => {
            const reviewItem = document.createElement('div');
            reviewItem.classList.add('review-item');
            reviewItem.classList.add(answer.isCorrect ? 'correct' : 'incorrect');
            
            reviewItem.innerHTML = `
                <div class="question-number">Question ${index + 1} (ID: ${answer.questionId})</div>
                <div class="question-text">${answer.question}</div>
                <div class="options-review">
                    ${Object.entries(answer.options).map(([letter, text]) => `
                        <div class="option ${letter === answer.correctOption ? 'correct' : ''} ${letter === answer.selectedOption && letter !== answer.correctOption ? 'incorrect' : ''}">
                            <div class="option-letter">${letter}</div>
                            <div class="option-text">${text}</div>
                        </div>
                    `).join('')}
                </div>
                <div class="review-answer">
                    Your answer: ${answer.selectedOption} - ${answer.isCorrect ? 'Correct' : 'Incorrect'}
                    ${!answer.isCorrect ? `<p>Correct answer: ${answer.correctOption}</p>` : ''}
                </div>
            `;
            
            elements.reviewList.appendChild(reviewItem);
        });
    }
    
    // Start timer function
    function startTimer() {
        let seconds = 0;
        timerInterval = setInterval(() => {
            seconds++;
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            elements.timer.textContent = `Time: ${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    // Utility functions for showing/hiding elements
    function showElement(element) {
        element.classList.remove('hidden');
    }
    
    function hideElement(element) {
        element.classList.add('hidden');
    }
      // Event listeners
    elements.submitBtn.addEventListener('click', submitAnswer);
    elements.nextBtn.addEventListener('click', nextQuestion);
    elements.reviewBtn.addEventListener('click', showReview);
    
    // Add export button functionality if it exists
    const exportBtn = document.getElementById('export-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportResults);
    }
    
    // Function to export quiz results
    function exportResults() {
        const totalQuestions = state.questions.length;
        const answeredQuestions = state.answers.length;
        const correctAnswers = state.score;
        const timeTaken = elements.timeTaken.textContent;
        
        // Create results text
        const resultsText = `
AZ-104 Exam Review Results
==========================
Date: ${new Date().toLocaleDateString()}
Time: ${new Date().toLocaleTimeString()}

Summary:
--------
Total Questions: ${totalQuestions}
Answered Questions: ${answeredQuestions}
Correct Answers: ${correctAnswers}
Score: ${Math.round((correctAnswers / totalQuestions) * 100)}%
Time Taken: ${timeTaken}

Question Details:
----------------
${state.answers.map((answer, index) => `
Question ${index + 1} (ID: ${answer.questionId}):
${answer.question.substring(0, 100)}...
Your Answer: ${answer.selectedOption} (${answer.isCorrect ? 'Correct' : 'Incorrect'})
${!answer.isCorrect ? `Correct Answer: ${answer.correctOption}` : ''}
`).join('\n')}
`;

        // Create a blob from the text
        const blob = new Blob([resultsText], { type: 'text/plain' });
        
        // Create a download link and trigger it
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `az104-quiz-results-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    // Initialize the quiz when the page loads
    initQuiz();
});
