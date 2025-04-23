package com.saiph.incident_management.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;

import com.saiph.incident_management.filter.JwtAuthenticationFilter;
import com.saiph.incident_management.service.*;

import waffle.servlet.spi.BasicSecurityFilterProvider;
import waffle.servlet.spi.NegotiateSecurityFilterProvider;
import waffle.servlet.spi.SecurityFilterProviderCollection;
import waffle.spring.NegotiateSecurityFilter;
import waffle.spring.NegotiateSecurityFilterEntryPoint;
import waffle.spring.WindowsAuthenticationProvider;
import waffle.windows.auth.impl.WindowsAuthProviderImpl;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;

import java.io.IOException;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JWTService jwtService;
    
    @Autowired
    private ActiveDirectoryUserService adUserService;

    @Autowired
    private JwtAuthenticationFilter jwtAuthFilter;

    // Windows Authentication components
    @Bean
    public WindowsAuthProviderImpl windowsAuthProvider() {
        return new WindowsAuthProviderImpl();
    }

    @Bean
    public WindowsAuthenticationProvider windowsAuthenticationProvider() {
        WindowsAuthenticationProvider provider = new WindowsAuthenticationProvider();
        provider.setAuthProvider(windowsAuthProvider());
        
        // For older Waffle versions, setPrincipalFormat takes a String not an enum
        provider.setPrincipalFormat("fqn");
        provider.setRoleFormat("fqn");
        
        return provider;
    }

    @Bean
    public SecurityFilterProviderCollection securityFilterProviders() {
        WindowsAuthProviderImpl authProvider = windowsAuthProvider();
        return new SecurityFilterProviderCollection(
            new waffle.servlet.spi.SecurityFilterProvider[] {
                new NegotiateSecurityFilterProvider(authProvider),
                new BasicSecurityFilterProvider(authProvider)
            }
        );
    }

    @Bean
    public NegotiateSecurityFilterEntryPoint negotiateSecurityFilterEntryPoint() {
        NegotiateSecurityFilterEntryPoint entryPoint = new NegotiateSecurityFilterEntryPoint();
        entryPoint.setProvider(securityFilterProviders());
        return entryPoint;
    }
    
    // Custom success handler for Windows Auth
    @Bean
    public WindowsAuthSuccessHandler windowsAuthSuccessHandler() {
        return new WindowsAuthSuccessHandler();
    }

    // Custom success handler implementation
    public class WindowsAuthSuccessHandler extends SimpleUrlAuthenticationSuccessHandler {
        @Override
        public void onAuthenticationSuccess(
                HttpServletRequest request, 
                HttpServletResponse response,
                Authentication authentication) throws IOException, ServletException {
            
            // Extract user information from Windows authentication
            String username = authentication.getName();
            
            // Process AD user in your service
            adUserService.processWindowsAuthentication(authentication);
            
            // Map AD groups to your application roles
            String role = adUserService.mapAdGroupsToApplicationRoles(
                authentication.getAuthorities())
                .stream()
                .findFirst()
                .orElse("ROLE_USER")
                .replace("ROLE_", "");
            
            // Generate JWT token
            String token = jwtService.generateToken(username);
            
            // Set the response
            response.setContentType("application/json");
            response.getWriter().write(String.format(
                "{\"message\":\"Windows authentication successful\",\"token\":\"%s\",\"role\":\"%s\",\"username\":\"%s\"}",
                token, role, username
            ));
        }
    }

    @Bean
    public NegotiateSecurityFilter negotiateSecurityFilter() {
        NegotiateSecurityFilter filter = new NegotiateSecurityFilter();
        filter.setProvider(securityFilterProviders());
        
        // Older versions of Waffle don't have setAuthenticationSuccessHandler
        // We need to extend the filter to override the success behavior
        
        return filter;
    }

    @Bean
    public AuthenticationManager authenticationManager(HttpSecurity http) throws Exception {
        return http.getSharedObject(AuthenticationManagerBuilder.class)
                .authenticationProvider(windowsAuthenticationProvider())
                .build();
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // Disable CSRF for API access
        http.csrf(csrf -> csrf.disable());
        
        // Configure authorization rules
        http.authorizeHttpRequests(authorize -> authorize
            .requestMatchers("/api/users/login", "/api/users/register", "/api/public/**", "/api/windowsAuth").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .requestMatchers("/api/technician/**").hasRole("TECHNICIAN")
            .requestMatchers("/api/user/**").hasRole("USER")
            .anyRequest().authenticated()
        );
        
        // Add a controller endpoint to handle Windows Auth instead of using a filter
        
        // Add JWT filter for token validation
        http.addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);
            
        return http.build();
    }
}