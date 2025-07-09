package ticketmgmt.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Component
public class JwtUtil {

    // Secret key for JWT signing. This should be a strong, randomly generated key.
    // In a production environment, store this securely (e.g., environment variable).
    @Value("${jwt.secret}")
    private String SECRET_KEY;

    // Expiration time for the token (e.g., 10 hours)
    @Value("${jwt.expiration}")
    private long JWT_TOKEN_VALIDITY; // in milliseconds

    // Retrieve username from JWT token
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    // Retrieve expiration date from a JWT token
    public Date extractExpiration(String token) {
        return extractClaim(token, Claims::getExpiration);
    }

    // Generic method to extract a specific claim from the token
    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        final Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    // Retrieve all claims from the token
    private Claims extractAllClaims(String token) {
        return Jwts.parserBuilder().setSigningKey(getSigningKey()).build().parseClaimsJws(token).getBody();
    }

    // Check if the token has expired
    private Boolean isTokenExpired(String token) {
        return extractExpiration(token).before(new Date());
    }

    // Generate token for user
    public String generateToken(UserDetails userDetails) {
        Map<String, Object> claims = new HashMap<>();
        // Add roles to claims
        claims.put("roles", userDetails.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(java.util.stream.Collectors.toList()));
        return createToken(claims, userDetails.getUsername());
    }

    // Create the token
    private String createToken(Map<String, Object> claims, String subject) {
        return Jwts.builder()
                .setClaims(claims)
                .setSubject(subject)
                .setIssuedAt(new Date(System.currentTimeMillis()))
                .setExpiration(new Date(System.currentTimeMillis() + JWT_TOKEN_VALIDITY))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    // Validate token
    public Boolean validateToken(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return (username.equals(userDetails.getUsername()) && !isTokenExpired(token));
    }

    // Get the signing key from the secret
    private Key getSigningKey() {
        // Use recommended method to create a secure key for HS256
        if (SECRET_KEY == null || SECRET_KEY.trim().isEmpty()) {
            // If no secret key is provided, generate a secure key
            return Keys.secretKeyFor(SignatureAlgorithm.HS256);
        }

        try {
            byte[] keyBytes = Decoders.BASE64.decode(SECRET_KEY);
            // Verify key length meets requirements (≥ 256 bits for HS256)
            if (keyBytes.length * 8 < 256) {
                throw new IllegalArgumentException("The JWT secret key is too short");
            }
            return Keys.hmacShaKeyFor(keyBytes);
        } catch (Exception e) {
            // Fallback to a secure generated key if there's any issue with the provided key
            return Keys.secretKeyFor(SignatureAlgorithm.HS256);
        }
    }
}
