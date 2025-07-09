// src\main\java\ticketmgmt\dto\AuditLogResponse.java
package ticketmgmt.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AuditLogResponse {
    private Integer id;
    private String message;
    private LocalDateTime timestamp;
}