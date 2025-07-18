package ticketmgmt;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "ticketmgmt")
public class TicketMgmtApplication {

    public static void main(String[] args) {
        SpringApplication.run(TicketMgmtApplication.class, args);
    }

}
