# Amazon Connect Child Welfare Flow

##  Overview
This **Amazon Connect call flow** is designed to provide **efficient and automated** support for **Child Welfare services**. The system allows callers to:
- **To Report child abuse,or any other issues**
- **Schedule, reschedule, or cancel therapy appointments**
- **Leave a voicemail if agents are unavailable**
- **Receive a callback instead of waiting in a queue**
- **Receive appointment confirmations via email**
- **Check working hours and holiday closures before routing calls**

### Technologies Used
**Amazon Connect** (Call handling, IVR system)  
**Amazon Lex** (Natural Language Processing for self-service options)  
**AWS Lambda** (Backend logic for appointment management)  
**Amazon DynamoDB** (Appointment data storage)  
**Amazon SES** (Email notifications for confirmations)  
**Amazon API Gateway** (Enables web-based appointment lookup)  

## Call Flows in This Project
This repository contains the following **Amazon Connect Call Flows**:

### Caller Entry Main Path (Initial Call Routing)

### Purpose:
This flow serves as the entry point for all callers and determines the next step based on user input.
It ensures to check holiday dates,working hours and staffing availability options are checked before transferring calls.
Provides the main menu options:

Press 1 → Report child abuse
Press 2 → Lawyer/legal assistance
Press 3 → School personnel support
Press 4 → Therapy appointment self-service
Press 5 → General appointment booking and for various other options, (Agent books an appointment for the user through web UI)

It basically manages **initial call routing, staffing availablity, and holiday checks** before directing the caller.

### Therapy Self-Service Appointment
Purpose:
Allows users to book, reschedule, or cancel appointments automatically via Amazon Lex and DynamoDB.
Key Functions:User chooses a therapy appointment option (new, reschedule, cancel).
Amazon Lex bot handles scheduling queries.
AWS Lambda checks for available slots in DynamoDB.

It Automates **therapy appointment booking, rescheduling, and cancellation** using Amazon Lex.

### Interruptible Queue Flow with Callback
Purpose:
Reduces wait times by allowing customers to request a callback instead of waiting in a queue.
Key Functions:Plays a queue message while the caller waits.
Offers a callback option every 30 seconds.
If chosen, stores the user's phone number for later callbacks.
It Provides **callback options** for users in a queue, reducing wait times.

### Voicemail Flow
Purpose:
Ensures callers can leave a voicemail when agents are unavailable.
Key Functions: Records voicemail messages.
Stores voicemail recordings securely.
Emails the voicemail to an agent.

It Allows callers to **leave a voicemail** when no agent is available, and sends the recording via **email**.


### Resources used for building the voicemail flow:
**Integration:**  
This voicemail flow is based on the **Amazon Connect Voicemail Express** module:  
🔗 [Amazon Connect Voicemail Express GitHub](https://github.com/amazon-connect/voicemail-express-amazon-connect)

---

## How This System Improves Child Welfare Services
**Reduces agent workload** through **self-service automation**.  
**Prevents long wait times** using **callback queues**.  
**Eliminates manual appointment scheduling** through **Lex and DynamoDB**.  
**Provides 24/7 voicemail support** when agents are unavailable. 
** Agents can book appointments for users while they are on call **through a Web UI** and can also **check the appointment status**.

