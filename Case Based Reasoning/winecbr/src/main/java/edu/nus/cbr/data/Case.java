package edu.nus.cbr.data;

import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.FlavourAttr;
import edu.nus.cbr.cases.attributetypes.NoOfIngredientsAttr;
import edu.nus.cbr.cases.attributetypes.TureOrFalseAttr;
import lombok.Getter;
import lombok.Setter;

import java.io.Serializable;

/**
 * Created by shutao on 29/6/17.
 */
@Setter
@Getter
public class Case implements Serializable {
    private static final long serialVersionUID = 1L;

    private String receiptId;
    private String drinkName;
    private String ingredients;
    private TureOrFalseAttr sugar;
    private AlcoholAttr alcohol;
    private Double numOfLiquid;
    private NoOfIngredientsAttr numOfIngredients;
    private TureOrFalseAttr fruit;
    private TureOrFalseAttr juice;
    private FlavourAttr flavour;
    private String description;
}
