package com.saiph.incident_management.model;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;

public enum Specialization {
    NETWORK, HARDWARE, SOFTWARE, DATABASE, SECURITY;

    @JsonCreator
    public static Specialization fromString(String value) {
        return Specialization.valueOf(value.toUpperCase());
    }

    @JsonValue
    public String toString() {
        return this.name().toLowerCase();
    }
}
