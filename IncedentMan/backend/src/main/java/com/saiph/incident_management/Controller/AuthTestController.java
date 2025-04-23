package com.saiph.incident_management.Controller;


import com.saiph.incident_management.service.ActiveDirectoryUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api")
public class AuthTestController {

    @Autowired
    private ActiveDirectoryUserService adUserService;

    @GetMapping("/whoami")
    public Map<String, Object> whoAmI(Authentication authentication) {
        Map<String, Object> userInfo = new HashMap<>();
        
        if (authentication != null) {
            userInfo.put("username", authentication.getName());
            
            // Extract and add authorities/roles
            List<String> authorities = authentication.getAuthorities().stream()
                    .map(GrantedAuthority::getAuthority)
                    .collect(Collectors.toList());
            userInfo.put("authorities", authorities);
            
            // Map AD groups to application roles
            List<String> appRoles = adUserService.mapAdGroupsToApplicationRoles(
                    authentication.getAuthorities());
            userInfo.put("applicationRoles", appRoles);
            
            // Authentication type
            userInfo.put("authenticationType", authentication.getClass().getSimpleName());
        } else {
            userInfo.put("error", "Not authenticated");
        }
        
        return userInfo;
    }
    
    @GetMapping("/public/hello")
    public String publicEndpoint() {
        return "This is a public endpoint - no authentication required";
    }
    
    @GetMapping("/user/hello")
    public String userEndpoint() {
        return "Hello, User! You've accessed a protected user endpoint";
    }
    
    @GetMapping("/technician/hello")
    public String technicianEndpoint() {
        return "Hello, Technician! You've accessed a protected technician endpoint";
    }
    
    @GetMapping("/admin/hello")
    public String adminEndpoint() {
        return "Hello, Admin! You've accessed a protected admin endpoint";
    }
}