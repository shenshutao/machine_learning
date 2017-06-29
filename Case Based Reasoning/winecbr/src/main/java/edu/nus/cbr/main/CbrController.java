package edu.nus.cbr.main;

import edu.nus.cbr.algorithm.impl.NearestNeighborImpl;
import edu.nus.cbr.algorithm.impl.SimilarCase;
import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.TureOrFalseAttr;
import edu.nus.cbr.data.Case;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Map;

@Controller
public class CbrController {

    //    @Autowired
//    private CaseService caseService;
    @Autowired
    NearestNeighborImpl nearestNeighbor;

    @RequestMapping("/")
    public String index(Map<String, Object> model) {
        return "index";
    }

    @RequestMapping("/retrievecase")
    public String retrieveCase(@RequestParam("ingredients") String ingredients, @RequestParam("sugar") TureOrFalseAttr sugar, @RequestParam("alcohol") AlcoholAttr alcohol, @RequestParam("number") int number, Map<String, Object> model) throws Exception {
        Case newCase = new Case();
        newCase.setAlochol(alcohol);
        newCase.setSugar(sugar);
        newCase.setIngredients(ingredients);

        List<SimilarCase> cases = nearestNeighbor.retrieveSimilarCases(newCase, number);

        model.put("similarCaseList", cases);

        for(SimilarCase sc : cases) {
            System.out.println(sc.getSimilarCase().toString());
        }

        return "results";
    }

//    @RequestMapping("/retrievecase")
//    @ResponseBody
//    @Transactional(readOnly = true)
//    public String retrieveCase(@RequestParam("ingredients") String ingredients, @RequestParam("sugar") TureOrFalseAttr sugar, @RequestParam("alcohol") AlcoholAttr alcohol, @RequestParam("number") int number, Map<String, Object> model) {
//        CaseRepresentation newCase = new CaseRepresentation();
////        newCase.addAttribute();
//
//
//        NearestNeighbor nearestNeighbor = new NearestNeighborImpl();
//        List<CaseRepresentation> similarCases = nearestNeighbor.retrieveSimilarCases(newCase, number);
//
//
//        this.caseService.findAll();
//
//        return "welcome";
//    }
}