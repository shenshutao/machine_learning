package edu.nus.cbr.cases.attributetypes;

/**
 * Created by shutao on 29/6/17.
 */
public enum AlcoholAttr {
    HIGH(1),
    LOW(0.5),
    NONE(0);

    private double num;

    AlcoholAttr(double s) {
        this.num = s;
    }

    public double getNum() {
        return this.num;
    }

    public static AlcoholAttr permissiveValueOf(String name) {
        for (AlcoholAttr e : values()) {
            if (e.name().equalsIgnoreCase(name)) {
                return e;
            }
        }
        if ("0".equals(name)) {
            return AlcoholAttr.NONE;
        }
        return null;
    }
}
