# Intelligent Workflow Automation System
**Project Design & Execution Document**

---

## 1. Goal Description
The objective of this project is to automate end-to-end workflows across CRM, ERP, and messaging platforms with dynamic AI decision-making. The system processes incoming lead data (Name, Phone, Status, Interest Level) and orchestrates conditional actions in real-time.

## 2. Implemented Features
- **Workflow Orchestration Engine**: Built a scalable, modular Engine (`WorkflowOrchestrator`) in Python to completely replace hardcoded logic.
- **Conditional Logic & Dynamic Adaptation**: Rules evaluate the input triggers dynamically to classify users into High, Medium, or Low intent sequences.
- **Integration Across Systems**: Developed isolated mock systems (`CRMIntegration`, `SMSIntegration`, `EmailIntegration`) that get invoked sequentially based on the engine's routes.

---

## 3. Expected Deliverables

### A. Workflow Diagram
```mermaid
flowchart TD
    A[New Lead / Status Change Trigger] --> B{AI Orchestrator Engine}
    B --> C[Analyze Lead Data]
    C --> D{Interest Level?}
    
    D -->|High| E[Mark as 'Hot Prospect']
    E --> F[CRM: Update Status to Priority]
    F --> G[SMS API: Send Priority Offer]
    
    D -->|Medium| H[Mark as 'Nurture']
    H --> I[CRM: Update Status to Nurture]
    I --> J[Email API: Send Follow-up Sequence]
    
    D -->|Low| K[Mark as 'Cold']
    K --> L[CRM: Add to Retargeting List]
    
    G --> M[Log Execution Event]
    J --> M
    L --> M
    M --> N[End Workflow]
```

### B. Integration Architecture
```mermaid
architecture-beta
    group api(cloud)[API Layer]
    group core(server)[Core System]
    group external(database)[External Integrations]
    
    service trigger(internet)[Event Trigger] in api
    service orchestrator(server)[Workflow Orchestrator] in core
    service ai(disk)[AI Decision Engine] in core
    
    service crm(database)[Mock CRM] in external
    service email(cloud)[Email Services] in external
    service sms(cloud)[SMS Gateway] in external

    trigger:R --> L:orchestrator
    orchestrator:T <--> B:ai
    orchestrator:R --> L:crm
    orchestrator:R --> L:email
    orchestrator:R --> L:sms
```

### C. Sample Execution Flow
**System Sequence Trace**
```mermaid
sequenceDiagram
    participant Webhook as Event Trigger
    participant Orchestrator
    participant AI as AI Engine
    participant CRM as CRM System
    participant SMS as SMS API

    Webhook->>Orchestrator: Send Lead {Name: "John Doe", Phone: "555-0100", Interest: "High"}
    Orchestrator->>AI: Request Action Logic
    AI-->>Orchestrator: Route: High Intent -> [Sync CRM, Send Immediate SMS]
    
    Orchestrator->>CRM: POST /leads (Update Status to 'Hot Prospect')
    CRM-->>Orchestrator: 200 OK
    
    Orchestrator->>SMS: POST /send (Send priority offer code)
    SMS-->>Orchestrator: 202 Accepted
    
    Orchestrator->>Orchestrator: Log Trace [Step 1: CRM Sync, Step 2: SMS Sent]
    Orchestrator-->>Webhook: Workflow Completed
```

**Batch Processing Output Log (`simulate_dataset.py`)**
```text
======================================================
INTELLIGENT WORKFLOW AUTOMATION: BATCH EXECUTION TRACE
======================================================

[L_1000] Processing New Trigger -> Name: Aarav Sharma | Status: New | Interest Base: High
   -> Step 1: Received new lead processing request from Batch Excel Dataset.
   -> Step 2: Lead Classification: HIGH Intent (Score: 0.85).
   -> Step 3: Integration: Updated CRM record status to 'HOT Prospect'.
   -> Step 4: Integration: SMS API triggered with message 'priority offer code'.
   -> Step 5: Workflow execution complete.
------------------------------------------------------------
```
