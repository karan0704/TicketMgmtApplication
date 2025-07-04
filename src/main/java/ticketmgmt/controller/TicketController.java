package ticketmgmt.controller;

import org.apache.coyote.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.model.Ticket;
import ticketmgmt.service.TicketService;

@RestController
@RequestMapping("/api/tickets")
public class TicketController {
    @Autowired
    private TicketService ticketService;


    @PostMapping
    public ResponseEntity<Ticket> createTicket(@RequestBody Ticket ticket) {
        Ticket createdTicket = ticketService.createTicket(ticket.getCustomerName(), ticket.getIssueDescription());
        return ResponseEntity.ok(createdTicket);
    }

    @GetMapping
    public ResponseEntity<Ticket> getAllTickets() {
        return ResponseEntity.status(HttpStatus.OK).header();
    }

    @GetMapping("")
    public ResponseEntity<Ticket> getTicketById(int id) {
        return ticketService.findTicketById(id);
    }

    @PostMapping("")
    public void acknowledgeTicket(Ticket ticket) {
        ticketService.acknowledgeTicket(ticket);
    }

    public Response<>
}

