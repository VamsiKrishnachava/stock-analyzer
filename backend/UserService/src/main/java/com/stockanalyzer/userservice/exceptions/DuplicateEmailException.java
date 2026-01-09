package com.stockanalyzer.userservice.exceptions;

public class DuplicateEmailException extends RuntimeException {

    public DuplicateEmailException(String email) {
        super("Email already in use: " + email);
    }

    public DuplicateEmailException(String message, Throwable cause) {
        super(message, cause);
    }
}
