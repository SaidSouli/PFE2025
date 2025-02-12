package com.saiph.incident_management.repository;

import com.saiph.incident_management.model.Incident;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface IncidentRepository extends MongoRepository<Incident, String> {
    List<Incident> findByStatus(String status);
    List<Incident> findByPriority(int priority);
    List<Incident> findByCategory(String category);
    List<Incident> findByAssignedTechnicianId(String technicianId);
    List<Incident> findByReporterId(String reporterId);
}