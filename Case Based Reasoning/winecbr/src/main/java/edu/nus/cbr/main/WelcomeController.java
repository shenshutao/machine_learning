package edu.nus.cbr.main;

import java.util.Map;

import edu.nus.cbr.cases.CaseRepresentation;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class WelcomeController {

	@RequestMapping("/")
	public String welcome(Map<String, Object> model) {
		return "welcome";
	}

	@RequestMapping("/retrievecase")
	public String retrievecase(@RequestParam("ingredients") String ingredients, @RequestParam("sugar") String sugar, Map<String, Object> model) {
        CaseRepresentation newCase = new CaseRepresentation();

		return "welcome";
	}
}