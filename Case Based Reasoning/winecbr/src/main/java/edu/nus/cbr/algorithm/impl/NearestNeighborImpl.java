package edu.nus.cbr.algorithm.impl;

import edu.nus.cbr.algorithm.DistanceMetric;
import edu.nus.cbr.algorithm.NearestNeighbor;
import edu.nus.cbr.cases.attributetypes.AlcoholAttr;
import edu.nus.cbr.cases.attributetypes.FlavourAttr;
import edu.nus.cbr.cases.attributetypes.NoOfIngredientsAttr;
import edu.nus.cbr.cases.attributetypes.TureOrFalseAttr;
import edu.nus.cbr.data.Case;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

/**
 * Created by Shutao on 27/6/2017.
 */
@Component("nearestNeighbor")
public class NearestNeighborImpl implements NearestNeighbor {
    private static final char DEFAULT_QUOTE = '\"';
    private static final char DEFAULT_SEPARATOR = ',';


    @Value("${case.library.file}")
    private String csvFile = "cocktailcasebase.csv";

    @Autowired
    DistanceMetric distanceMetric;

    @Override
    public List<SimilarCase> retrieveSimilarCases(Case target, Weights weights, int number) throws Exception {

        SimilarCase[] similarCasesList = new SimilarCase[number];
        List<Case> caseInLibList = readCasesFromCSVFile();

        /*
         * 1.Normalization No of Liquid. Other fields already normalized
         * Simple way, min 0, max 5
         */
        for (Case c1 : caseInLibList) {
            double afterNorm = (c1.getNumOfLiquid() - 0) / (5 - 0);
            c1.setNumOfLiquid(afterNorm);
        }

        /*
         * 2.Calculate distance.
         */
        for (Case c : caseInLibList) {
            double distance = distanceMetric.calDistance(c, target, weights);
            if (similarCasesList[0] == null) {
                similarCasesList[0] = new SimilarCase(distance, c);
            } else {
                for (int i = number - 1; i >= 0; i--) {
                    if (similarCasesList[i] == null) {
                        continue;
                    }
                    if (distance > similarCasesList[i].getDistance()) {
                        if (i < number - 1) {
                            for (int n = number - 1; n > i + 1; n--) {
                                similarCasesList[n] = similarCasesList[n - 1];
                            }
                            similarCasesList[i + 1] = new SimilarCase(distance, c);
                        }
                        break;
                    } else if (i == 0) {
                        for (int n = number - 1; n > i; n--) {
                            similarCasesList[n] = similarCasesList[n - 1];
                        }
                        similarCasesList[i] = new SimilarCase(distance, c);
                    }
                }
            }
        }

        return Arrays.asList(similarCasesList);
    }

    public List<Case> readCasesFromCSVFile() throws Exception {
        Scanner scanner = new Scanner(new File(csvFile));
        scanner.nextLine();

        List<Case> caseList = new ArrayList<>();
        while (scanner.hasNext()) {
            String line = scanner.nextLine();
            List<String> split = parseLine(line);
            System.out.println(" 0" + split.get(0) + " 1" + split.get(1) + " 2" + split.get(2) + " 3" + split.get(3) + " 4" + split.get(4) + " 5" + split.get(5) + " 6" + split.get(6) + " 7" + split.get(7) + " 8" + split.get(8) + " 9" + split.get(9) + " 10" + split.get(10));

            Case c = new Case();
            c.setReceiptId(split.get(0));
            c.setDrinkName(split.get(1));
            c.setIngredients(split.get(2));
            c.setSugar(TureOrFalseAttr.permissiveValueOf(split.get(3)));
            c.setAlcohol(AlcoholAttr.permissiveValueOf(split.get(4)));
            c.setNumOfLiquid(Double.valueOf(split.get(5)));
            c.setNumOfIngredients(NoOfIngredientsAttr.permissiveValueOf(Integer.valueOf(split.get(6))));
            c.setFruit(TureOrFalseAttr.permissiveValueOf(split.get(7)));
            c.setJuice(TureOrFalseAttr.permissiveValueOf(split.get(8)));
            c.setFlavour(FlavourAttr.permissiveValueOf(split.get(9)));

            c.setDescription(split.get(10));

            caseList.add(c);
        }
        scanner.close();

        return caseList;
    }

//    public static void main(String[] args) {
//        try {
//            NearestNeighborImpl nearestNeighbor = new NearestNeighborImpl();
//            nearestNeighbor.retrieveSimilarCases(new Case(), 4);
//        } catch (Exception e) {
//            e.printStackTrace();
//        }
//    }


    public static List<String> parseLine(String cvsLine) {

        List<String> result = new ArrayList<>();

        //if empty, return!
        if (cvsLine == null && cvsLine.isEmpty()) {
            return result;
        }

        char customQuote = DEFAULT_QUOTE;
        char separators = DEFAULT_SEPARATOR;

        StringBuffer curVal = new StringBuffer();
        boolean inQuotes = false;
        boolean startCollectChar = false;
        boolean doubleQuotesInColumn = false;

        char[] chars = cvsLine.toCharArray();

        for (char ch : chars) {

            if (inQuotes) {
                startCollectChar = true;
                if (ch == customQuote) {
                    inQuotes = false;
                    doubleQuotesInColumn = false;
                } else {

                    //Fixed : allow "" in custom quote enclosed
                    if (ch == '\"') {
                        if (!doubleQuotesInColumn) {
                            curVal.append(ch);
                            doubleQuotesInColumn = true;
                        }
                    } else {
                        curVal.append(ch);
                    }

                }
            } else {
                if (ch == customQuote) {

                    inQuotes = true;

                    //Fixed : allow "" in empty quote enclosed
                    if (chars[0] != '"' && customQuote == '\"') {
                        curVal.append('"');
                    }

                    //double quotes in column will hit this!
                    if (startCollectChar) {
                        curVal.append('"');
                    }

                } else if (ch == separators) {

                    result.add(curVal.toString());

                    curVal = new StringBuffer();
                    startCollectChar = false;

                } else if (ch == '\r') {
                    //ignore LF characters
                    continue;
                } else if (ch == '\n') {
                    //the end, break!
                    break;
                } else {
                    curVal.append(ch);
                }
            }

        }

        result.add(curVal.toString());

        return result;
    }

}
