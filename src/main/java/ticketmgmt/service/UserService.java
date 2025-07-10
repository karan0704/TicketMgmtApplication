package ticketmgmt.service;

import ticketmgmt.model.User;

public interface UserService {
    User saveUser(User user);
    User findByUsername(String username);
    User findByEmail(String email);
    boolean existsByUsername(String username);
    boolean existsByEmail(String email);
}
