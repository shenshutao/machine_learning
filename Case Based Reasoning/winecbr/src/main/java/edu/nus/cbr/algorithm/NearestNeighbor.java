package edu.nus.cbr.algorithm;

import edu.nus.cbr.algorithm.impl.SimilarCase;
import edu.nus.cbr.algorithm.impl.Weights;
import edu.nus.cbr.data.Case;

import java.util.List;

/**
 * Created by Shutao on 27/6/2017.
 */
public interface NearestNeighbor {

    public List<SimilarCase> retrieveSimilarCases(Case target, Weights weights, int number) throws Exception;
}
