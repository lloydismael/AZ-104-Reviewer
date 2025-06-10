# Extract all questions from the AZ-104 PDF and save to JSON
import PyPDF2
import re
import json
import os

def extract_questions(pdf_path):
    questions = []
    q_id = 1
    
    print(f'Opening PDF file: {pdf_path}')
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f'PDF has {len(pdf_reader.pages)} pages')
        
        all_text = ''
        for i, page in enumerate(pdf_reader.pages):
            if i % 50 == 0:
                print(f'Processing page {i+1}/{len(pdf_reader.pages)}')
            all_text += page.extract_text() + '\n'
        
        print(f'Total text length: {len(all_text)} characters')
        
        # Find all questions using regex
        # Look for patterns like "Question: 123" or "QUESTION 123"
        question_markers = list(re.finditer(r'(?:Question:?\s+(\d+)|QUESTION:?\s+(\d+))', all_text))
        print(f'Found {len(question_markers)} question markers')
        
        # Process each question block
        for i, marker in enumerate(question_markers):
            # Get the question number
            q_num = marker.group(1) if marker.group(1) else marker.group(2)
            start_pos = marker.end()
            
            # Determine end position (start of next question or end of text)
            if i < len(question_markers) - 1:
                end_pos = question_markers[i+1].start()
            else:
                end_pos = len(all_text)
            
            # Extract the question block
            block = all_text[start_pos:end_pos].strip()
            
            # Extract options (A, B, C, D)
            options = {}
            options_match = re.findall(r'([A-D])\.?\s*(.*?)(?=[A-D]\.|\n[Aa]nswer:|$)', block, re.DOTALL)
            for opt_letter, opt_text in options_match:
                options[opt_letter] = opt_text.strip()
            
            # Extract answer
            answer_match = re.search(r'[Aa]nswer:\s*([A-D])', block)
            if answer_match and len(options) >= 2:
                correct_answer = answer_match.group(1)
                
                # Get question text (everything before options)
                first_option_pos = -1
                for opt in 'ABCD':
                    pos = block.find(f'{opt}.')
                    if pos > 0 and (first_option_pos == -1 or pos < first_option_pos):
                        first_option_pos = pos
                
                if first_option_pos > 0:
                    question_text = block[:first_option_pos].strip()
                    
                    # Clean up question text (remove "Certy IQ" and other unwanted text)
                    question_text = re.sub(r'Certy\s*IQ', '', question_text)
                    question_text = question_text.strip()
                    
                    # Add to questions list if the question text is not too short
                    if len(question_text) > 10:
                        questions.append({
                            'id': q_id,
                            'question': question_text,
                            'options': options,
                            'correct_answer': correct_answer
                        })
                        q_id += 1
                        
                        if q_id % 50 == 0:
                            print(f'Extracted {q_id-1} questions')
    
    print(f'Extracted {len(questions)} questions total')
    return questions

def main():
    try:
        # Define paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        pdf_path = os.path.join(parent_dir, 'az-104_update may 31 2024.pdf')
        output_path = os.path.join(current_dir, 'az104_questions.json')
        
        print(f'Current directory: {current_dir}')
        print(f'PDF path: {pdf_path}')
        print(f'Output path: {output_path}')
        
        # Extract questions
        questions = extract_questions(pdf_path)
        
        # If we have questions, save them to JSON
        if questions and len(questions) >= 10:
            with open(output_path, 'w') as f:
                json.dump(questions, f, indent=4)
            print(f'Saved {len(questions)} questions to {output_path}')
        else:
            print('Not enough questions extracted, using sample questions')
            
            # Sample questions as fallback
            sample_questions = [
                {
                    "id": 1,
                    "question": "You have an Azure subscription that contains a resource group named RG1. RG1 contains 100 virtual machines. Your company has three cost centers named Manufacturing, Sales, and Research. The Manufacturing cost center uses 50 virtual machines, the Sales cost center uses 30 virtual machines, and the Research cost center uses 20 virtual machines. You need to implement a solution that allows you to track the costs for each department. What should you do?",
                    "options": {
                        "A": "Add a tag to each virtual machine that has a name of Cost Center and a value of the appropriate cost center.",
                        "B": "Move the virtual machines for each cost center to a separate resource group.",
                        "C": "Create a resource group for each cost center and move the appropriate virtual machines to each new resource group.",
                        "D": "Create a policy that prevents the creation of virtual machines that do not have a tag named Cost Center."
                    },
                    "correct_answer": "A"
                },
                # Add more sample questions here if needed (the 5 existing ones)
            ]
            
            with open(output_path, 'w') as f:
                json.dump(sample_questions, f, indent=4)
            print(f'Saved {len(sample_questions)} sample questions to {output_path}')
    except Exception as e:
        print(f'Error: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
