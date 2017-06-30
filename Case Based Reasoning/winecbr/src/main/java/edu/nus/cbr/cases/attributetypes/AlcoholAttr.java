package edu.nus.cbr.cases.attributetypes;

/**
 * Created by shutao on 29/6/17.
 */
public enum AlcoholAttr implements BasicAttr {
    HIGH(1),
    LOW(0.5),
    NONE(0);

    private Double num;

    AlcoholAttr(double s) {
        this.num = s;
    }

    public Double getNum() {
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
