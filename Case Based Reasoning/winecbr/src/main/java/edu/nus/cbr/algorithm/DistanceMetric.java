package edu.nus.cbr.algorithm;

import edu.nus.cbr.algorithm.impl.Weights;
import edu.nus.cbr.data.Case;

/**
 * Created by shutao on 29/6/17.
 */
public interface DistanceMetric {
    public double calSimilarity(Case case1, Case case2, Weights weights);
}
