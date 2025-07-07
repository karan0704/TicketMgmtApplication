package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ticketmgmt.service.FileStorageService;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileUploadController {

    private final FileStorageService fileStorageService;

    @PostMapping("/upload/{ticketId}")
    public ResponseEntity<String> upload(@RequestParam MultipartFile file, @PathVariable Integer ticketId) {
        try {
            String path = fileStorageService.saveFile(file);
            fileStorageService.attachToTicket(ticketId, path); // ticket -> logFile
            return ResponseEntity.ok("File saved and attached to ticket ID: " + ticketId);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Failed to upload file");
        }
    }

    @GetMapping("/ticket/{ticketId}")
    public ResponseEntity<?> getFiles(@PathVariable Integer ticketId) {
        return ResponseEntity.ok(fileStorageService.getFilesByTicket(ticketId));
    }
}
