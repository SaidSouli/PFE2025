import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private currentUserSubject = new BehaviorSubject<any>(null);
  public currentUser$ = this.currentUserSubject.asObservable();

  constructor(private http: HttpClient, private router: Router) {}

  login(username: string, password: string) {
    
    username = username.trim();
    password = password.trim();
    
    return this.http.post<any>('http://localhost:8080/api/users/login', {
      username,
      password
    }).subscribe({
      next: (response) => {
        if (response && response.token) {
          localStorage.setItem('jwtToken', response.token);
          localStorage.setItem('username', response.username);
          localStorage.setItem('role', response.role);
          this.currentUserSubject.next(response);

          this.redirectBasedOnRole(response.role);
        } else {
          console.error('No token found in response');
        }
      },
      error: (error) => {
        console.error('Login failed', error);
      }
    });
  }

  logout() {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  getCurrentUser() {
    return this.currentUserSubject.value;
  }

  isLoggedIn() {
    return !!localStorage.getItem('jwtToken');
  }

  private redirectBasedOnRole(role: string) {
    switch (role.toLowerCase()) {
      case 'admin':
        this.router.navigate(['/admin']);
        break;
      case 'user':
        this.router.navigate(['/report-incident']);
        break;
      case 'technician':
        this.router.navigate(['/technician']);
        break;
      default:
        this.router.navigate(['/home']);
    }
  }
}