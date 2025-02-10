package com.saiph.incident_management.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;
import com.saiph.incident_management.model.User;
import com.saiph.incident_management.repository.UserRepository;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public User createUser(User user) {
        return userRepository.save(user);
    }

    public User findByUsername(String username) {
        return userRepository.findByUsername(username);
    }
    public boolean deleteUser(String id) {
        Optional<User> userOptional = userRepository.findById(id);
        
        if (userOptional.isPresent()) {
            userRepository.deleteById(id);
            return true;
        }
        
        return false;
    }
    public User updateUser(String id, User updatedUser) {
        Optional<User> existingUserOptional = userRepository.findById(id);
        
        if (existingUserOptional.isPresent()) {
            User existingUser = existingUserOptional.get();
            
            // Update fields selectively
            if (updatedUser.getUsername() != null) {
                existingUser.setUsername(updatedUser.getUsername());
            }
            if (updatedUser.getPassword() != null) {
                existingUser.setPassword(updatedUser.getPassword());
            }
            if (updatedUser.getEmail() != null) {
                existingUser.setEmail(updatedUser.getEmail());
            }
            if (updatedUser.getRole() != null) {
                existingUser.setRole(updatedUser.getRole());
            }
            
            return userRepository.save(existingUser);
        }
        
        return null;
    }
    public User getUserById(String id) {
        Optional<User> userOptional = userRepository.findById(id);
        return userOptional.orElse(null); // Returns the User if found, or null if not
    }
}