package ticketmgmt.model;

import jakarta.persistence.*;
import lombok.*;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Engineer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String name;
    private String email;
    private String designation;

    @OneToMany(mappedBy = "assignedEngineer", cascade = CascadeType.ALL)
    private List<Ticket> assignedTickets;
}
