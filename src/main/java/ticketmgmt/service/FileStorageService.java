package ticketmgmt.service;

import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import ticketmgmt.model.LogFile;
import ticketmgmt.model.Ticket;
import ticketmgmt.repository.LogFileRepository;
import ticketmgmt.repository.TicketRepository;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class FileStorageService {

    private static final String UPLOAD_DIR = "uploads";

    private final TicketRepository ticketRepository;
    private final LogFileRepository logFileRepository;

    /**
     * Save a file to the local file system.
     *
     * @param file MultipartFile uploaded from frontend/Postman
     * @return the stored file's full path as String
     * @throws IOException if file can't be saved
     */
    public String saveFile(MultipartFile file) throws IOException {
        Path uploadPath = Paths.get(UPLOAD_DIR);

        if (!Files.exists(uploadPath)) {
            Files.createDirectories(uploadPath);
        }

        String filename = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        Path filePath = uploadPath.resolve(filename);
        file.transferTo(filePath.toFile());

        return filePath.toString();
    }

    /**
     * Save a file and associate it with a specific ticket.
     *
     * @param ticketId The ID of the ticket to attach the file to
     * @param filePath Full path of the uploaded file
     */
    @Transactional
    public void attachToTicket(Integer ticketId, String filePath) {
        Ticket ticket = ticketRepository.findById(ticketId)
                .orElseThrow(() -> new RuntimeException("Ticket not found"));

        LogFile logFile = LogFile.builder()
                .filePath(filePath)
                .ticket(ticket)
                .build();

        logFileRepository.save(logFile);
    }

    /**
     * Get all file paths attached to a ticket.
     *
     * @param ticketId The ticket ID
     * @return List of file paths as Strings
     */
    public List<String> getFilesByTicket(Integer ticketId) {
        return logFileRepository.findByTicketId(ticketId)
                .stream()
                .map(LogFile::getFilePath)
                .collect(Collectors.toList());
    }
}
