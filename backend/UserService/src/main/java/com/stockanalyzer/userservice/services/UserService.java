package com.stockanalyzer.userservice.services;

import com.stockanalyzer.userservice.dtos.UserResponseDto;

public interface UserService {

    void createUser(String fullName, String password, String email);

    void deleteUser(Long userId);

    void updateUserEmail(Long userId, String newEmail);

    void updateUserFullName(Long userId, String newFullName);

    void updateUserPassword(Long userId, String newPassword);

    UserResponseDto getUserById(Long userId);

    UserResponseDto getUserByEmail(String email);


    
}
