package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.LogFile;

import java.util.List;

public interface LogFileRepository extends JpaRepository<LogFile, Integer> {
    List<LogFile> findByTicketId(Integer ticketId);
}
