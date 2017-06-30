package edu.nus.cbr.main;

import edu.nus.cbr.algorithm.impl.NearestNeighborImpl;
import edu.nus.cbr.algorithm.impl.SimilarCase;
import edu.nus.cbr.algorithm.impl.Weights;
import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.FlavourAttr;
import edu.nus.cbr.cases.attributetypes.NoOfIngredientsAttr;
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
        Weights weights = new Weights();
        model.put("weights", weights);
        return "index";
    }

    @RequestMapping("/retrievecase")
    public String retrieveCase(@RequestParam("ingredients") String ingredients,
                               @RequestParam("sugar") TureOrFalseAttr sugar,
                               @RequestParam("alcohol") AlcoholAttr alcohol,
                               @RequestParam("fruit") TureOrFalseAttr fruit,
                               @RequestParam("juice") TureOrFalseAttr juice,
                               @RequestParam("flavour") FlavourAttr flavour,
                               @RequestParam(value = "noofliquid", required = false) Double noofliquid,
                               @RequestParam("noofingred") NoOfIngredientsAttr noofingred,
                               @RequestParam("number") int number,
                               Map<String, Object> model) throws Exception {
        Case newCase = new Case();
        newCase.setAlcohol(alcohol);
        newCase.setSugar(sugar);
        newCase.setIngredients(ingredients);
        newCase.setFruit(fruit);
        newCase.setJuice(juice);
        newCase.setFlavour(flavour);
        newCase.setNumOfLiquid(noofliquid);
        newCase.setNumOfIngredients(noofingred);

        Weights weights = new Weights();


        List<SimilarCase> cases = nearestNeighbor.retrieveSimilarCases(newCase, weights, number);

        model.put("similarCaseList", cases);

        for (SimilarCase sc : cases) {
            System.out.println(sc.getSimilarCase().toString());
        }

        return "results";
    }
}