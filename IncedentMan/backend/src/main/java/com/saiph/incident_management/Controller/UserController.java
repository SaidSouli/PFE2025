package com.saiph.incident_management.Controller;

import com.saiph.incident_management.model.User;
import com.saiph.incident_management.model.LoginRequest;
import com.saiph.incident_management.model.Specialization;
import com.saiph.incident_management.model.Technician;
import com.saiph.incident_management.service.JWTService;
import com.saiph.incident_management.service.UserService;


import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
@CrossOrigin  
public class UserController {
    private final UserService userService;
    private final JWTService jwtService;

    public UserController(UserService userService , JWTService jwtService) {
        this.userService = userService;
        this.jwtService = jwtService;
    }

    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }

    @PostMapping
public ResponseEntity<?> createUser(@RequestBody Map<String, Object> userData) {
    try {
        User user;
        if ("technician".equalsIgnoreCase((String) userData.get("role"))) {
            user = new Technician();
            Technician technician = (Technician) user;
            
            // Handle specializations conversion
            if (userData.containsKey("specializations")) {
                List<String> specs = (List<String>) userData.get("specializations");
                technician.setSpecializations(specs.stream()
                    .map(String::toUpperCase)
                    .map(Specialization::valueOf)
                    .collect(Collectors.toList()));
            }
        } else {
            user = new User();
        }

        // Common field mapping
        user.setUsername((String) userData.get("username"));
        user.setPassword((String) userData.get("password"));
        user.setEmail((String) userData.get("email"));
        user.setRole((String) userData.get("role"));

        User savedUser = userService.createUser(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUser);
        
    } catch (IllegalArgumentException e) {
        return ResponseEntity.badRequest().body("Invalid specialization value");
    } catch (Exception e) {
        return ResponseEntity.internalServerError().body("Server error: " + e.getMessage());
    }
}
    @PostMapping("/login")
    public ResponseEntity<?> loginUser (@RequestBody LoginRequest loginRequest) {
        
        User user = userService.findByUsername(loginRequest.getUsername());

       
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body("User  not found");
        }

        
        if (!user.getPassword().equals(loginRequest.getPassword())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Invalid password");
        }

        
        String token = jwtService.generateToken(user.getUsername());

        
        return ResponseEntity.ok(Map.of(
            "message", "Login successful",
            "token", token, 
            "role", user.getRole(),
            "username", user.getUsername()
        ));
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteUser(@PathVariable String id) {
        boolean deleted = userService.deleteUser(id);
        
        if (deleted) {
            return ResponseEntity.ok().body("User deleted successfully");
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    @PutMapping("/{id}")
    public ResponseEntity<?> updateUser(@PathVariable String id, @RequestBody User user) {
        User updatedUser = userService.updateUser(id, user);
        
        if (updatedUser != null) {
            return ResponseEntity.ok(updatedUser);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable String id) {
        User user = userService.getUserById(id); 
        if (user != null) {
            return ResponseEntity.ok(user); 
        } else {
            return ResponseEntity.notFound().build(); 
    }
}
}