package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.Engineer;

public interface EngineerRepository extends JpaRepository<Engineer, Integer> {
}
