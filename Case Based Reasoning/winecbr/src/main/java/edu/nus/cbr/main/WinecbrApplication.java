package edu.nus.cbr.main;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;


@SpringBootApplication
@ComponentScan("edu.nus.cbr")
public class WinecbrApplication {

    public static void main(String[] args) {
        SpringApplication.run(WinecbrApplication.class, args);
    }
}