package com.stockanalyzer.userservice.dtos;

import java.time.Instant;

public class UserResponseDto {
    private Long id;
    private String name;        
    private String email;
    private Instant createdAt;
    private Instant updatedAt;

    public UserResponseDto(Long id, String name, String email, Instant createdAt, Instant updatedAt) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }
    public Long getId() {
        return id;
    }       
    public String getName() {
        return name;
    }
    public String getEmail() {
        return email;
    }   
    public Instant getCreatedAt() {
        return createdAt;
    }
    public Instant getUpdatedAt() {
        return updatedAt;
    }
}
