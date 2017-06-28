package edu.nus.cbr.main;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

/**
 * Created by Shutao on 27/6/2017.
 */
@Controller
public class CbrController2 {

    @RequestMapping("/hello2")
    public ModelAndView hello2() {
        ModelAndView modelAndView = new ModelAndView("/index");
        modelAndView.addObject("message", "Shutao");
        return modelAndView;
    }
}
