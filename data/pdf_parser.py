import PyPDF2
import re
import json
import os
import traceback

def extract_questions_from_pdf(pdf_path):
    """
    Extract questions and answers from the AZ-104 PDF file
    """
    questions = []
    
    try:
        print(f"Opening PDF file: {pdf_path}")
        # Open the PDF file
        with open(pdf_path, 'rb') as file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"PDF has {len(pdf_reader.pages)} pages")
            
            # First pass: collect all text to analyze structure
            full_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
                if page_num % 50 == 0:  # Only print every 50 pages to reduce output clutter
                    print(f"Processed page {page_num+1}/{len(pdf_reader.pages)}")
            
            print(f"Total characters extracted: {len(full_text)}")
            print("Extracting questions from text...")
            
            # Find all question markers
            # Using various patterns to catch different formats in the PDF
            question_markers = re.finditer(r'(?:Question:?\s*(\d+)|QUESTION:?\s*(\d+))', full_text)
            
            # Get the positions of all question markers
            question_positions = []
            for match in question_markers:
                q_num = match.group(1) if match.group(1) else match.group(2)
                question_positions.append((int(q_num), match.start(), match.end()))
            
            question_positions.sort(key=lambda x: x[1])  # Sort by position in text
            
            print(f"Found {len(question_positions)} question markers")
            
            # Extract question blocks using the positions
            question_count = 0
            for i, (q_num, start_pos, end_pos) in enumerate(question_positions):
                # Get the text from this question to the next one
                if i < len(question_positions) - 1:
                    next_start = question_positions[i+1][1]
                    block_text = full_text[end_pos:next_start].strip()
                else:
                    block_text = full_text[end_pos:].strip()
                
                # Skip if block is too short
                if len(block_text) < 20:
                    continue
                
                # Extract answer section
                answer_match = re.search(r'[Aa]nswer:\s*([A-D])', block_text)
                if not answer_match:
                    print(f"No answer found for question {q_num}, skipping")
                    continue
                
                correct_answer = answer_match.group(1)
                
                # Find the options A, B, C, D
                options_sections = re.findall(r'([A-D])\.[\s\n]*(.*?)(?=[A-D]\.|\n[Aa]nswer:|$)', block_text, re.DOTALL)
                
                if not options_sections or len(options_sections) < 2:
                    print(f"Not enough options found for question {q_num}, skipping")
                    continue
                
                options = {}
                for opt_letter, opt_text in options_sections:
                    options[opt_letter] = opt_text.strip()
                
                # Find the question text (everything before the options)
                first_option_pos = block_text.find('A.')
                if first_option_pos == -1:
                    # Try another common format
                    first_option_pos = block_text.find('A\n')
                
                if first_option_pos > 0:
                    question_text = block_text[:first_option_pos].strip()
                else:
                    # If we can't find option A, use the first 1/3 of the text as the question
                    question_text = block_text[:len(block_text)//3].strip()
                
                # Clean up question text
                question_text = re.sub(r'Certy\s*IQ', '', question_text)
                question_text = question_text.strip()
                
                # Skip if question text is too short
                if len(question_text) < 10:
                    print(f"Question text too short for question {q_num}, skipping")
                    continue
                
                # Skip if we don't have enough options
                if len(options) < 2:
                    print(f"Not enough valid options for question {q_num}, skipping")
                    continue
                
                # Add to our questions list
                questions.append({
                    'id': q_num,
                    'question': question_text,
                    'options': options,
                    'correct_answer': correct_answer
                })
                
                question_count += 1
                if question_count % 50 == 0:  # Only print every 50 questions to reduce output clutter
                    print(f"Successfully extracted {question_count} questions so far")
        
        # Sort questions by ID
        questions.sort(key=lambda x: x['id'])
        
        # Renumber questions from 1 to N
        for i, q in enumerate(questions):
            q['id'] = i + 1
            
        print(f"Extracted and processed {len(questions)} questions total")
    except Exception as e:
        print(f"Error extracting questions: {str(e)}")
        traceback.print_exc()
    
    return questions

def save_questions_to_json(questions, output_path):
    """
    Save extracted questions to a JSON file
    """
    with open(output_path, 'w') as f:
        json.dump(questions, f, indent=4)
    
    print(f"Saved {len(questions)} questions to {output_path}")
    with open(output_path, 'w') as f:
        json.dump(questions, f, indent=4)
    
    print(f"Saved {len(questions)} questions to {output_path}")

if __name__ == "__main__":
    try:
        # Define paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        pdf_path = os.path.join(parent_dir, 'az-104_update may 31 2024.pdf')
        output_path = os.path.join(current_dir, 'az104_questions.json')
        
        print(f"Current directory: {current_dir}")
        print(f"Parent directory: {parent_dir}")
        print(f"PDF path: {pdf_path}")
        print(f"Output path: {output_path}")
        
        # Check if PDF file exists
        if not os.path.exists(pdf_path):
            print(f"ERROR: PDF file not found: {pdf_path}")
            print("Please make sure the PDF file is in the correct location.")
        else:
            # Extract questions from PDF
            questions = extract_questions_from_pdf(pdf_path)
            
            # Check if we got any questions
            if not questions or len(questions) < 10:
                print("WARNING: Too few questions extracted from PDF. Using backup extraction method...")
                
                # If we didn't get enough questions, try a different approach
                # This is a backup method to ensure we get questions
                backup_questions = []
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(pdf_path)
                    
                    # Process page by page looking for Question markers
                    current_question = {}
                    current_question_text = ""
                    current_options = {}
                    current_answer = ""
                    question_count = 0
                    
                    for page_index in range(len(reader.pages)):
                        page_text = reader.pages[page_index].extract_text()
                        
                        # Look for question number patterns
                        if re.search(r'Question:?\s+\d+', page_text):
                            # If we have a complete question from before, save it
                            if current_question and current_options and current_answer:
                                backup_questions.append({
                                    'id': len(backup_questions) + 1,
                                    'question': current_question_text.strip(),
                                    'options': current_options.copy(),
                                    'correct_answer': current_answer
                                })
                                question_count += 1
                                if question_count % 50 == 0:
                                    print(f"Backup method: extracted {question_count} questions")
                            
                            # Reset for next question
                            current_question_text = ""
                            current_options = {}
                            current_answer = ""
                        
                        # Extract question text, options, and answer
                        question_match = re.search(r'(Question:?\s+\d+.*?)([A-D]\.)', page_text, re.DOTALL)
                        if question_match:
                            current_question_text += question_match.group(1)
                        
                        # Extract options
                        options_matches = re.findall(r'([A-D])\.(.*?)(?=[A-D]\.|\n[Aa]nswer:|$)', page_text, re.DOTALL)
                        for opt, text in options_matches:
                            current_options[opt] = text.strip()
                        
                        # Extract answer
                        answer_match = re.search(r'[Aa]nswer:\s*([A-D])', page_text)
                        if answer_match:
                            current_answer = answer_match.group(1)
                    
                    # Add the last question if it's valid
                    if current_question_text and current_options and current_answer:
                        backup_questions.append({
                            'id': len(backup_questions) + 1,
                            'question': current_question_text.strip(),
                            'options': current_options.copy(),
                            'correct_answer': current_answer
                        })
                    
                    print(f"Backup method extracted {len(backup_questions)} questions")
                    
                    if len(backup_questions) > len(questions):
                        questions = backup_questions
                except Exception as e:
                    print(f"Error in backup extraction: {str(e)}")
            
            # If we still don't have enough questions, use sample questions as failsafe
            if not questions or len(questions) < 10:
                print("WARNING: Could not extract enough questions. Including sample questions.")
                # Add some sample questions 
                sample_questions = [
                    {
                        "id": 1,
                        "question": "You have an Azure subscription that contains a resource group named RG1. RG1 contains 100 virtual machines. Your company has three cost centers named Manufacturing, Sales, and Research. The Manufacturing cost center uses 50 virtual machines, the Sales cost center uses 30 virtual machines, and the Research cost center uses 20 virtual machines. You need to implement a solution that allows you to track the costs for each department. What should you do?",
                        "options": {
                            "A": "Add a tag to each virtual machine that has a name of Cost Center and a value of the appropriate cost center.",
                            "B": "Move the virtual machines for each cost center to a separate resource group.",
                            "C": "Create a resource group for each cost center and move the appropriate virtual machines to each new resource group.",                            "D": "Create a policy that prevents the creation of virtual machines that do not have a tag named Cost Center."
                        },
                        "correct_answer": "A"
                    },
                    {
                        "id": 2,
                        "question": "You have an Azure subscription that contains a virtual network named VNET1. VNET1 contains four subnets named Subnet1, Subnet2, Subnet3, and Subnet4. You plan to deploy Azure Application Gateway to Subnet1. Which configuration must be changed before you deploy Application Gateway?",
                        "options": {
                            "A": "The service endpoint of Subnet1",
                            "B": "The address space of VNET1",
                            "C": "The network security group (NSG) linked to Subnet1",
                            "D": "The address space of Subnet1"
                        },
                        "correct_answer": "D"
                    },
                    {
                        "id": 3,
                        "question": "You have Azure virtual machines that run Windows Server 2019 and are configured as web servers. You have an Azure Load Balancer that provides load balancing for the web servers. You need to ensure that the load balancer can distribute traffic based on URL path. What should you do?",
                        "options": {
                            "A": "Create a load balancing rule",
                            "B": "Add a health probe",
                            "C": "Upgrade to Azure Application Gateway",
                            "D": "Add an inbound NAT rule"
                        },
                        "correct_answer": "C"
                    },
                    {
                        "id": 4,
                        "question": "You have an Azure subscription that contains a storage account. You have an on-premises server named Server1 that runs Windows Server 2019. You plan to use Azure Backup to back up Server1 to the storage account. What else should you create before you can configure Azure Backup?",
                        "options": {
                            "A": "A Recovery Services vault",
                            "B": "A backup policy",
                            "C": "A Backup Server",
                            "D": "A site-to-site VPN"
                        },
                        "correct_answer": "A"
                    },
                    {
                        "id": 5,
                        "question": "You have an Azure subscription that contains a virtual network named VNet1. VNet1 contains four subnets named Gateway, Perimeter, NVA, and Production. The NVA subnet contains a network virtual appliance (NVA) named VM1 that runs Windows Server 2019. You create a route table named RT1. RT1 contains the routes shown in the following table.\n\nName | Address Prefix | Next Hop Type | Next Hop IP address\n-----|----------------|---------------|------------------\nRoute1 | 10.10.10.0/24 | VirtualAppliance | 10.0.1.4\nRoute2 | 10.20.20.0/24 | VirtualAppliance | 10.0.1.4\n\nYou need to ensure that all traffic from the Perimeter subnet to the Production subnet is inspected by VM1. What should you do?",
                        "options": {
                            "A": "Apply RT1 to the Perimeter subnet.",
                            "B": "Configure VM1 as a router.",
                            "C": "Apply RT1 to the Production subnet.",
                            "D": "Create a network interface, and then configure IP forwarding."
                        },
                        "correct_answer": "A"
                    }
                ]
                
                # Combine sample questions with any extracted questions
                if questions:
                    # Keep only sample questions that don't overlap with extracted question IDs
                    extracted_ids = [q['id'] for q in questions]
                    sample_questions = [q for q in sample_questions if q['id'] not in extracted_ids]
                    questions.extend(sample_questions)
                else:
                    questions = sample_questions
            
            # Save questions to JSON
            save_questions_to_json(questions, output_path)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        traceback.print_exc()
                    },
                    {
                        "id": 2,
                        "question": "You have an Azure subscription that contains a virtual network named VNET1. VNET1 contains four subnets named Subnet1, Subnet2, Subnet3, and Subnet4. You plan to deploy Azure Application Gateway to Subnet1. Which configuration must be changed before you deploy Application Gateway?",
                        "options": {
                            "A": "The service endpoint of Subnet1",
                            "B": "The address space of VNET1",
                            "C": "The network security group (NSG) linked to Subnet1",
                            "D": "The address space of Subnet1"
                        },
                        "correct_answer": "D"
                    },
                    {
                        "id": 3,
                        "question": "You have Azure virtual machines that run Windows Server 2019 and are configured as web servers. You have an Azure Load Balancer that provides load balancing for the web servers. You need to ensure that the load balancer can distribute traffic based on URL path. What should you do?",
                        "options": {
                            "A": "Create a load balancing rule",
                            "B": "Add a health probe",
                            "C": "Upgrade to Azure Application Gateway",
                            "D": "Add an inbound NAT rule"
                        },
                        "correct_answer": "C"
                    },
                    {
                        "id": 4,
                        "question": "You have an Azure subscription that contains a storage account. You have an on-premises server named Server1 that runs Windows Server 2019. You plan to use Azure Backup to back up Server1 to the storage account. What else should you create before you can configure Azure Backup?",
                        "options": {
                            "A": "A Recovery Services vault",
                            "B": "A backup policy",
                            "C": "A Backup Server",
                            "D": "A site-to-site VPN"
                        },
                        "correct_answer": "A"
                    },
                    {
                        "id": 5,
                        "question": "You have an Azure subscription that contains a virtual network named VNet1. VNet1 contains four subnets named Gateway, Perimeter, NVA, and Production. The NVA subnet contains a network virtual appliance (NVA) named VM1 that runs Windows Server 2019. You create a route table named RT1. RT1 contains the routes shown in the following table.\n\nName | Address Prefix | Next Hop Type | Next Hop IP address\n-----|----------------|---------------|------------------\nRoute1 | 10.10.10.0/24 | VirtualAppliance | 10.0.1.4\nRoute2 | 10.20.20.0/24 | VirtualAppliance | 10.0.1.4\n\nYou need to ensure that all traffic from the Perimeter subnet to the Production subnet is inspected by VM1. What should you do?",
                        "options": {
                            "A": "Apply RT1 to the Perimeter subnet.",
                            "B": "Configure VM1 as a router.",
                            "C": "Apply RT1 to the Production subnet.",
                            "D": "Create a network interface, and then configure IP forwarding."
                        },
                        "correct_answer": "A"
                    }
                ]
                questions = sample_questions
            
            # Save questions to JSON
            save_questions_to_json(questions, output_path)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        traceback.print_exc()
