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
    private double similarity;
    private Case caseObj;

    public SimilarCase(double similarity, Case similarCase) {
        this.similarity = similarity;
        this.caseObj = similarCase;

    }
}
