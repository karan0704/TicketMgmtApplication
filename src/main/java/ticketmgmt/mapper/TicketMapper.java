package ticketmgmt.mapper;

import org.springframework.stereotype.Component;
import ticketmgmt.dto.TicketResponse;
import ticketmgmt.dto.CustomerResponse;
import ticketmgmt.dto.EngineerResponse;
import ticketmgmt.model.Ticket;
import ticketmgmt.model.Customer;
import ticketmgmt.model.Engineer;

@Component
public class TicketMapper {

    public TicketResponse toResponse(Ticket ticket) {
        return TicketResponse.builder()
                .id(ticket.getId())
                .issueDescription(ticket.getIssueDescription())
                .ticketStatus(ticket.getTicketStatus())
                .priority(ticket.getPriority())
                .ticketResponse(ticket.getTicketResponse())
                .customer(ticket.getCustomer() != null ? toCustomerResponse(ticket.getCustomer()) : null)
                .assignedEngineer(ticket.getAssignedEngineer() != null ? toEngineerResponse(ticket.getAssignedEngineer()) : null)
                .build();
    }

    private CustomerResponse toCustomerResponse(Customer customer) {
        return CustomerResponse.builder()
                .id(customer.getId())
                .name(customer.getName())
                .email(customer.getEmail())
                .phoneNumber(customer.getPhoneNumber())
                .companyName(customer.getCompanyName())
                .build();
    }

    private EngineerResponse toEngineerResponse(Engineer engineer) {
        return EngineerResponse.builder()
                .id(engineer.getId())
                .name(engineer.getName())
                .email(engineer.getEmail())
                .designation(engineer.getDesignation())
                .build();
    }
}