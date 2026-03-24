class CRMIntegration:
    def update_status(self, lead_id: str, status: str):
        # Mock CRM API Call
        return f"Integration: Updated CRM record status to '{status}'."

class SMSIntegration:
    def send_sms(self, phone: str, message: str):
        # Mock SMS API Call
        return f"Integration: SMS API triggered with message '{message}'."

class EmailIntegration:
    def send_email(self, email: str, sequence: str):
        # Mock Email API Call
        return f"Integration: Scheduled Email sequence '{sequence}' via Email API."

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
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), 'HOT Prospect'),
                    lambda lead, prob: self.sms.send_sms(lead.get('Phone', 'unknown'), 'priority offer code')
                ]
            },
            {
                "condition": lambda prob: 0.4 <= prob < 0.7,
                "classification": "MEDIUM Intent",
                "actions": [
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), 'Nurture'),
                    lambda lead, prob: self.email.send_email(lead.get('Email', 'unknown'), '#2')
                ]
            },
            {
                "condition": lambda prob: prob < 0.4,
                "classification": "LOW Intent",
                "actions": [
                    lambda lead, prob: self.crm.update_status(lead.get('id', 'new_lead'), 'generic re-targeting list')
                ]
            }
        ]

    def process_lead(self, lead_data: dict, probability: float):
        events = []
        events.append({"step": 1, "action": f"Received new lead processing request from {lead_data.get('LeadSource', 'Unknown')}."})
        
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
