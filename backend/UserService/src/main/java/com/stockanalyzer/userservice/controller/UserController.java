package com.stockanalyzer.userservice.controller;


import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.stockanalyzer.userservice.dtos.UserResponseDto;
import com.stockanalyzer.userservice.services.UserService;


@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponseDto> getUserDetails(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }
    
}
