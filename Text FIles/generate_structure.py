import os

# Define paths
resource_path = r"D:\Learning Projects\TicketMgmtApplication\src\main\resources"
config_path = r"D:\Learning Projects\TicketMgmtApplication\src\main\java\ticketmgmt\config"

# Content of application.properties
application_properties = """# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/ticketmgmt
spring.datasource.username=root
spring.datasource.password=your_mysql_password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA Config
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect

# Server
server.port=8080

# File Upload (optional)
file.upload-dir=uploads

# Logging
logging.level.org.hibernate.SQL=DEBUG
"""

# Content of CorsConfig.java
cors_config = """package ticketmgmt.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig {

    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                        .allowedOrigins("http://localhost:4200")  // Angular frontend
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*");
            }
        };
    }
}
"""

# Create directories
os.makedirs(resource_path, exist_ok=True)
os.makedirs(config_path, exist_ok=True)

# Write application.properties
with open(os.path.join(resource_path, "application.properties"), "w") as f:
    f.write(application_properties)

# Write CorsConfig.java
with open(os.path.join(config_path, "CorsConfig.java"), "w") as f:
    f.write(cors_config)

print("✅ application.properties and CorsConfig.java created successfully.")
