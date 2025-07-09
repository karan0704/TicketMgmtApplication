package ticketmgmt.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ticketmgmt.model.*;
import ticketmgmt.repository.CustomerRepository;
import ticketmgmt.repository.EngineerRepository;
import ticketmgmt.repository.TicketRepository;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class TicketService {

    private final TicketRepository ticketRepository;
    private final CustomerRepository customerRepository;
    private final EngineerRepository engineerRepository;
    private final AuditLogService auditLogService;

    // Create new ticket and associate with a customer
    public Ticket createTicket(String customerName, String issue, TicketPriority priority) {
        Customer customer = customerRepository.findByName(customerName)
                .orElseThrow(() -> new RuntimeException("Customer not found"));

        Ticket ticket = Ticket.builder()
                //.customerName(customerName)
                .issueDescription(issue)
                .ticketStatus(TicketStatus.OPEN)
                .priority(priority)
                .ticketResponse("Ticket created")
                .customer(customer)
                .build();

        Ticket savedTicket = ticketRepository.save(ticket);
        auditLogService.log(savedTicket, "Ticket created");
        return savedTicket;
    }

    // Get a ticket by ID
    public Optional<Ticket> getTicketById(Integer ticketId) {
        return ticketRepository.findById(ticketId);
    }

    // Engineer chooses (claims) a ticket
    public Ticket assignTicketToEngineer(Integer ticketId, Integer engineerId) {
        Ticket ticket = ticketRepository.findById(ticketId)
                .orElseThrow(() -> new RuntimeException("Ticket not found"));
        Engineer engineer = engineerRepository.findById(engineerId)
                .orElseThrow(() -> new RuntimeException("Engineer not found"));

        ticket.setAssignedEngineer(engineer);
        auditLogService.log(ticket, "Assigned to engineer: " + engineer.getName());
        return ticketRepository.save(ticket);
    }

    // Engineer removes themselves from ticket
    public Ticket unassignEngineer(Integer ticketId) {
        Ticket ticket = ticketRepository.findById(ticketId)
                .orElseThrow(() -> new RuntimeException("Ticket not found"));

        ticket.setAssignedEngineer(null);
        auditLogService.log(ticket, "Unassigned engineer");
        return ticketRepository.save(ticket);
    }

    // Get all tickets
    public List<Ticket> getAllTickets() {
        return ticketRepository.findAll();
    }
}
