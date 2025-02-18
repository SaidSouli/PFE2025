package com.saiph.incident_management.dto;


public class AIPredictionResponse {
    private String category;
    private int priority;

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }
}
