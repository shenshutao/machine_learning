package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.algorithm.DistanceMetric;
import edu.nus.cbr.cases.AttrType;
import edu.nus.cbr.cases.Attribute;
import edu.nus.cbr.cases.CaseRepresentation;

/**
 * Created by shutao on 29/6/17.
 */
public class EuclideanMetric implements DistanceMetric{
    @Override
    public double calDistance(CaseRepresentation case1, CaseRepresentation case2) {

        double sum = 0;
        for(String attributeName : case1.getAttributeMap().keySet()) {
            Attribute attribute1 = case1.getAttributeMap().get(attributeName);
            Attribute attribute2 = case2.getAttributeMap().get(attributeName);

            if (attribute1 != null && attribute2 != null) {
                if (AttrType.NUMBER.equals(attribute1.getType())) {
                    double v1 = Double.valueOf(attribute1.getValue());
                    double v2 = Double.valueOf(attribute2.getValue());

                    sum += (v1 - v2) * (v1 - v2);
                }
            }
        }
        double result = Math.sqrt(sum);

        return result;
    }

    public static void main(String args[]) {
        CaseRepresentation case1 = new CaseRepresentation();
        CaseRepresentation case2 = new CaseRepresentation();
        case1.addAttribute("key", new Attribute(AttrType.NUMBER, "4"));
        case2.addAttribute("key", new Attribute(AttrType.NUMBER, "8"));

        EuclideanMetric em = new EuclideanMetric();
        System.out.println(em.calDistance(case1, case2));
    }
}
