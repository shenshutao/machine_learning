package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.data.Case;

/**
 * Created by shutao on 30/6/17.
 */
public class SimilarCase {
    private double distance;
    private Case similarCase;

    public SimilarCase(double distance, Case similarCase) {
        this.distance = distance;
        this.similarCase = similarCase;
    }

    public double getDistance() {
        return distance;
    }

    public void setDistance(double distance) {
        this.distance = distance;
    }

    public Case getSimilarCase() {
        return similarCase;
    }

    public void setSimilarCase(Case similarCase) {
        this.similarCase = similarCase;
    }
}
