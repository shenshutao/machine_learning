package edu.nus.cbr.algorithm;

import edu.nus.cbr.data.Case;

/**
 * Created by shutao on 29/6/17.
 */
public interface DistanceMetric {
    public double calDistance(Case case1, Case case2);
}