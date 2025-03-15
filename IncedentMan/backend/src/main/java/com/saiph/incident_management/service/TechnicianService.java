package com.saiph.incident_management.service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.data.mongodb.core.FindAndModifyOptions;

import java.util.List;
import java.util.Optional;

import org.bson.types.ObjectId;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.saiph.incident_management.model.Incident;
import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.repository.IncidentRepository;
import com.saiph.incident_management.repository.TechnicianRepository;

@Service
public class TechnicianService {

    @Autowired
    private TechnicianRepository technicianRepository;
    @Autowired
    private IncidentRepository incidentRepository;

    @Autowired
    private MongoTemplate mongoTemplate;

    public List<Specialization> getSpecializationsByUsername(String username) {
        Technician technician = technicianRepository.findByUsername(username);
        if (technician == null) {
            throw new RuntimeException("Technician not found with username: " + username);
        }
        return technician.getSpecializations();
    }

    @Transactional
    public Technician updateAssignedIncidentStatus(String technicianId, String incidentId, String status) {
        Query query = new Query(Criteria.where("_id").is(technicianId)
                .and("assignedIncidents._id").is(new ObjectId(incidentId)));
        
        Update update = new Update().set("assignedIncidents.$.status", status);
        
        Technician updatedTechnician = mongoTemplate.findAndModify(
                query, update, FindAndModifyOptions.options().returnNew(true), Technician.class);

        if (updatedTechnician == null) {
            throw new RuntimeException("Technician or Incident not found with given IDs.");
        }

        return updatedTechnician;
    }
    public Technician getAssignedTechnician(String incidentId) {
        // Find the incident by ID
        Optional<Incident> incidentOpt = incidentRepository.findById(incidentId);
        if (incidentOpt.isEmpty()) {
            return null;
        }
        
        // Find the technician assigned to this incident
        Optional<Technician> technicianOpt = technicianRepository.findByAssignedIncidents_Id(incidentId);
        if (technicianOpt.isEmpty()) {
            return null;
        }
        
        return technicianOpt.get();
    }
}
