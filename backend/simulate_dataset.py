import pandas as pd
from workflow_engine import WorkflowOrchestrator
import sys

def main():
    file_path = r'c:\Users\HP\Downloads\placement_project\placement_project\leads_dataset.xlsx'
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading excel file: {e}")
        sys.exit(1)

    orchestrator = WorkflowOrchestrator()

    print("======================================================")
    print("INTELLIGENT WORKFLOW AUTOMATION: BATCH EXECUTION TRACE")
    print("======================================================\n")

    for index, row in df.iterrows():
        lead_data = {
            'id': f"L_{index+1000}",
            'Name': row.get('Name', 'Unknown'),
            'Phone': row.get('Phone', 'Unknown'),
            'Email': 'contact@example.com', # fallback since email wasn't explicitly requested
            'Status': row.get('Status', 'New'),
            'Interest Level': row.get('Interest Level', 'Low'),
            'LeadSource': 'Batch Excel Dataset'
        }
        
        # Determine internal ML probability equivalent from "Interest Level"
        interest = str(row.get('Interest Level', 'Low')).strip().lower()
        if interest == 'high':
            prob = 0.85
        elif interest == 'medium':
            prob = 0.55
        else:
            prob = 0.20
            
        print(f"[{lead_data['id']}] Processing New Trigger -> Name: {lead_data['Name']} | Status: {lead_data['Status']} | Interest Base: {lead_data['Interest Level']}")
        
        events = orchestrator.process_lead(lead_data, prob)
        
        for e in events:
            print(f"   -> Step {e['step']}: {e['action']}")
            
        print("-" * 60)

if __name__ == "__main__":
    main()
