package ticketmgmt.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ticketmgmt.model.AuditLog;
import ticketmgmt.model.Ticket;
import ticketmgmt.repository.AuditLogRepository;

import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class AuditLogService {

    private final AuditLogRepository auditLogRepository;

    public void log(Ticket ticket, String message) {
        AuditLog log = AuditLog.builder()
                .ticket(ticket)
                .message(message)
                .timestamp(LocalDateTime.now())
                .build();
        auditLogRepository.save(log);
    }
}
