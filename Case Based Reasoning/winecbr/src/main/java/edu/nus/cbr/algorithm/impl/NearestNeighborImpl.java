package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.algorithm.NearestNeighbor;
import edu.nus.cbr.cases.AttrType;
import edu.nus.cbr.cases.Attribute;
import edu.nus.cbr.cases.CaseRepresentation;

import java.math.BigDecimal;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by Shutao on 27/6/2017.
 */
public class NearestNeighborImpl implements NearestNeighbor {
    @Override
    public List<CaseRepresentation> retrieveSimilarCases(CaseRepresentation target) {

        //

        return null;
    }

    private static double calCaseDistance(CaseRepresentation case1, CaseRepresentation case2) {
        double sum = 0;
        for(String attributeName : case1.getAttributeMap().keySet()) {
            Attribute attribute1 = case1.getAttributeMap().get(attributeName);
            Attribute attribute2 = case2.getAttributeMap().get(attributeName);

            if(attribute1 != null && attribute2 != null) {
                if (AttrType.NUMBER.equals(attribute1.getType())) {
                    double v1 = Double.valueOf(attribute1.getValue());
                    double v2 = Double.valueOf(attribute2.getValue());

                    sum += (v1 - v2) * (v1 - v2);
                }
//                else
//                    if (AttrType.NOMINAL.equals(attribute1.getType())) {
//                    if(attribute1.getValue().equals(attribute2.getValue())) {
//                        sum += 1;
//                    } else {
//                        sum += 0;
//                    }
//                }
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
        System.out.println(calCaseDistance(case1, case2));
    }
}
