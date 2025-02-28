package com.saiph.incident_management.Controller;

import com.saiph.incident_management.model.Incident;

import com.saiph.incident_management.service.IncidentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;


import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/incidents")
public class IncidentController {
    
    @Autowired
    private IncidentService incidentService;
   
    
    @GetMapping
    public ResponseEntity<List<Incident>> getAllIncidents() {
        return new ResponseEntity<>(incidentService.getAllIncidents(), HttpStatus.OK);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<Incident> getIncidentById(@PathVariable String id) {
        return incidentService.getIncidentById(id)
                .map(incident -> new ResponseEntity<>(incident, HttpStatus.OK))
                .orElse(new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }
    
    @PostMapping
    public ResponseEntity<Incident> createIncident(@RequestBody Incident incident) {
        return new ResponseEntity<>(incidentService.createIncident(incident), HttpStatus.CREATED);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<Incident> updateIncident(@PathVariable String id, @RequestBody Incident incident) {
        Incident updatedIncident = incidentService.updateIncident(id, incident);
        if (updatedIncident != null) {
            return new ResponseEntity<>(updatedIncident, HttpStatus.OK);
        }
        return new ResponseEntity<>(HttpStatus.NOT_FOUND);
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteIncident(@PathVariable String id) {
        incidentService.deleteIncident(id);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
    
    @GetMapping("/status/{status}")
    public ResponseEntity<List<Incident>> getIncidentsByStatus(@PathVariable String status) {
        return new ResponseEntity<>(incidentService.findByStatus(status), HttpStatus.OK);
    }
    
    @GetMapping("/priority/{priority}")
    public ResponseEntity<List<Incident>> getIncidentsByPriority(@PathVariable int priority) {
        return new ResponseEntity<>(incidentService.findByPriority(priority), HttpStatus.OK);
    }
    
    @GetMapping("/category/{category}")
    public ResponseEntity<List<Incident>> getIncidentsByCategory(@PathVariable String category) {
        return new ResponseEntity<>(incidentService.findByCategory(category), HttpStatus.OK);
    }
    
    @GetMapping("/technician/{technicianId}")
    public ResponseEntity<List<Incident>> getIncidentsByTechnician(@PathVariable String technicianId) {
        return new ResponseEntity<>(incidentService.findByTechnician(technicianId), HttpStatus.OK);
    }
    
    @GetMapping("/reporter/{reporterId}")
    public ResponseEntity<List<Incident>> getIncidentsByReporter(@PathVariable String reporterId) {
        return new ResponseEntity<>(incidentService.findByReporter(reporterId), HttpStatus.OK);
    }
    
    @PostMapping("/by-specialization")
    public ResponseEntity<List<Incident>> getIncidentsBySpecialization(@RequestBody Map<String, List<String>> request) {
        List<String> specializations = request.get("specializations");
        List<Incident> incidents = incidentService.findByCategoryIn(specializations);
        return ResponseEntity.ok(incidents);
    }
    @PutMapping("/{incidentId}/take-charge")
    public ResponseEntity<?> takeChargeIncident(@PathVariable String incidentId, @RequestParam String username) {
        incidentService.takeChargeIncident(incidentId, username);
        return ResponseEntity.ok().build();
    }

}
