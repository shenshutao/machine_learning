package edu.nus.cbr.main;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.ModelAndView;

import java.util.Map;

/**
 * Created by Shutao on 27/6/2017.
 */
@RestController
public class CbrController {

    @RequestMapping("/hello")
    public String home() {
        return "HelloWorld";
    }
}
