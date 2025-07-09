/*package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.dto.TicketRequest;
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
    public ResponseEntity<Ticket> createTicket(//@RequestParam String customerName, @RequestParam String issue,@RequestParam TicketPriority priority
                                               @RequestBody TicketRequest request) {
        Ticket created = ticketService.createTicket(request.getCustomerName(), request.getIssue(), request.getPriority());
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
}*/
package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.dto.TicketRequest;
import ticketmgmt.dto.TicketResponse;
import ticketmgmt.mapper.TicketMapper;
import ticketmgmt.service.TicketService;

import jakarta.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/tickets")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class TicketController {

    private final TicketService ticketService;
    private final TicketMapper ticketMapper;

    @PostMapping("/create")
    public ResponseEntity<TicketResponse> createTicket(@Valid @RequestBody TicketRequest request) {
        var ticket = ticketService.createTicket(request.getCustomerName(), request.getIssue(), request.getPriority());
        return ResponseEntity.ok(ticketMapper.toResponse(ticket));
    }

    @GetMapping("/{id}")
    public ResponseEntity<TicketResponse> getTicket(@PathVariable Integer id) {
        return ticketService.getTicketById(id)
                .map(ticket -> ResponseEntity.ok(ticketMapper.toResponse(ticket)))
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/{id}/assign/{engineerId}")
    public ResponseEntity<TicketResponse> assign(@PathVariable Integer id, @PathVariable Integer engineerId) {
        var ticket = ticketService.assignTicketToEngineer(id, engineerId);
        return ResponseEntity.ok(ticketMapper.toResponse(ticket));
    }

    @PostMapping("/{id}/unassign")
    public ResponseEntity<TicketResponse> unassign(@PathVariable Integer id) {
        var ticket = ticketService.unassignEngineer(id);
        return ResponseEntity.ok(ticketMapper.toResponse(ticket));
    }

    @GetMapping("/all")
    public ResponseEntity<List<TicketResponse>> getAllTickets() {
        var tickets = ticketService.getAllTickets().stream()
                .map(ticketMapper::toResponse)
                .collect(Collectors.toList());
        return ResponseEntity.ok(tickets);
    }
}
