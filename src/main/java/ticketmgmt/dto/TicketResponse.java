package ticketmgmt.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import ticketmgmt.model.TicketPriority;
import ticketmgmt.model.TicketStatus;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TicketResponse {
    private Integer id;
    private String issueDescription;
    private TicketStatus ticketStatus;
    private TicketPriority priority;
    private String ticketResponse;
    private CustomerResponse customer;
    private EngineerResponse assignedEngineer;
}
