# Simple script to extract at least 100 questions from the AZ-104 PDF
import PyPDF2
import re
import json
import os
import time

def extract_batch_of_questions(pdf_path, num_questions=200):
    start_time = time.time()
    questions = []
    
    try:
        print(f"Opening PDF file: {pdf_path}")
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            print(f"PDF has {num_pages} pages")
            
            # Extract 10 pages at a time to find questions more efficiently
            page_batch_size = 10
            current_page = 0
            extracted_count = 0
            
            while current_page < num_pages and extracted_count < num_questions:
                batch_end = min(current_page + page_batch_size, num_pages)
                batch_text = ""
                
                # Extract text from this batch of pages
                for i in range(current_page, batch_end):
                    batch_text += pdf_reader.pages[i].extract_text() + "\n"
                
                # Find questions in this batch
                # Look for patterns like "Question: X" or "QUESTION X"
                question_blocks = re.split(r'(?:Question\s+\d+|QUESTION\s+\d+)', batch_text)[1:]  # Split by question markers
                question_numbers = re.findall(r'(?:Question\s+(\d+)|QUESTION\s+(\d+))', batch_text)  # Extract question numbers
                
                # Process each question block in this batch
                for i, block in enumerate(question_blocks):
                    if i >= len(question_numbers) or extracted_count >= num_questions:
                        break
                    
                    # Get question number
                    q_num = question_numbers[i][0] if question_numbers[i][0] else question_numbers[i][1]
                    
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
                            
                            # Clean up question text
                            question_text = re.sub(r'Certy\s*IQ', '', question_text)
                            question_text = question_text.strip()
                            
                            # Add to questions list if the question text is not too short
                            if len(question_text) > 10:
                                questions.append({
                                    'id': extracted_count + 1,
                                    'question': question_text,
                                    'options': options,
                                    'correct_answer': correct_answer
                                })
                                extracted_count += 1
                                
                                if extracted_count % 10 == 0:
                                    print(f"Found {extracted_count} questions so far")
                
                # Move to next batch of pages
                current_page = batch_end
                print(f"Processed pages {current_page}/{num_pages}")
        
        elapsed_time = time.time() - start_time
        print(f"Extraction completed in {elapsed_time:.2f} seconds")
        print(f"Extracted {len(questions)} questions total")
    except Exception as e:
        print(f"Error extracting questions: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return questions

def main():
    try:
        # Define paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir) 
        pdf_path = os.path.join(parent_dir, 'az-104_update may 31 2024.pdf')
        output_path = os.path.join(script_dir, 'az104_questions.json')
        
        print(f"Script directory: {script_dir}")
        print(f"PDF path: {pdf_path}")
        print(f"Output path: {output_path}")
        
        # Extract a batch of questions (adjust number as needed)
        questions = extract_batch_of_questions(pdf_path, num_questions=200)
        
        if questions and len(questions) >= 10:
            # Save the extracted questions to JSON
            with open(output_path, 'w') as f:
                json.dump(questions, f, indent=4)
            print(f"Successfully saved {len(questions)} questions to {output_path}")
        else:
            print("Failed to extract enough questions")
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
