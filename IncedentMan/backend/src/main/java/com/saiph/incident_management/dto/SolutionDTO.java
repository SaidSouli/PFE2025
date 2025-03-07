package com.saiph.incident_management.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class SolutionDTO {

    @JsonProperty("IncidentId")
    private String incidentId;
    
    @JsonProperty("TechnicianName")
    private String technicianName;
    
    @JsonProperty("description")
    private String description;
    
    // Default constructor required for Jackson
    public SolutionDTO() {
    }
    
    public SolutionDTO(String incidentId, String technicianName, String description) {
        this.incidentId = incidentId;
        this.technicianName = technicianName;
        this.description = description;
    }
    
    public String getIncidentId() {
        return incidentId;
    }
    
    public void setIncidentId(String incidentId) {
        this.incidentId = incidentId;
    }
    
    public String getTechnicianName() {
        return technicianName;
    }
    
    public void setTechnicianName(String technicianName) {
        this.technicianName = technicianName;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }

    @Override
    public String toString() {
        return "SolutionDTO [incidentId=" + incidentId + ", technicianName=" + technicianName + ", description="
                + (description != null && description.length() > 30 ? description.substring(0, 30) + "..." : description) + "]";
    }
}