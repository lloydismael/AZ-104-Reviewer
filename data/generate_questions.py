# Simple script to generate a large set of sample questions
import json
import os

def generate_sample_questions(num_questions=572):
    """Generate a large set of sample AZ-104 questions"""
    questions = []
    
    # Base questions that will be duplicated and modified
    base_questions = [
        {
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
            "question": "You have an Azure subscription that contains a virtual network named VNet1. VNet1 contains four subnets named Gateway, Perimeter, NVA, and Production. The NVA subnet contains a network virtual appliance (NVA) named VM1 that runs Windows Server 2019. You create a route table named RT1. RT1 contains the routes shown in the following table.\n\nName | Address Prefix | Next Hop Type | Next Hop IP address\n-----|----------------|---------------|------------------\nRoute1 | 10.10.10.0/24 | VirtualAppliance | 10.0.1.4\nRoute2 | 10.20.20.0/24 | VirtualAppliance | 10.0.1.4\n\nYou need to ensure that all traffic from the Perimeter subnet to the Production subnet is inspected by VM1. What should you do?",
            "options": {
                "A": "Apply RT1 to the Perimeter subnet.",
                "B": "Configure VM1 as a router.",
                "C": "Apply RT1 to the Production subnet.",
                "D": "Create a network interface, and then configure IP forwarding."
            },
            "correct_answer": "A"
        },
        {
            "question": "You have an Azure subscription that contains an Azure Storage account named storage1 and an Azure Key Vault named vault1. You plan to create an Azure function app named app1 that will use a system-assigned managed identity to access storage1. You need to ensure that app1 can access the connection string for storage1. The solution must minimize the number of secrets that are stored in the code for app1. What should you do?",
            "options": {
                "A": "Store the connection string in vault1, and then create an access policy in vault1.",
                "B": "Store the connection string in an app setting of app1, and then enable the system-assigned managed identity for app1.",
                "C": "Store the connection string in vault1, enable the system-assigned managed identity for app1, and then create an access policy in vault1.",
                "D": "Store the connection string in an app setting of app1."
            },
            "correct_answer": "C"
        },
        {
            "question": "You have a Microsoft 365 tenant and an Azure subscription. You plan to grant access to developers to manage all the resources in the Azure subscription. The developers have Microsoft accounts that are already associated to the Azure subscription as guests. You need to ensure that the developers can access the Azure subscription by using the Microsoft Entra ID credentials of the Microsoft 365 tenant. What should you do?",
            "options": {
                "A": "From the Microsoft 365 admin center, modify the user settings of Microsoft Entra ID.",
                "B": "From the Azure portal, register an identity provider in Microsoft Entra ID.",
                "C": "From the Microsoft 365 admin center, purchase Microsoft Entra ID P1 licenses for the developers.",
                "D": "From the Azure portal, modify the directory role of the developer accounts."
            },
            "correct_answer": "B"
        },
        {
            "question": "You have an Azure subscription that contains a resource group named rg1017. In rg1017, you create an internal load balancer named lb17 and a virtual machine named vm17 that has the required supporting resources. You need to ensure that all traffic from the 10.0.0.0/16 subnet to vm17 is routed through lb17. What should you do?",
            "options": {
                "A": "Create a route table, and then apply the route table to the subnet that contains vm17.",
                "B": "Configure a load balancing rule.",
                "C": "Create an inbound NAT rule.",
                "D": "Configure a health probe."
            },
            "correct_answer": "B"
        },
        {
            "question": "You have an Azure subscription that contains a virtual network named VNet1. VNet1 contains a subnet named Subnet1. You create a network security group (NSG) named NSG1. You need to apply NSG1 to Subnet1. What should you do?",
            "options": {
                "A": "From the Azure portal, select VNet1, and then select Service endpoints.",
                "B": "From Azure PowerShell, run the Set-AzVirtualNetworkSubnetConfig and the Set-AzVirtualNetwork cmdlets.",
                "C": "From Azure PowerShell, run the Set-AzNetworkSecurityGroup cmdlet.",
                "D": "From the Azure portal, select NSG1, and then select Inbound security rules."
            },
            "correct_answer": "B"
        },
        {
            "question": "You need to monitor the health status of resources in an Azure subscription. The solution must meet the following requirements: Include an interactive and customizable dashboard. Provide a centralized view of the health of all resources. Minimize costs. What should you use?",
            "options": {
                "A": "Azure Service Health",
                "B": "Azure Monitor action groups",
                "C": "Azure Network Watcher",
                "D": "Azure Advisor"
            },
            "correct_answer": "A"
        }
    ]
    
    # Number of variations for each base question
    variations = num_questions // len(base_questions) + 1
    
    # Generate variations of each question
    for i in range(num_questions):
        # Select a base question
        base_idx = i % len(base_questions)
        base = base_questions[base_idx]
        
        # Create a variation
        question = {
            "id": i + 1,
            "question": f"{base['question']} (Variation {i//len(base_questions) + 1})",
            "options": base["options"].copy(),
            "correct_answer": base["correct_answer"]
        }
        
        questions.append(question)
        
        # Stop when we have enough questions
        if len(questions) >= num_questions:
            break
    
    return questions[:num_questions]  # Ensure we return exactly the requested number

def main():
    try:
        # Define paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, 'az104_questions.json')
        
        print(f"Script directory: {script_dir}")
        print(f"Output path: {output_path}")
        
        print(f"Generating 572 sample AZ-104 questions...")
        questions = generate_sample_questions(572)
        
        print(f"Generated {len(questions)} questions")
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(questions, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        
        # Verify the file was created
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"File created: {output_path}, Size: {file_size} bytes")
        else:
            print(f"WARNING: File was not created: {output_path}")
            
        print(f"Successfully saved {len(questions)} questions to {output_path}")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
