package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ticketmgmt.service.FileStorageService;
//
//@RestController
//@RequestMapping("/api/files")
//@RequiredArgsConstructor
public class FileUploadController {

   /* private final FileStorageService fileStorageService;

    @PostMapping("/upload")
    public ResponseEntity<String> upload(@RequestParam MultipartFile file) {
        try {
            String path = fileStorageService.saveFile(file);
            return ResponseEntity.ok("File saved at: " + path);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("Failed to upload file");
        }/*
    }
}
