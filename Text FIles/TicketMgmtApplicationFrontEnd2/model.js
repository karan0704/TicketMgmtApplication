// models.js
// Defines enums and conceptual data structures for clarity.

// Enums from backend (mapping Java enums to JavaScript objects)
const TicketStatus = {
    OPEN: 'OPEN',
    IN_PROGRESS: 'IN_PROGRESS',
    RESOLVED: 'RESOLVED',
    CLOSED: 'CLOSED',
    REOPENED: 'REOPENED',
};

const TicketPriority = {
    LOW: 'LOW',
    MEDIUM: 'MEDIUM',
    HIGH: 'HIGH',
    CRITICAL: 'CRITICAL',
};

// Data Transfer Objects (DTOs) - For documentation purposes in plain JS
// In a TypeScript project, these would be actual interfaces.

/*
// Example structure for AuditLog
const AuditLog = {
    id: 'number',
    message: 'string',
    timestamp: 'string', // LocalDateTime maps to String in JSON
    ticket: 'Ticket' // Reference to Ticket object
};

// Example structure for Customer
const Customer = {
    id: 'number',
    name: 'string',
    email: 'string',
    phoneNumber: 'string',
    companyName: 'string',
    tickets: 'Array<Ticket>' // List<Ticket>
};

// Example structure for Engineer
const Engineer = {
    id: 'number',
    name: 'string',
    email: 'string',
    designation: 'string',
    assignedTickets: 'Array<Ticket>' // List<Ticket>
};

// Example structure for IssueAttachment
const IssueAttachment = {
    id: 'number',
    fileName: 'string',
    filePath: 'string',
    ticket: 'Ticket'
};

// Example structure for LogFile
const LogFile = {
    id: 'number',
    filename: 'string',
    filePath: 'string',
    ticket: 'Ticket'
};

// Example structure for Ticket
const Ticket = {
    id: 'number',
    customerName: 'string',
    issueDescription: 'string',
    ticketStatus: 'TicketStatus', // Enum reference
    priority: 'TicketPriority',   // Enum reference
    ticketResponse: 'string',
    logFiles: 'Array<LogFile>',
    auditLogs: 'Array<AuditLog>',
    customer: 'Customer',
    assignedEngineer: 'Engineer'
};
*/
