package com.saiph.incident_management.service;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

import waffle.spring.WindowsAuthenticationToken;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.logging.Logger;

@Service
public class ActiveDirectoryUserService {
    private static final Logger logger = Logger.getLogger(ActiveDirectoryUserService.class.getName());
    
    @Autowired
    private UserServiceAD userService; // Your existing user service

    /**
     * Get the current authenticated user
     */
    public String getCurrentUsername() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null) {
            return authentication.getName();
        }
        return null;
    }

    /**
     * Map AD groups to application roles
     * Returns roles in the format your application expects (without "ROLE_" prefix)
     */
    public List<String> mapAdGroupsToApplicationRoles(Collection<? extends GrantedAuthority> authorities) {
        List<String> roles = new ArrayList<>();
        
        for (GrantedAuthority authority : authorities) {
            String authorityString = authority.getAuthority();
            logger.info("Found authority: " + authorityString);
            
            // Add mappings based on your AD group names
            // Adjust these names to match your actual AD group names
            if (authorityString.contains("Domain Admins") || 
                authorityString.contains("App_Administrators")) {
                roles.add("ROLE_ADMIN");
            } else if (authorityString.contains("App_Technicians")) {
                roles.add("ROLE_TECHNICIAN");
            } else if (authorityString.contains("App_NormalUsers")) {
                roles.add("ROLE_USER");
            }
        }
        
        // If no specific role found, default to USER
        if (roles.isEmpty()) {
            roles.add("ROLE_USER");
        }
        
        return roles;
    }

    /**
     * Process Windows authentication and create/update local user as needed
     */
    public void processWindowsAuthentication(Authentication authentication) {
        if (authentication instanceof WindowsAuthenticationToken) {
            String username = authentication.getName();
            logger.info("Processing Windows authentication for: " + username);
            
            // Map AD groups to an application role
            String role = mapAdGroupsToApplicationRoles(authentication.getAuthorities())
                .stream()
                .findFirst()
                .orElse("ROLE_USER")
                .replace("ROLE_", ""); // Remove the ROLE_ prefix to match your model
            
            // Check if the user already exists in your local database
            if (userService.findByUsername(username) == null) {
                // Create a local user entry for this AD user
                // This depends on your User model and service implementation
                // This is just a placeholder - you'll need to adapt it
                userService.createUserFromAD(username, role);
            }
        }
    }
}