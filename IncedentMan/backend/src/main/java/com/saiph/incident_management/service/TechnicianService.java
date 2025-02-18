package com.saiph.incident_management.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.repository.TechnicianRepository;

@Service
public class TechnicianService {

    @Autowired
    private TechnicianRepository technicianRepository;

    public List<Specialization> getSpecializationsByUsername(String username) {
        Technician technician = technicianRepository.findByUsername(username);

            return technician.getSpecializations();
    }

}