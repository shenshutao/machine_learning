package edu.nus.cbr.main;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;


@SpringBootApplication
@ComponentScan("edu.nus.cbr")
//@EntityScan(basePackageClasses=Case.class)
//@EnableJpaRepositories(basePackages = {
//        "edu.nus.cbr.db"
//})
public class WinecbrApplication {

    public static void main(String[] args) {
        SpringApplication.run(WinecbrApplication.class, args);
    }
}