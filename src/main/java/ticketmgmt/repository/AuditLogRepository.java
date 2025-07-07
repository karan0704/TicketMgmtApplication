package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.AuditLog;

public interface AuditLogRepository extends JpaRepository<AuditLog, Integer> {
}
