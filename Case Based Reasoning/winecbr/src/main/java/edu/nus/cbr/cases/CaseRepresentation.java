package edu.nus.cbr.cases;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by Shutao on 27/6/2017.
 */
public class CaseRepresentation {
    private Map<String, Attribute> attributeMap = new HashMap<>();

    public Map<String, Attribute> getAttributeMap() {
        return attributeMap;
    }

//    public void setAttributeMap(Map<String, Attribute> attributeMap) {
//        this.attributeMap = attributeMap;
//    }

    public void addAttribute(String name, Attribute attribute) {
        attributeMap.put(name, attribute);
    }
}
