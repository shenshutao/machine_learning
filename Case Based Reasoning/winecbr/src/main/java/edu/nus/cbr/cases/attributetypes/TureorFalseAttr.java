package edu.nus.cbr.cases.attributetypes;

/**
 * Created by shutao on 29/6/17.
 */
public enum TureOrFalseAttr {
    TRUE(1),
    FALSE(0);

    private int num;

    TureOrFalseAttr(int i) {
        this.num = i;
    }

    public int getNum() {
        return this.num;
    }

    public static TureOrFalseAttr permissiveValueOf(String name) {
        for (TureOrFalseAttr e : values()) {
            if (e.name().equalsIgnoreCase(name)) {
                return e;
            }
        }

        return null;
    }
}
