package com.saiph.incident_management.repository;


import com.saiph.incident_management.model.User;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface UserRepository extends MongoRepository<User, String> {
    User findByUsername(String username);
    User findByEmail(String email);
}