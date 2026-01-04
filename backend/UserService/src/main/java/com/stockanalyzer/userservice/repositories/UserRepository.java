package com.stockanalyzer.userservice.repositories;

import java.util.Optional;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.stockanalyzer.userservice.entities.User;

@Repository
public interface UserRepository extends JpaRepository<User,Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    boolean existsById(Long id);
    Optional<User> findById(Long id);
    void deleteById(Long id);
    Page<User> findAll(Pageable pageable);
}
