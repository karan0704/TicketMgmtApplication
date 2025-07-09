package ticketmgmt.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.model.AppUser;
import ticketmgmt.repository.AppUserRepository;
import ticketmgmt.util.JwtUtil; // Import JwtUtil
import ticketmgmt.service.AppUserDetailsService; // Import AppUserDetailsService

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager; // Renamed for clarity
    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil; // Inject JwtUtil
    private final AppUserDetailsService userDetailsService; // Inject AppUserDetailsService

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody AppUser user) {
        try {
            if (userRepository.findByUsername(user.getUsername()).isPresent()) {
                Map<String, String> error = new HashMap<>();
                error.put("error", "Username already exists");
                return ResponseEntity.badRequest().body(error);
            }

            user.setPassword(passwordEncoder.encode(user.getPassword()));
            AppUser savedUser = userRepository.save(user);

            Map<String, Object> response = new HashMap<>();
            response.put("message", "User registered successfully");
            response.put("username", savedUser.getUsername());
            response.put("role", savedUser.getRole().name());

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Registration failed: " + e.getMessage()); // Provide more detail
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody AppUser user) {
        try {
            // Authenticate the user using Spring Security's AuthenticationManager
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(user.getUsername(), user.getPassword()));

            // Set the authentication in the SecurityContext (optional for stateless, but good practice)
            SecurityContextHolder.getContext().setAuthentication(authentication);

            // Load user details to generate token with correct authorities/roles
            final org.springframework.security.core.userdetails.UserDetails userDetails =
                    userDetailsService.loadUserByUsername(user.getUsername());

            // Generate JWT token
            final String jwt = jwtUtil.generateToken(userDetails);

            AppUser loggedInUser = userRepository.findByUsername(user.getUsername())
                    .orElseThrow(() -> new RuntimeException("User not found after successful authentication."));

            Map<String, Object> response = new HashMap<>();
            response.put("message", "Login successful");
            response.put("username", loggedInUser.getUsername());
            response.put("role", loggedInUser.getRole().name());
            response.put("userId", loggedInUser.getId());
            response.put("token", jwt); // Return the JWT token

            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Invalid credentials: " + e.getMessage()); // Provide more detail
            return ResponseEntity.badRequest().body(error);
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout() {
        // For JWT, logout is primarily client-side (removing the token).
        // Clearing the server-side SecurityContext is good practice but not strictly necessary for stateless.
        SecurityContextHolder.getContext().setAuthentication(null);
        Map<String, String> response = new HashMap<>();
        response.put("message", "Logged out successfully (client-side token removal expected)");
        return ResponseEntity.ok(response);
    }
}
