package ticketmgmt.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ticketmgmt.model.Ticket;
import ticketmgmt.model.TicketStatus;
import ticketmgmt.repository.TicketRepository;

import java.util.List;

@Service
public class TicketService {

    @Autowired
    private TicketRepository ticketRepository;

    /*Create Ticket*/
    public Ticket createTicket(String customerName, String issueDescription) {
        Ticket ticket = new Ticket();
        ticket.setCustomerName(customerName);
        ticket.setIssueDescription(issueDescription);
        ticket.setTicketStatus(TicketStatus.Open);
        ticket.setResponse("Ticket created, under review");

        return ticketRepository.save(ticket);
    }

    /*FindBy ID Ticket*/
    public Ticket findTicketById(int ticketId) {
        return ticketRepository.findById(ticketId).orElse(null);
    }

    public List<Ticket> findAllTickets() {
        return null;
    }

    public void acknowledgeTicket(Ticket ticket) {
        ticketRepository.save(ticket);
    }

}
