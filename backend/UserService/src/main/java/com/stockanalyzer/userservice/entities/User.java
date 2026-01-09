package com.stockanalyzer.userservice.entities;

import java.time.Instant;
import java.util.Objects;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name="users")
public class User {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	@Column(nullable = false)
	private String fullName;
	
	@Column(nullable = false)
	private String password;
	
	@Column(nullable = false, unique = true)
	private String email;

	@Column(nullable = false, updatable = false, insertable = false)
	private Instant createdAt;
	
	private Instant updatedAt;
	
	public User(String fullName, String password, String email) {
		this.fullName = fullName;
		this.password = password;
		this.email = email;
	}

	public String getEmail() {
		return email;
	}

	public void setEmail(String email) {
		this.email = email;
	}

	public Long getId() {
		return id;
	}

	public String getFullName() {
		return fullName;
	}

	public void setFullName(String fullName) {
		this.fullName = fullName;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}
	
	public Instant getCreatedAt() {
		return createdAt;
	}

	public Instant getUpdatedAt() {
		return updatedAt;
	}
	
	@Override
	public int hashCode() {
		return Objects.hash(this.email);
	}
	
	@Override 
	public boolean equals(Object obj) {
		if(this == obj) return true;
		if (obj == null) return false;
		if(getClass() != obj.getClass()) return false;
		User other = (User) obj;
		return Objects.equals(other.email, this.email);
	}

	
	

}
