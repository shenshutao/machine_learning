package edu.nus.cbr.data;

import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.FlaverAttr;
import edu.nus.cbr.cases.attributetypes.TureOrFalseAttr;

import java.io.Serializable;

/**
 * Created by shutao on 29/6/17.
 */
public class Case implements Serializable {

    private static final long serialVersionUID = 1L;

    private String receiptId;
    private String drinkName;
    private String ingredients;
    private TureOrFalseAttr sugar;
    private AlcoholAttr alochol;
    private int numOfLiquid;
    private int numOfIngredients;
    private TureOrFalseAttr fruit;
    private TureOrFalseAttr juice;
    private FlaverAttr flaver;
    private String description;

    public String getReceiptId() {
        return receiptId;
    }

    public void setReceiptId(String receiptId) {
        this.receiptId = receiptId;
    }

    public String getDrinkName() {
        return drinkName;
    }

    public void setDrinkName(String drinkName) {
        this.drinkName = drinkName;
    }

    public int getNumOfLiquid() {
        return numOfLiquid;
    }

    public void setNumOfLiquid(int numOfLiquid) {
        this.numOfLiquid = numOfLiquid;
    }

    public int getNumOfIngredients() {
        return numOfIngredients;
    }

    public void setNumOfIngredients(int numOfIngredients) {
        this.numOfIngredients = numOfIngredients;
    }

    public TureOrFalseAttr getFruit() {
        return fruit;
    }

    public void setFruit(TureOrFalseAttr fruit) {
        this.fruit = fruit;
    }

    public TureOrFalseAttr getJuice() {
        return juice;
    }

    public void setJuice(TureOrFalseAttr juice) {
        this.juice = juice;
    }

    public FlaverAttr getFlaver() {
        return flaver;
    }

    public void setFlaver(FlaverAttr flaver) {
        this.flaver = flaver;
    }

    public String getIngredients() {
        return ingredients;
    }

    public void setIngredients(String ingredients) {
        this.ingredients = ingredients;
    }

    public TureOrFalseAttr getSugar() {
        return sugar;
    }

    public void setSugar(TureOrFalseAttr sugar) {
        this.sugar = sugar;
    }

    public AlcoholAttr getAlochol() {
        return alochol;
    }

    public void setAlochol(AlcoholAttr alochol) {
        this.alochol = alochol;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}
