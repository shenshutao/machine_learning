package edu.nus.cbr.algorithm;

import edu.nus.cbr.cases.CaseRepresentation;

/**
 * Created by shutao on 29/6/17.
 */
public interface DistanceMetric {
    public double calDistance(CaseRepresentation case1, CaseRepresentation case2);
}
