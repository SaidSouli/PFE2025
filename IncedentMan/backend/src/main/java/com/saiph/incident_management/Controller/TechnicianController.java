package com.saiph.incident_management.Controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.service.TechnicianService;

@RestController
@RequestMapping("/api/technicians")
public class TechnicianController {

    @Autowired
    private TechnicianService technicianService;

    @GetMapping("/{username}/specializations")
    public ResponseEntity<List<Specialization>> getTechnicianSpecializations(@PathVariable String username) {
        List<Specialization> specializations = technicianService.getSpecializationsByUsername(username);
        return ResponseEntity.ok(specializations);
    }
}
