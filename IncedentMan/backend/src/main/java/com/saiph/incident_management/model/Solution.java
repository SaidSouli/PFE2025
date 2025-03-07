package com.saiph.incident_management.model;

import java.util.Date;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "solutions")
public class Solution {

    @Id
    private String id;
    private String description;
    private Date creationDate;

    @DBRef
    private Technician creator;

    @DBRef
    private Incident incident;
    
    public Solution() {
    }
    
    public Solution(String description, Technician creator, Incident incident) {
        this.description = description;
        this.creator = creator;
        this.incident = incident;
    }

    public Solution(String description, Date creationDate, Technician creator, Incident incident) {
        this.description = description;
        this.creationDate = creationDate;
        this.creator = creator;
        this.incident = incident;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Date getCreationDate() {
        return creationDate;
    }

    public void setCreationDate(Date creationDate) {
        this.creationDate = creationDate;
    }

    public Technician getCreator() {
        return creator;
    }

    public void setCreator(Technician creator) {
        this.creator = creator;
    }

    public Incident getIncident() {
        return incident;
    }

    public void setIncident(Incident incident) {
        this.incident = incident;
    }
}