package com.saiph.incident_management.model;

import java.util.Date;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import com.fasterxml.jackson.annotation.JsonBackReference;



@Document(collection = "incidents")
public class Incident {
    @Id
    private String id;
    private String title;
    private String description;
    private Date creationDate = new Date();
    private String status = "Open";  // Default status
    private int priority = 2;        // Default priority
    private String category = "GENERAL"; // Default category
    @DBRef
    private User reporter;
    @DBRef
    @JsonBackReference
    private Technician assignedTechnician;
    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }
    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
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
    public String getStatus() {
        return status;
    }
    public void setStatus(String status) {
        this.status = status;
    }
    public int getPriority() {
        return priority;
    }
    public void setPriority(int priority) {
        this.priority = priority;
    }
    public String getCategory() {
        return category;
    }
    public void setCategory(String category) {
        this.category = category;
    }
    public User getReporter() {
        return reporter;
    }
    public void setReporter(User reporter) {
        this.reporter = reporter;
    }
    public Technician getAssignedTechnician() {
        return assignedTechnician;
    }
    public void setAssignedTechnician(Technician assignedTechnician) {
        this.assignedTechnician = assignedTechnician;
    }
    
    
}
