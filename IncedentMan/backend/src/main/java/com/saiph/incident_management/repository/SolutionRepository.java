package com.saiph.incident_management.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.saiph.incident_management.model.Solution;

@Repository
public interface SolutionRepository extends MongoRepository<Solution, String> {
    Solution findByIncidentId(String incidentId);
    List<Solution> findByCreatorId(String creatorId);
    List<Solution> findAll();
}