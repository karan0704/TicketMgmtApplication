package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.model.Ticket;
import ticketmgmt.model.TicketPriority;
import ticketmgmt.service.TicketService;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/tickets")
@RequiredArgsConstructor
public class TicketController {

    private final TicketService ticketService;

    @PostMapping("/create")
    public ResponseEntity<Ticket> createTicket(@RequestParam String customerName,
                                               @RequestParam String issue,
                                               @RequestParam TicketPriority priority) {
        Ticket created = ticketService.createTicket(customerName, issue, priority);
        return ResponseEntity.ok(created);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Ticket> getTicket(@PathVariable Integer id) {
        Optional<Ticket> ticket = ticketService.getTicketById(id);
        return ticket.map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{id}/assign/{engineerId}")
    public ResponseEntity<Ticket> assign(@PathVariable Integer id, @PathVariable Integer engineerId) {
        return ResponseEntity.ok(ticketService.assignTicketToEngineer(id, engineerId));
    }

    @PostMapping("/{id}/unassign")
    public ResponseEntity<Ticket> unassign(@PathVariable Integer id) {
        return ResponseEntity.ok(ticketService.unassignEngineer(id));
    }

    @GetMapping("/all")
    public ResponseEntity<List<Ticket>> getAllTickets() {
        return ResponseEntity.ok(ticketService.getAllTickets());
    }
}
