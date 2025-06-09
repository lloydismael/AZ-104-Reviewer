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
            
            # Initialize variables
            current_question = {}
            in_question = False
            question_text = ""
            options = []
            answer = ""
            question_number = 0
            
            # Process each page
            full_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text += text + "\n"
                print(f"Processed page {page_num+1}/{len(pdf_reader.pages)}")
            
            print("Extracting questions from text...")
            # Find question patterns 
            question_blocks = re.split(r'(?:Question\s+\d+|QUESTION\s+\d+)', full_text)[1:]  # Split by question markers
            question_numbers = re.findall(r'(?:Question\s+(\d+)|QUESTION\s+(\d+))', full_text)  # Extract question numbers
            
            print(f"Found {len(question_blocks)} potential question blocks")
            print(f"Found {len(question_numbers)} question numbers")
            
            # Process each question block
            for i, block in enumerate(question_blocks):
                if i >= len(question_numbers):
                    break
                    
                # Get question number
                q_num = question_numbers[i][0] if question_numbers[i][0] else question_numbers[i][1]
                
                # Find the question text, options and correct answer
                # Pattern may need adjustment based on the actual PDF format
                question_text = block.strip()
                
                # Extract options (A, B, C, D)
                options_pattern = re.findall(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', question_text, re.DOTALL)
                options = {opt[0]: opt[1].strip() for opt in options_pattern}
                
                # Try to find the correct answer
                answer_match = re.search(r'Correct\s+[Aa]nswer:\s*([A-D])', question_text)
                if answer_match:
                    answer = answer_match.group(1)
                else:
                    # Alternative pattern
                    answer_match = re.search(r'[Aa]nswer:\s*([A-D])', question_text)
                    if answer_match:
                        answer = answer_match.group(1)
                
                # Clean question text
                # Remove the options and answer section
                clean_question = re.sub(r'([A-D])\.\s*(.*?)(?=(?:[A-D]\.|$))', '', question_text, flags=re.DOTALL)
                clean_question = re.sub(r'Correct\s+[Aa]nswer:\s*[A-D]', '', clean_question)
                clean_question = re.sub(r'[Aa]nswer:\s*[A-D]', '', clean_question)
                clean_question = clean_question.strip()
                
                # Add to questions list if we have options and an answer
                if options and answer:
                    questions.append({
                        'id': int(q_num),
                        'question': clean_question,
                        'options': options,
                        'correct_answer': answer
                    })
                    print(f"Successfully extracted question {q_num}")
                else:
                    print(f"Skipping question {q_num} - missing options or answer")
        
        print(f"Extracted {len(questions)} questions total")
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
            # Fallback to create sample questions for testing
            print("Creating sample questions for testing...")
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
            save_questions_to_json(sample_questions, output_path)
        else:
            # Extract questions from PDF
            questions = extract_questions_from_pdf(pdf_path)
            
            # Check if we got any questions
            if not questions:
                print("WARNING: No questions extracted from PDF. Creating sample questions for testing...")
                # Create sample questions for testing
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
