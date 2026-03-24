class CRMIntegration:
    def update_status(self, lead_id: str, lead_name: str, status: str):
        # Mock CRM API Call
        return f"Integration: Updated CRM record for '{lead_name}' to status '{status}'."

class SMSIntegration:
    def send_sms(self, phone: str, message: str):
        # Mock SMS API Call
        return f"Integration: SMS API triggered for {phone} with '{message}'."

class EmailIntegration:
    def send_email(self, email: str, sequence: str):
        # Mock Email API Call
        return f"Integration: Scheduled Email sequence '{sequence}' for {email}."

class WorkflowOrchestrator:
    def __init__(self):
        self.crm = CRMIntegration()
        self.sms = SMSIntegration()
        self.email = EmailIntegration()
        
        # Dynamic rules for conditional routing
        self.rules = [
            {
                "condition": lambda prob: prob >= 0.7,
                "classification": "HIGH Intent",
                "actions": [
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), lead.get('Name', 'Unknown'), 'HOT Prospect'),
                    lambda lead, prob: self.sms.send_sms(lead.get('Phone', 'unknown'), 'Priority Offer Code')
                ]
            },
            {
                "condition": lambda prob: 0.4 <= prob < 0.7,
                "classification": "MEDIUM Intent",
                "actions": [
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), lead.get('Name', 'Unknown'), 'Nurture'),
                    lambda lead, prob: self.email.send_email(lead.get('Email', 'unknown'), '#2 Follow-up')
                ]
            },
            {
                "condition": lambda prob: prob < 0.4,
                "classification": "LOW Intent",
                "actions": [
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), lead.get('Name', 'Unknown'), 'Generic Re-targeting List')
                ]
            }
        ]

    def process_lead(self, lead_data: dict, probability: float):
        events = []
        lead_identifier = f"{lead_data.get('Name', 'Unknown')} ({lead_data.get('LeadSource', 'Unknown')})"
        events.append({"step": 1, "action": f"Received new lead processing request for: {lead_identifier}."})
        
        step_counter = 2
        for rule in self.rules:
            if rule["condition"](probability):
                events.append({"step": step_counter, "action": f"Lead Classification: {rule['classification']} (Score: {probability:.2f})."})
                step_counter += 1
                for action in rule["actions"]:
                    result = action(lead_data, probability)
                    events.append({"step": step_counter, "action": result})
                    step_counter += 1
                break
        
        events.append({"step": step_counter, "action": "Workflow execution complete."})
        return events
