package ticketmgmt.controller;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.context.HttpSessionSecurityContextRepository;
import org.springframework.web.bind.annotation.*;
import ticketmgmt.dto.LoginRequest;
import ticketmgmt.dto.RegistrationRequest;
import ticketmgmt.model.User;
import ticketmgmt.service.UserService;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final UserService userService;
    private final PasswordEncoder passwordEncoder;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest loginRequest, HttpServletRequest request) {
        try {
            // Authenticate user credentials
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            loginRequest.getUsername(), 
                            loginRequest.getPassword()
                    )
            );

            // Set authentication in security context
            SecurityContextHolder.getContext().setAuthentication(authentication);

            // Create session and store security context
            HttpSession session = request.getSession(true);
            session.setAttribute(HttpSessionSecurityContextRepository.SPRING_SECURITY_CONTEXT_KEY, 
                    SecurityContextHolder.getContext());

            // Create response with session information
            Map<String, Object> response = new HashMap<>();
            response.put("status", "success");
            response.put("message", "Login successful");
            response.put("username", loginRequest.getUsername());

            return ResponseEntity.ok(response);
        } catch (BadCredentialsException e) {
            Map<String, String> response = new HashMap<>();
            response.put("status", "error");
            response.put("message", "Invalid username or password");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
        }
    }

    @PostMapping("/register")
    public ResponseEntity<?> register(@RequestBody RegistrationRequest registrationRequest) {
        // Check if username already exists
        if (userService.existsByUsername(registrationRequest.getUsername())) {
            Map<String, String> response = new HashMap<>();
            response.put("status", "error");
            response.put("message", "Username already exists");
            return ResponseEntity.badRequest().body(response);
        }

        // Check if email already exists
        if (userService.existsByEmail(registrationRequest.getEmail())) {
            Map<String, String> response = new HashMap<>();
            response.put("status", "error");
            response.put("message", "Email already exists");
            return ResponseEntity.badRequest().body(response);
        }

        // Create new user
        User user = new User();
        user.setUsername(registrationRequest.getUsername());
        user.setEmail(registrationRequest.getEmail());
        user.setPassword(passwordEncoder.encode(registrationRequest.getPassword()));

        userService.saveUser(user);

        Map<String, String> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "User registered successfully");

        return ResponseEntity.ok(response);
    }

    @GetMapping("/login-success")
    public ResponseEntity<?> loginSuccess() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "You have been logged in successfully");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/login-failure")
    public ResponseEntity<?> loginFailure() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "error");
        response.put("message", "Login failed: Invalid credentials");
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(response);
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpServletRequest request, HttpServletResponse response) {
        HttpSession session = request.getSession(false);
        if (session != null) {
            session.invalidate();
        }
        SecurityContextHolder.clearContext();

        Map<String, String> responseMap = new HashMap<>();
        responseMap.put("status", "success");
        responseMap.put("message", "Logged out successfully");

        return ResponseEntity.ok(responseMap);
    }

    @GetMapping("/logout-success")
    public ResponseEntity<?> logoutSuccess() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "success");
        response.put("message", "You have been logged out successfully");
        return ResponseEntity.ok(response);
    }

    @GetMapping("/user-info")
    public ResponseEntity<?> getUserInfo() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || 
                "anonymousUser".equals(authentication.getPrincipal())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("User not authenticated");
        }

        UserDetails userDetails = (UserDetails) authentication.getPrincipal();
        Map<String, Object> response = new HashMap<>();
        response.put("username", userDetails.getUsername());
        response.put("authorities", userDetails.getAuthorities());

        return ResponseEntity.ok(response);
    }
}