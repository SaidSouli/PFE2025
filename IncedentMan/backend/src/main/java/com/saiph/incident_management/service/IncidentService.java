package com.saiph.incident_management.service;

import com.saiph.incident_management.model.Incident;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.model.User;
import com.saiph.incident_management.repository.IncidentRepository;
import com.saiph.incident_management.repository.TechnicianRepository;
import com.saiph.incident_management.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class IncidentService {
    
    @Autowired
    private IncidentRepository incidentRepository;
    @Autowired
    private TechnicianRepository technicianRepository;
    @Autowired
    private UserRepository userRepository;
    @Value("${ai.service.url}")
    private String aiServiceUrl;
    
    @Autowired
    private RestTemplate restTemplate;
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
    //said did this 
    @SuppressWarnings({"unchecked" })
    public Incident createIncident(Incident incident) {
        try {
            
            if (incident.getCategory() == null || incident.getCategory().isEmpty() || incident.getPriority() == 0) {
                Map<String, String> request = new HashMap<>();
                request.put("description", incident.getDescription());
    
                ResponseEntity<Map> aiResponse = restTemplate.postForEntity(
                        aiServiceUrl + "/predict",
                        request,
                        Map.class
                );
    
                if (aiResponse.getBody() != null) {
                    Map<String, Object> responseBody = aiResponse.getBody();
                    if (responseBody != null && responseBody.containsKey("prediction")) {
                        Map<String, Object> predictions = (Map<String, Object>) responseBody.get("prediction");
                        if (predictions != null) {
                            if (incident.getCategory() == null || incident.getCategory().isEmpty()) {
                                incident.setCategory((String) predictions.get("category"));
                            }
                            if (incident.getPriority() == 0) {
                                incident.setPriority(((Number) predictions.get("priority")).intValue());
                            }
                        }
                    }
                }
            }
    
            // Ghassen added  reporter
            String reporterUsername = incident.getReporter().getUsername(); 
            User reporter = userRepository.findByUsername(reporterUsername); 
    
            if (reporter != null) {
                incident.setReporter(reporter); 
            } else {
                throw new RuntimeException("Reporter not found"); 
            }
    
        } catch (Exception e) {
            System.err.println("Error calling AI service or finding reporter: " + e.getMessage());
            if (incident.getCategory() == null || incident.getCategory().isEmpty()) {
                incident.setCategory("GENERAL");
            }
            if (incident.getPriority() == 0) {
                incident.setPriority(2);
            }
        }
    
        loadUserData(incident); 
        return incidentRepository.save(incident); 
    }
    //ghassen updated this funvtion
    public Incident updateIncident(String id, Incident incident) {
        if (incidentRepository.existsById(id)) {
            Incident existingIncident = incidentRepository.findById(id).orElse(null);
            if (existingIncident != null) {
                incident.setId(id);
                
                incident.setReporter(existingIncident.getReporter());
                loadUserData(incident);
                return incidentRepository.save(incident);
            }
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
    // said added this 
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


    // said added this
    public List<Incident> findByCategoryIn(List<String> specializations) {
        
        List<String> lowerCaseSpecializations = specializations.stream()
            .map(String::toLowerCase)
            .collect(Collectors.toList());

        
        return incidentRepository.findAll().stream()
            .filter(incident -> {
                String lowerCaseCategory = incident.getCategory().toLowerCase();
                return lowerCaseSpecializations.contains(lowerCaseCategory);
            })
            .collect(Collectors.toList());
    }
    //ghassen added this
    public void takeChargeIncident(String incidentId, String username) {
        
        Incident incident = incidentRepository.findById(incidentId)
                .orElseThrow(() -> new RuntimeException("Incident not found"));

        
        User user = technicianRepository.findByUsername(username);


        
        if (!(user instanceof Technician)) {
            throw new RuntimeException("User  is not a technician");
        }

        Technician technician = (Technician) user;

        
        incident.setStatus("In progress");
        incident.setAssignedTechnician(technician);

        
        technician.getAssignedIncidents().add(incident);

        
        incidentRepository.save(incident);
        technicianRepository.save(technician);
    }
    //said added this
    public List<Incident> getIncidentsByTechnicianUsername(String username) {
        Technician technician = technicianRepository.findByUsername(username);
        if (technician != null) {
            return technician.getAssignedIncidents();
        }
        return List.of(); 
    }
    //by ghassen
    public List<Incident> getIncidentsByReporterUsername(String username) {
        User reporter = userRepository.findByUsername(username);
        if (reporter != null) {
            return incidentRepository.findByReporter(reporter);
        }
        return List.of(); 
    }
    
}
