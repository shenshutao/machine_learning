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
                               @RequestParam("noofliquid") Double noofliquid,
                               @RequestParam("noofingred") NoOfIngredientsAttr noofingred,
                               @RequestParam("weightIngredients") Double weightIngredients,
                               @RequestParam("weightSugar") Double weightSugar,
                               @RequestParam("weightAlcohol") Double weightAlcohol,
                               @RequestParam("weightFruit") Double weightFruit,
                               @RequestParam("weightJuice") Double weightJuice,
                               @RequestParam("weightFlavour") Double weightFlavour,
                               @RequestParam("weightNoOfIngredients") Double weightNoOfIngredients,
                               @RequestParam("weightNoOfLiquid") Double weightNoOfLiquid,
                               @RequestParam("number") int number,
                               Map<String, Object> model) throws Exception {
        Case newCase = new Case();
        newCase.setAlcohol(alcohol);
        newCase.setSugar(sugar);
        newCase.setIngredients(ingredients);
        newCase.setFruit(fruit);
        newCase.setJuice(juice);
        newCase.setFlavour(flavour);
        newCase.setNoOfLiquid(noofliquid);
        newCase.setNoOfIngredients(noofingred);

        Weights weights = new Weights();
        weights.setWeightIngredients(weightIngredients);
        weights.setWeightSugar(weightSugar);
        weights.setWeightAlcohol(weightAlcohol);
        weights.setWeightFruit(weightFruit);
        weights.setWeightJuice(weightJuice);
        weights.setWeightFlavour(weightFlavour);
        weights.setWeightNoOfIngredients(weightNoOfIngredients);
        weights.setWeightNoOfLiquid(weightNoOfLiquid);

        List<SimilarCase> cases = nearestNeighbor.retrieveSimilarCases(newCase, weights, number);

        newCase.setNoOfLiquid(noofliquid);
        newCase.setNoOfIngredients(noofingred);
        model.put("newCase", newCase);
        model.put("similarCaseList", cases);

        return "results";
    }
}