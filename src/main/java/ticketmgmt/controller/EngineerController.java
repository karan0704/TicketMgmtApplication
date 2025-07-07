package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.model.Engineer;
import ticketmgmt.repository.EngineerRepository; // Make sure this import is correct

import java.util.List;

@RestController
@RequestMapping("/api/engineers")
@RequiredArgsConstructor
public class EngineerController {

    private final EngineerRepository engineerRepository; // Inject EngineerRepository

    @GetMapping
    public ResponseEntity<List<Engineer>> getAllEngineers() {
        // This endpoint will return all engineers from the database
        return ResponseEntity.ok(engineerRepository.findAll());
    }

    // Optional: Add an endpoint to create engineers for testing
    @PostMapping
    public ResponseEntity<Engineer> createEngineer(@RequestBody Engineer engineer) {
        return ResponseEntity.ok(engineerRepository.save(engineer));
    }
}
    