package ticketmgmt.model;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity
public class Ticket {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int ticketId;
    private String issueDescription;
    private String customerName;




    private String response;

    @Enumerated(EnumType.STRING)
    TicketStatus ticketStatus;

    @ManyToOne(cascade = CascadeType.ALL)
    Ticket ticket;
}
