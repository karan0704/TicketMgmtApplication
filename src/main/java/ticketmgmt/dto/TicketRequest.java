package ticketmgmt.dto;

import lombok.Data;
import ticketmgmt.model.TicketPriority;

@Data

public class TicketRequest {
    private String customerName;
    private String issue;
    private TicketPriority priority;
}
