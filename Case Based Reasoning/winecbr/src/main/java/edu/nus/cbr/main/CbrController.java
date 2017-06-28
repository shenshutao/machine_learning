package edu.nus.cbr.main;

import java.util.List;
import java.util.Map;

import edu.nus.cbr.algorithm.NearestNeighbor;
import edu.nus.cbr.algorithm.impl.NearestNeighborImpl;
import edu.nus.cbr.cases.CaseRepresentation;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class CbrController {

	@RequestMapping("/")
	public String index(Map<String, Object> model) {
		return "index";
	}

	@RequestMapping("/retrievecase")
	public String retrieveCase(@RequestParam("ingredients") String ingredients, @RequestParam("sugar") String sugar, @RequestParam("number") int number,  Map<String, Object> model) {
        CaseRepresentation newCase = new CaseRepresentation();

        NearestNeighbor nearestNeighbor = new NearestNeighborImpl();
        List<CaseRepresentation> similarCases = nearestNeighbor.retrieveSimilarCases(newCase, number);


		return "welcome";
	}
}