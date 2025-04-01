package com.saiph.incident_management.service;

import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.saiph.incident_management.model.Incident;
import com.saiph.incident_management.model.Solution;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.repository.IncidentRepository;
import com.saiph.incident_management.repository.SolutionRepository;
import com.saiph.incident_management.repository.TechnicianRepository;

@Service
public class SolutionService {
    
    @Autowired
    private SolutionRepository solutionRepository;
    
    @Autowired
    private IncidentRepository incidentRepository;
    
    @Autowired
    private TechnicianRepository technicianRepository;
    
    public Solution createSolution(String incidentId, String technicianName, String description) {
        // Get the incident
        Incident incident = incidentRepository.findById(incidentId)
                .orElseThrow(() -> new RuntimeException("Incident not found with id: " + incidentId));
        
        // Get the technician
        Technician technician = technicianRepository.findByUsername(technicianName);
        if (technician == null) {
            throw new RuntimeException("Technician not found with name: " + technicianName);
        }
        
        // Check if this technician is assigned to this incident
        if (!technician.getId().equals(incident.getAssignedTechnician().getId())) {
            throw new RuntimeException("This technician is not assigned to this incident");
        }
        
        // Check if incident already has a solution
        Solution existingSolution = solutionRepository.findByIncidentId(incidentId);
        if (existingSolution != null) {
            throw new RuntimeException("This incident already has a solution");
        }
        
        // Create and save the solution
        Solution solution = new Solution(description, technician, incident);
        solution.setCreationDate(new Date());
        
        // Update incident status and resolution date
        incident.setStatus("Waiting");
        incident.setResolutionDate(new Date());
        incidentRepository.save(incident);
        
        // Update the assignedIncidents list in the Technician object
        List<Incident> assignedIncidents = technician.getAssignedIncidents();
        for (int i = 0; i < assignedIncidents.size(); i++) {
            if (assignedIncidents.get(i).getId().equals(incidentId)) {
                assignedIncidents.set(i, incident); // Update the incident in the list
                break;
            }
        }
        technicianRepository.save(technician); // Save the updated technician
        
        return solutionRepository.save(solution);
    }
    
    public Solution updateSolution(String solutionId, String description) {
        Solution solution = solutionRepository.findById(solutionId)
                .orElseThrow(() -> new RuntimeException("Solution not found with id: " + solutionId));
        
        solution.setDescription(description);
        return solutionRepository.save(solution);
    }
    
    public Solution getSolutionByIncidentId(String incidentId) {
        return solutionRepository.findByIncidentId(incidentId);
    }
    
    public Solution getSolutionById(String id) {
        return solutionRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Solution not found with id: " + id));
    }
    
    public List<Solution> getAllSolutions() {
        return solutionRepository.findAll();
    }
    
    public void deleteSolution(String solutionId) {
        // Récupérer la solution
        Solution solution = solutionRepository.findById(solutionId)
                .orElseThrow(() -> new RuntimeException("Solution not found with id: " + solutionId));
        
        // Récupérer l'incident associé à la solution
        Incident incident = solution.getIncident();
        
        // Récupérer le technicien assigné à l'incident
        Technician technician = incident.getAssignedTechnician();
        
        // Mettre à jour le statut de l'incident vers "In Progress"
        incident.setStatus("In progress");
        incident.setResolutionDate(null); // Réinitialiser la date de résolution
        
        // Sauvegarder l'incident mis à jour
        incidentRepository.save(incident);
        
        // Mettre à jour la liste assignedIncidents du technicien
        List<Incident> assignedIncidents = technician.getAssignedIncidents();
        for (int i = 0; i < assignedIncidents.size(); i++) {
            if (assignedIncidents.get(i).getId().equals(incident.getId())) {
                assignedIncidents.set(i, incident); // Mettre à jour l'incident dans la liste
                break;
            }
        }
        
        // Sauvegarder le technicien mis à jour
        technicianRepository.save(technician);
        
        // Supprimer la solution
        solutionRepository.delete(solution);
    }
    
}