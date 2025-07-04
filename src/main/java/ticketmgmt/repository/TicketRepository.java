package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ticketmgmt.model.Ticket;
import ticketmgmt.model.TicketStatus;

@Repository
public interface TicketRepository extends JpaRepository<Ticket, Integer> {

    public Ticket findByCustomerName(String  customerName);
    public Ticket findByTicketStatus(TicketStatus ticketStatus);



}
