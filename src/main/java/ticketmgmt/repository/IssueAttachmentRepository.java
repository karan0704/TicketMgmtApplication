package ticketmgmt.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import ticketmgmt.model.IssueAttachment;

public interface IssueAttachmentRepository extends JpaRepository<IssueAttachment,Integer> {
}
