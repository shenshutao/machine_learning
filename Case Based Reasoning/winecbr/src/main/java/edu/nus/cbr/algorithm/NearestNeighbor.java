package edu.nus.cbr.algorithm;

import edu.nus.cbr.cases.CaseRepresentation;

import java.util.List;

/**
 * Created by Shutao on 27/6/2017.
 */
public interface NearestNeighbor {

    public List<CaseRepresentation> retrieveSimilarCases(CaseRepresentation target, int number);
}
