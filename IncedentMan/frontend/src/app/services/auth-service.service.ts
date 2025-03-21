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
          localStorage.setItem('firstLogin',response.firstLogin)
          this.currentUserSubject.next(response);
          if (response.firstLogin){
            this.router.navigate(['/set-password'])
          }else{
          this.redirectBasedOnRole(response.role);}
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
    if (!this.currentUserSubject.value) {
      
      const token = localStorage.getItem('jwtToken');
      const username = localStorage.getItem('username');
      const role = localStorage.getItem('role');
      const firstLogin = localStorage.getItem('firstLogin');
      
      if (token && username && role) {
        const user = {
          token,
          username,
          role,
          firstLogin: firstLogin === 'true'
        };
        this.currentUserSubject.next(user);
        return user;
      }
    }
    return this.currentUserSubject.value;
  }

  isLoggedIn() {
    return !!localStorage.getItem('jwtToken');
  }

  public redirectBasedOnRole(role: string) {
    switch (role.toLowerCase()) {
      case 'admin':
        this.router.navigate(['/admin']);
        break;
      case 'user':
        this.router.navigate(['/incident-consult']);
        break;
      case 'technician':
        this.router.navigate(['/technician']);
        break;
      default:
        this.router.navigate(['/home']);
    }
  }
  
isFirstLogin(): boolean {
  return localStorage.getItem('firstLogin') === 'true';
}


clearFirstLoginFlag(): void {
  localStorage.setItem('firstLogin', 'false');
}
}