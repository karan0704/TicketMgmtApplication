// src\main\java\ticketmgmt\dto\LogFileResponse.java
package ticketmgmt.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LogFileResponse {
    private Integer id;
    private String fileName; // Expose just the file name
    // You might also want to expose filePath if the frontend needs to download it
    // private String filePath;
}