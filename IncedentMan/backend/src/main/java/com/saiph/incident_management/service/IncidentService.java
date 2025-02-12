package com.saiph.incident_management.service;

import com.saiph.incident_management.model.Incident;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.model.User;
import com.saiph.incident_management.repository.IncidentRepository;
import com.saiph.incident_management.repository.UserRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class IncidentService {
    
    @Autowired
    private IncidentRepository incidentRepository;
    @Autowired
    private UserRepository userRepository;
    
    public List<Incident> getAllIncidents() {
        List<Incident> incidents = incidentRepository.findAll();
        for (Incident incident : incidents) {
            loadUserData(incident);
        }
        return incidents;
    }
    
    public Optional<Incident> getIncidentById(String id) {
        Optional<Incident> incidentOpt = incidentRepository.findById(id);
        if (incidentOpt.isPresent()) {
            Incident incident = incidentOpt.get();
            loadUserData(incident);
        }
        return incidentOpt;
    }
    
    public Incident createIncident(Incident incident) {
        
        loadUserData(incident);
        return incidentRepository.save(incident);
    }
    
    public Incident updateIncident(String id, Incident incident) {
        if (incidentRepository.existsById(id)) {
            incident.setId(id);
            loadUserData(incident);
            return incidentRepository.save(incident);
        }
        return null;
    }
    
    public void deleteIncident(String id) {
        incidentRepository.deleteById(id);
    }
    
    public List<Incident> findByStatus(String status) {
        return incidentRepository.findByStatus(status);
    }
    
    public List<Incident> findByPriority(int priority) {
        return incidentRepository.findByPriority(priority);
    }
    
    public List<Incident> findByCategory(String category) {
        return incidentRepository.findByCategory(category);
    }
    
    public List<Incident> findByTechnician(String technicianId) {
        return incidentRepository.findByAssignedTechnicianId(technicianId);
    }
    
    public List<Incident> findByReporter(String reporterId) {
        return incidentRepository.findByReporterId(reporterId);
    }
    private void loadUserData(Incident incident) {
        
        if (incident.getReporter() != null && incident.getReporter().getId() != null) {
            Optional<User> reporter = userRepository.findById(incident.getReporter().getId());
            reporter.ifPresent(incident::setReporter);
        }
        
        
        if (incident.getAssignedTechnician() != null && incident.getAssignedTechnician().getId() != null) {
            Optional<User> technician = userRepository.findById(incident.getAssignedTechnician().getId());
            if (technician.isPresent() && technician.get() instanceof Technician) {
                incident.setAssignedTechnician((Technician) technician.get());
            }
        }
    }
}
