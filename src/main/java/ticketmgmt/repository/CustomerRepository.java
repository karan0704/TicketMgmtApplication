package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.Customer;

import java.util.Optional;

public interface CustomerRepository extends JpaRepository<Customer, Integer> {
    Optional<Customer> findByName(String name);
}
