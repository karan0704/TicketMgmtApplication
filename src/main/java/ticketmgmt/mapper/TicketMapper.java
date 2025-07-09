// src\main\java\ticketmgmt\mapper\TicketMapper.java
package ticketmgmt.mapper;

import org.springframework.stereotype.Component;
import ticketmgmt.dto.TicketResponse;
import ticketmgmt.dto.CustomerResponse;
import ticketmgmt.dto.EngineerResponse;
import ticketmgmt.dto.LogFileResponse; // Import LogFileResponse
import ticketmgmt.dto.AuditLogResponse; // Import AuditLogResponse
import ticketmgmt.model.Ticket;
import ticketmgmt.model.Customer;
import ticketmgmt.model.Engineer;
import ticketmgmt.model.LogFile; // Import LogFile model
import ticketmgmt.model.AuditLog; // Import AuditLog model

import java.util.stream.Collectors; // Import Collectors

@Component
public class TicketMapper {

    public TicketResponse toResponse(Ticket ticket) {
        return TicketResponse.builder()
                .id(ticket.getId())
                .issueDescription(ticket.getIssueDescription())
                .ticketStatus(ticket.getTicketStatus())
                .priority(ticket.getPriority())
                .ticketResponse(ticket.getTicketResponse())
                .customer(ticket.getCustomer() != null ? toCustomerResponse(ticket.getCustomer()) : null)
                .assignedEngineer(ticket.getAssignedEngineer() != null ? toEngineerResponse(ticket.getAssignedEngineer()) : null)
                .logFiles(ticket.getLogFiles() != null ? ticket.getLogFiles().stream()
                        .map(this::toLogFileResponse)
                        .collect(Collectors.toList()) : null) // Map logFiles
                .auditLogs(ticket.getAuditLogs() != null ? ticket.getAuditLogs().stream()
                        .map(this::toAuditLogResponse)
                        .collect(Collectors.toList()) : null) // Map auditLogs
                .build();
    }

    private CustomerResponse toCustomerResponse(Customer customer) {
        return CustomerResponse.builder()
                .id(customer.getId())
                .name(customer.getName())
                .email(customer.getEmail())
                .phoneNumber(customer.getPhoneNumber())
                .companyName(customer.getCompanyName())
                .build();
    }

    private EngineerResponse toEngineerResponse(Engineer engineer) {
        return EngineerResponse.builder()
                .id(engineer.getId())
                .name(engineer.getName())
                .email(engineer.getEmail())
                .designation(engineer.getDesignation())
                .build();
    }

    // New method to map LogFile to LogFileResponse
    private LogFileResponse toLogFileResponse(LogFile logFile) {
        // Extract just the filename from the filePath for display
        String fileName = logFile.getFilePath() != null ?
                logFile.getFilePath().substring(logFile.getFilePath().lastIndexOf('/') + 1) :
                null;
        if (fileName == null && logFile.getFilePath() != null) { // Handle Windows paths
            fileName = logFile.getFilePath().substring(logFile.getFilePath().lastIndexOf('\\') + 1);
        }
        return LogFileResponse.builder()
                .id(logFile.getId())
                .fileName(fileName)
                .build();
    }

    // New method to map AuditLog to AuditLogResponse
    private AuditLogResponse toAuditLogResponse(AuditLog auditLog) {
        return AuditLogResponse.builder()
                .id(auditLog.getId())
                .message(auditLog.getMessage())
                .timestamp(auditLog.getTimestamp())
                .build();
    }
}