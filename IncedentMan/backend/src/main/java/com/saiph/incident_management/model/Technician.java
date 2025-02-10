package com.saiph.incident_management.model;

import java.util.ArrayList;
import java.util.List;

import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "users")
public class Technician extends User {
    private List<Specialization> specializations = new ArrayList<>();
    private List<Incident> assignedIncidents = new ArrayList<>();
    
    public List<Specialization> getSpecializations() {
        return specializations;
    }
    public void setSpecializations(List<Specialization> specializations) {
        this.specializations = specializations;
    }
    public List<Incident> getAssignedIncidents() {
        return assignedIncidents;
    }
    public void setAssignedIncidents(List<Incident> assignedIncidents) {
        this.assignedIncidents = assignedIncidents;
    }
    
}