package edu.nus.cbr.cases;

/**
 * Created by Shutao on 27/6/2017.
 */
public class Attribute {
    AttrType type;
    String value;

    public Attribute() {
    }

    public Attribute(AttrType type, String value) {
        this.type = type;
        this.value = value;
    }

    public AttrType getType() {
        return type;
    }

    public void setType(AttrType type) {
        this.type = type;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return "Attribute{" +
                "type=" + type +
                ", value='" + value + '\'' +
                '}';
    }
}
