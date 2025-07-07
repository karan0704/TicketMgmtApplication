package ticketmgmt.model;

import jakarta.persistence.*;
import lombok.*;
import java.util.List;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String name;
    private String email;
    private String phoneNumber;
    private String companyName;

    @OneToMany(mappedBy = "customer", cascade = CascadeType.ALL)
    private List<Ticket> tickets;
}
