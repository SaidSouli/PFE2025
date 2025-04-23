package com.saiph.incident_management.service;

import com.saiph.incident_management.model.User;
import com.saiph.incident_management.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Collections;

@Service
public class UserServiceAD implements UserDetailsService {

    @Autowired
    private UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = findByUsername(username);
        if (user == null) {
            throw new UsernameNotFoundException("User not found with username: " + username);
        }
        
        // Create Spring Security UserDetails object from your User entity
        return new org.springframework.security.core.userdetails.User(
            user.getUsername(),
            user.getPassword(),  // This will be "WINDOWS_AUTH" for AD users
            Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + user.getRole()))
        );
    }
    
    public User findByUsername(String username) {
        // This method should already exist in your service
        return userRepository.findByUsername(username);
    }
    
    public User save(User user) {
        // This method should already exist in your service
        return userRepository.save(user);
    }
    
    public User createUserFromAD(String username, String role) {
        // Check if user already exists
        User existingUser = findByUsername(username);
        if (existingUser != null) {
            return existingUser;
        }
        
        // Create a new user with AD username
        User user = new User();
        user.setUsername(username);
        user.setPassword("WINDOWS_AUTH"); // Special marker password, not used for login
        user.setRole(role);
        user.setEmail(username + "@incidentmgmt.local"); // Default email, can be updated later
        user.setFirstLogin(true);
        
        // Save the user
        return save(user);
    }
    
}