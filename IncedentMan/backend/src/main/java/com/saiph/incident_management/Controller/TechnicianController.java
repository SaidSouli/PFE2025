package com.saiph.incident_management.Controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;


import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.repository.IncidentRepository;
import com.saiph.incident_management.repository.TechnicianRepository;
import com.saiph.incident_management.service.TechnicianService;

@RestController
@RequestMapping("/api/technicians")
public class TechnicianController {

    @Autowired
    private TechnicianService technicianService;
    @Autowired 
    private IncidentRepository incidentRepository;
    @Autowired
    private TechnicianRepository technicianRepository;
    

    @GetMapping("/{username}/specializations")
    public ResponseEntity<List<Specialization>> getTechnicianSpecializations(@PathVariable String username) {
        List<Specialization> specializations = technicianService.getSpecializationsByUsername(username);
        return ResponseEntity.ok(specializations);
    }
    @PutMapping("/{technicianId}/incidents/{incidentId}/status")
    public ResponseEntity<Technician> updateIncidentStatus(
            @PathVariable String technicianId,
            @PathVariable String incidentId,
            @RequestParam String status) {
        
        Technician updatedTechnician = technicianService.updateAssignedIncidentStatus(technicianId, incidentId, status);
        return ResponseEntity.ok(updatedTechnician);
    }
    @GetMapping("/{incidentId}/technician")
    public ResponseEntity<Technician> getAssignedTechnician(@PathVariable String incidentId) {
        Technician technician = technicianService.getAssignedTechnician(incidentId);
        
        if (technician == null) {
            return ResponseEntity.notFound().build();
        }
        
        return ResponseEntity.ok(technician);
    }
    
}
