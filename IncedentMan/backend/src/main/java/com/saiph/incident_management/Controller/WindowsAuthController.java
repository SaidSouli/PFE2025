package com.saiph.incident_management.Controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.saiph.incident_management.service.ActiveDirectoryUserService;
import com.saiph.incident_management.service.JWTService;

import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class WindowsAuthController {

    @Autowired
    private JWTService jwtService;
    
    @Autowired
    private ActiveDirectoryUserService adUserService;

    @GetMapping("/windowsAuth")
    public Map<String, String> windowsAuth(Authentication auth, HttpServletResponse response) throws IOException {
        Map<String, String> result = new HashMap<>();
        
        if (auth != null) {
            // Extract username from Windows authentication
            String username = auth.getName();
            
            // Process the Windows auth user
            adUserService.processWindowsAuthentication(auth);
            
            // Map AD groups to application roles
            String role = adUserService.mapAdGroupsToApplicationRoles(auth.getAuthorities())
                .stream()
                .findFirst()
                .orElse("ROLE_USER")
                .replace("ROLE_", "");
            
            // Generate JWT token
            String token = jwtService.generateToken(username);
            
            result.put("message", "Windows authentication successful");
            result.put("token", token);
            result.put("role", role);
            result.put("username", username);
        } else {
            result.put("message", "Authentication failed");
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        }
        
        return result;
    }
}