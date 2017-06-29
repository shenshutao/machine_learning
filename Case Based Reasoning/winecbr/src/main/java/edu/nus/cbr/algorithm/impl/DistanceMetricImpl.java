package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.algorithm.DistanceMetric;
import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.TureOrFalseAttr;
import edu.nus.cbr.data.Case;
import org.springframework.stereotype.Component;
import org.thymeleaf.util.StringUtils;

import java.util.Arrays;
import java.util.List;

/**
 * Created by shutao on 29/6/17.
 */
@Component("distanceMetric")
public class DistanceMetricImpl implements DistanceMetric {

    private static final String DEFAULT_INGREDIENTS_SEPARATOR = ";";

    @Override
    public double calDistance(Case caseInLib, Case newCase) {
        double distanceIngredients = calIngredientsDistance(caseInLib.getIngredients(), newCase.getIngredients());
        double distanceSugar = calTrueOrFalseDistance(caseInLib.getSugar(), newCase.getSugar());
        double distanceAlcohol = calAlcoholDistance(caseInLib.getAlochol(), newCase.getAlochol());

        double result = Math.sqrt(Math.pow(2, distanceIngredients) + Math.pow(2, distanceSugar) + Math.pow(2, distanceAlcohol));

        return result;
    }

    private double calAlcoholDistance(AlcoholAttr target, AlcoholAttr newCase) {
        if (target == null || newCase == null) {
            return 1;
        }

        return Math.abs(target.getNum() - newCase.getNum());
    }

    private double calIngredientsDistance(String targetIngredients, String newCaseIngredients) {
        if (StringUtils.isEmptyOrWhitespace(targetIngredients) || StringUtils.isEmptyOrWhitespace(newCaseIngredients)) {
            return 1;
        }

        List<String> newCaseIngredientsList = Arrays.asList(newCaseIngredients.toUpperCase().split(DEFAULT_INGREDIENTS_SEPARATOR));
        List<String> targetIngredientsList = Arrays.asList(targetIngredients.toUpperCase().split(DEFAULT_INGREDIENTS_SEPARATOR));

        double n = 0;
        for (String s : targetIngredientsList) {
            if (newCaseIngredientsList.contains(s)) {
                n++;
            }
        }
        return 1 - n / targetIngredientsList.size();
    }

    private double calTrueOrFalseDistance(TureOrFalseAttr target, TureOrFalseAttr newCase) {
        if (target == null || newCase == null) {
            return 1;
        }

        if (target.equals(newCase)) {
            return 0;
        } else {
            return 1;
        }
    }

//    public static void main(String args[]) {
//        DistanceMetricImpl dm = new DistanceMetricImpl();
//        System.out.println(dm.calIngredientsDistance("a;b;c", "A;b;c"));
//    }
}
