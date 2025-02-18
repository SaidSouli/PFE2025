package com.saiph.incident_management.repository;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import com.saiph.incident_management.model.Technician;

@Repository
public interface TechnicianRepository extends MongoRepository<Technician,String> {
        Technician findByUsername (String username);
}

