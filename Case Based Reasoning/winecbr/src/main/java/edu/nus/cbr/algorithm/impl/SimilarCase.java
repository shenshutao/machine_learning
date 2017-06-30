package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.data.Case;
import lombok.Getter;
import lombok.Setter;

/**
 * Created by shutao on 30/6/17.
 */
@Setter
@Getter
public class SimilarCase {
    private double distance;
    private Case similarCase;

    public SimilarCase(double distance, Case similarCase) {
        this.distance = distance;
        this.similarCase = similarCase;
    }
}
