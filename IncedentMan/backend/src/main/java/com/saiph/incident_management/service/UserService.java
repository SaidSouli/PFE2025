package com.saiph.incident_management.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.model.Technician;
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
    public User updateUser(String id, Map<String, Object> userData) {
    Optional<User> existingUserOptional = userRepository.findById(id);
    
    if (existingUserOptional.isPresent()) {
        User existingUser = existingUserOptional.get();
        
        // Update base fields
        if (userData.containsKey("username")) {
            existingUser.setUsername((String) userData.get("username"));
        }
        if (userData.containsKey("password")) {
            existingUser.setPassword((String) userData.get("password"));
        }
        if (userData.containsKey("email")) {
            existingUser.setEmail((String) userData.get("email"));
        }
        if (userData.containsKey("role")) {
            existingUser.setRole((String) userData.get("role"));
        }
        
        // Handle technician specializations
        if (existingUser instanceof Technician && userData.containsKey("specializations")) {
            Technician technician = (Technician) existingUser;
            Object specsObj = userData.get("specializations");
            
            if (specsObj instanceof List<?>) {
                List<?> specsList = (List<?>) specsObj;
                List<Specialization> specs = new ArrayList<>();
                
                for (Object item : specsList) {
                    if (item instanceof String) {
                        try {
                            Specialization spec = Specialization.valueOf(((String) item).toUpperCase());
                            specs.add(spec);
                        } catch (IllegalArgumentException e) {
                            throw new IllegalArgumentException("Invalid specialization value: " + item);
                        }
                    } else {
                        throw new IllegalArgumentException("Specialization values must be strings");
                    }
                }
                
                technician.setSpecializations(specs);
            } else {
                throw new IllegalArgumentException("Specializations must be a list");
            }
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