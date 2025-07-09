package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.dto.TicketRequest;
import ticketmgmt.dto.TicketResponse;
import ticketmgmt.mapper.TicketMapper;
import ticketmgmt.model.TicketStatus; // Import TicketStatus
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

    // New endpoint to update ticket status
    @PutMapping("/{id}/status") // Using PUT for updates
    public ResponseEntity<TicketResponse> updateTicketStatus(@PathVariable Integer id, @RequestParam TicketStatus status) {
        var ticket = ticketService.updateTicketStatus(id, status);
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