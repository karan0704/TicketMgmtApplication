package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ticketmgmt.dto.ApiResponse; // Import the new DTO
import ticketmgmt.service.FileStorageService;

@RestController
@RequestMapping("/api/files")
@RequiredArgsConstructor
public class FileUploadController {

    private final FileStorageService fileStorageService;

    @PostMapping("/upload/{ticketId}")
    public ResponseEntity<ApiResponse> upload(@RequestParam MultipartFile file, @PathVariable Integer ticketId) {
        try {
            String path = fileStorageService.saveFile(file);
            fileStorageService.attachToTicket(ticketId, path); // ticket -> logFile
            return ResponseEntity.ok(ApiResponse.builder().success(true).message("File uploaded successfully!").build());
        } catch (Exception e) {
            e.printStackTrace(); // Log the actual exception for debugging on the server side
            return ResponseEntity.internalServerError().body(ApiResponse.builder().success(false).message("Failed to upload file: " + e.getMessage()).build());
        }
    }

    @GetMapping("/ticket/{ticketId}")
    public ResponseEntity<java.util.List<String>> getFiles(@PathVariable Integer ticketId) {
        return ResponseEntity.ok(fileStorageService.getFilesByTicket(ticketId));
    }
}