package edu.nus.cbr.cases.attributetypes;

/**
 * Created by shutao on 29/6/17.
 */
public enum FlavourAttr {
    SWEET,
    MINTY,
    SOUR,
    SALTY,
    SPICY;

    public static FlavourAttr permissiveValueOf(String name) {
        for (FlavourAttr e : values()) {
            if (e.name().equalsIgnoreCase(name)) {
                return e;
            }
        }

        return null;
    }
}
