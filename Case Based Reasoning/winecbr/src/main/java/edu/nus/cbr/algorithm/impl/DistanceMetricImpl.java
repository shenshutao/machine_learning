package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.algorithm.DistanceMetric;
import edu.nus.cbr.cases.attributetypes.BasicAttr;
import edu.nus.cbr.cases.attributetypes.FlavourAttr;
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
    public double calDistance(Case caseInLib, Case newCase, Weights weights) {
        double distanceIngredients = calIngredientsDistance(caseInLib.getIngredients(), newCase.getIngredients());
        double distanceSugar = calTrueOrFalseDistance(caseInLib.getSugar(), newCase.getSugar());
        double distanceAlcohol = calCustomDistance(caseInLib.getAlcohol(), newCase.getAlcohol());
        double distanceFruit = calTrueOrFalseDistance(caseInLib.getFruit(), newCase.getFruit());
        double distanceJuice = calTrueOrFalseDistance(caseInLib.getJuice(), newCase.getJuice());
        double distanceFlavour = calFlavourDistance(caseInLib.getFlavour(), newCase.getFlavour());
        double distanceNoOfIngredients = calCustomDistance(caseInLib.getNumOfIngredients(), newCase.getNumOfIngredients());
        double distanceNoOfLiquid = calNormalDistance(caseInLib.getNumOfLiquid(), newCase.getNumOfLiquid());

        double result = Math.sqrt(Math.pow(2, distanceIngredients) * weights.getWeightIngredients()
                + Math.pow(2, distanceSugar) * weights.getWeightSugar()
                + Math.pow(2, distanceAlcohol) * weights.getWeightAlcohol()
                + Math.pow(2, distanceFruit) * weights.getWeightFruit()
                + Math.pow(2, distanceJuice) * weights.getWeightJuice()
                + Math.pow(2, distanceFlavour) * weights.getWeightFlavour()
                + Math.pow(2, distanceNoOfIngredients) * weights.getWeightNoOfIngredients()
                + Math.pow(2, distanceNoOfLiquid) * weights.getWeightNoOfLiquid());

        return result;
    }

    private double calCustomDistance(BasicAttr target, BasicAttr newCase) {
        if (target == null || newCase == null) {
            return 1;
        }

        return Math.abs(target.getNum() - newCase.getNum());
    }

    private double calFlavourDistance(FlavourAttr target, FlavourAttr newCase) {
        if (target == null || newCase == null) {
            return 1;
        }

        if (target.equals(newCase)) {
            return 0;
        } else {
            return 1;
        }
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

    private double calNormalDistance(Double target, Double newCase) {
        if (target == null || newCase == null) {
            return 1;
        }

        return Math.abs(target - newCase);
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
