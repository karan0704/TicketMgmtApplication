package ticketmgmt.model;

import jakarta.persistence.CascadeType;
import jakarta.persistence.ManyToOne;

public class IssueAttachment {
    private Integer id;
    private byte[] imageData;
    private String comment;

    @ManyToOne(cascade = CascadeType.ALL)
    Ticket ticket;
}
