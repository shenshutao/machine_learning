package edu.nus.cbr.cases.attributetypes;

/**
 * Created by shutao on 29/6/17.
 */
public enum FlaverAttr {
    SWEET(1),
    SOUR(0.5),
    SPICY(0);

    private double num;

    FlaverAttr(double i) {
        this.num = i;
    }

    public double getNum() {
        return this.num;
    }

    public static FlaverAttr permissiveValueOf(String name) {
        for (FlaverAttr e : values()) {
            if (e.name().equalsIgnoreCase(name)) {
                return e;
            }
        }

        return null;
    }
}
