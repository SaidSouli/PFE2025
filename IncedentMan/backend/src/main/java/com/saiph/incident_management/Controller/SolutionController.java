package com.saiph.incident_management.Controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.saiph.incident_management.dto.SolutionDTO;
import com.saiph.incident_management.model.Solution;
import com.saiph.incident_management.service.SolutionService;

@RestController
@RequestMapping("/api/solutions")
public class SolutionController {

    @Autowired
    private SolutionService solutionService;

    @GetMapping
    public ResponseEntity<List<Solution>> getAllSolutions() {
        return ResponseEntity.ok(solutionService.getAllSolutions());
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getSolutionById(@PathVariable("id") String id) {
        try {
            Solution solution = solutionService.getSolutionById(id);
            return ResponseEntity.ok(solution);
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Error: " + e.getMessage());
        }
    }

    @GetMapping("/incident/{incidentId}")
    public ResponseEntity<?> getSolutionByIncidentId(@PathVariable("incidentId") String incidentId) {
        Solution solution = solutionService.getSolutionByIncidentId(incidentId);
        if (solution != null) {
            return ResponseEntity.ok(solution);
        } else {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("No solution found for incident ID: " + incidentId);
        }
    }

    @PostMapping
    public ResponseEntity<?> createSolution(@RequestBody SolutionDTO solutionDTO) {
        try {
            // Debug logging
            System.out.println("Received DTO: incidentId=" + solutionDTO.getIncidentId() + 
                ", technicianName=" + solutionDTO.getTechnicianName() + 
                ", description=" + (solutionDTO.getDescription() != null ? 
                        (solutionDTO.getDescription().length() > 30 ? 
                            solutionDTO.getDescription().substring(0, 30) + "..." : 
                            solutionDTO.getDescription()) : 
                        "null"));
            
            // Validate inputs
            if (solutionDTO.getIncidentId() == null || solutionDTO.getIncidentId().trim().isEmpty()) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Incident ID is required");
            }
            if (solutionDTO.getTechnicianName() == null || solutionDTO.getTechnicianName().trim().isEmpty()) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Technician name is required");
            }
            if (solutionDTO.getDescription() == null || solutionDTO.getDescription().trim().isEmpty()) {
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Description is required");
            }
            
            Solution solution = solutionService.createSolution(
                solutionDTO.getIncidentId(), 
                solutionDTO.getTechnicianName(), 
                solutionDTO.getDescription()
            );
            return ResponseEntity.status(HttpStatus.CREATED).body(solution);
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body("Error creating solution: " + e.getMessage());
        }
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateSolution(
            @PathVariable("id") String id,
            @RequestBody SolutionDTO solutionDTO) {
        try {
            Solution solution = solutionService.updateSolution(id, solutionDTO.getDescription());
            return ResponseEntity.ok(solution);
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Error updating solution: " + e.getMessage());
        }
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteSolution(@PathVariable("id") String id) {
        try {
            solutionService.deleteSolution(id);
            return ResponseEntity.noContent().build();
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("Error deleting solution: " + e.getMessage());
        }
    }
    @PostMapping("/test")
    public ResponseEntity<String> testEndpoint(@RequestBody SolutionDTO solutionDTO) {
        return ResponseEntity.ok("Received: " + solutionDTO.toString());
    }
}