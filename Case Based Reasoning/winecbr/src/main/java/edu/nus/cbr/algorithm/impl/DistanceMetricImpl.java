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
    public double calSimilarity(Case caseInLib, Case newCase, Weights weights) {
        double distanceIngredients = calIngredientsDistance(caseInLib.getIngredients(), newCase.getIngredients());
        double distanceSugar = calTrueOrFalseDistance(caseInLib.getSugar(), newCase.getSugar());
        double distanceAlcohol = calCustomDistance(caseInLib.getAlcohol(), newCase.getAlcohol());
        double distanceFruit = calTrueOrFalseDistance(caseInLib.getFruit(), newCase.getFruit());
        double distanceJuice = calTrueOrFalseDistance(caseInLib.getJuice(), newCase.getJuice());
        double distanceFlavour = calFlavourDistance(caseInLib.getFlavour(), newCase.getFlavour());
        double distanceNoOfIngredients = calCustomDistance(caseInLib.getNoOfIngredients(), newCase.getNoOfIngredients());
        double distanceNoOfLiquid = calNormalDistance(caseInLib.getNoOfLiquid(), newCase.getNoOfLiquid());

        double similarityIngredients = 1 - Math.abs(distanceIngredients);
        double similaritySugar = 1 - Math.abs(distanceSugar);
        double similarityAlcohol = 1 - Math.abs(distanceAlcohol);
        double similarityFruit = 1 - Math.abs(distanceFruit);
        double similarityJuice = 1 - Math.abs(distanceJuice);
        double similarityFlavour = 1 - Math.abs(distanceFlavour);
        double similarityNoOfIngredients = 1 - Math.abs(distanceNoOfIngredients);
        double similarityNoOfLiquid = 1 - Math.abs(distanceNoOfLiquid);

        double result =
                similarityIngredients * weights.getWeightIngredients()
                        + similaritySugar * weights.getWeightSugar()
                        + similarityAlcohol * weights.getWeightAlcohol()
                        + similarityFruit * weights.getWeightFruit()
                        + similarityJuice * weights.getWeightJuice()
                        + similarityFlavour * weights.getWeightFlavour()
                        + similarityNoOfIngredients * weights.getWeightNoOfIngredients()
                        + similarityNoOfLiquid * weights.getWeightNoOfLiquid();

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
