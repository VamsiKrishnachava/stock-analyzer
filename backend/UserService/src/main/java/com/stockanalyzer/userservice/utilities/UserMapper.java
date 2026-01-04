package com.stockanalyzer.userservice.utilities;

import com.stockanalyzer.userservice.dtos.UserResponseDto;
import com.stockanalyzer.userservice.entities.User;

public final class UserMapper {
    private UserMapper() {    }

    public static UserResponseDto toDto(User user) {
        return new UserResponseDto(
            user.getId(),
            user.getFullName(),
            user.getEmail(),
            user.getCreatedAt(),
            user.getUpdatedAt()
        );
    }
}
