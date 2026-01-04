package com.stockanalyzer.userservice.services.serviceImpl;

import com.stockanalyzer.userservice.entities.User;
import com.stockanalyzer.userservice.exceptions.UserNotFoundException;

import org.springframework.stereotype.Service;

import com.stockanalyzer.userservice.services.UserService;
import com.stockanalyzer.userservice.utilities.UserMapper;
import com.stockanalyzer.userservice.dtos.UserResponseDto;
import com.stockanalyzer.userservice.repositories.UserRepository;

@Service
public class UserServiceImpl implements UserService{

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public void createUser(String fullName, String password, String email) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'createUser'");
    }

    @Override
    public void deleteUser(Long userId) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'deleteUser'");
    }

    @Override
    public void updateUserEmail(Long userId, String newEmail) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'updateUserEmail'");
    }

    @Override
    public void updateUserFullName(Long userId, String newFullName) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'updateUserFullName'");
    }

    @Override
    public void updateUserPassword(Long userId, String newPassword) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'updateUserPassword'");
    }

    @Override
    public UserResponseDto getUserById(Long userId) {
        User user = userRepository.findById(userId).orElseThrow(() -> new UserNotFoundException("User not found for the given Id"));
        return UserMapper.toDto(user);
    }

    @Override
    public UserResponseDto getUserByEmail(String email) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'getUserByEmail'");
    }
    
}
