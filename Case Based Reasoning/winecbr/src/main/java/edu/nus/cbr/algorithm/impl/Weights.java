package edu.nus.cbr.algorithm.impl;

import lombok.Getter;
import lombok.Setter;

/**
 * Created by Shutao on 30/6/2017.
 */
@Setter
@Getter
public class Weights {
    double weightIngredients = 0.4;
    double weightSugar = 0.1;
    double weightAlcohol = 0.1;
    double weightFruit = 0.1;
    double weightJuice = 0.05;
    double weightFlavour = 0.1;
    double weightNoOfIngredients = 0.1;
    double weightNoOfLiquid = 0.05;
}
