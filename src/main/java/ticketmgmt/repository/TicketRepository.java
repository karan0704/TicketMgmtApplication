package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.Ticket;

public interface TicketRepository extends JpaRepository<Ticket, Integer> {
}
