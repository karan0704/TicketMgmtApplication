package ticketmgmt.model;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder

public class LogFile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String filename;
    private String filePath;

    @ManyToOne
    @JoinColumn(name = "ticket_id")
    private Ticket ticket;
}
