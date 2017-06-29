//package edu.nus.cbr.db;
//
//import org.springframework.data.domain.Page;
//import org.springframework.stereotype.Component;
//import org.springframework.transaction.annotation.Transactional;
//
//import java.util.List;
//
///**
// * Created by shutao on 29/6/17.
// */
//@Component("caseService")
//@Transactional
//public class CaseServiceImpl implements CaseService {
//    private final CaseRepository caseRepository;
//
//    public CaseServiceImpl(CaseRepository caseRepository) {
//        this.caseRepository = caseRepository;
//    }
//
//    @Override
//    public List<Case> findAll() {
//        return this.caseRepository.findAll();
//    }
//}
