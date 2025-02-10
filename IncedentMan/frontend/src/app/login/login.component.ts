import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  standalone: true,
  imports: [FormsModule]
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  message: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post<any>('http://localhost:8080/api/users/login', {
      username: this.username,
      password: this.password
    }).subscribe({
      next: (response) => {
        console.log('Login successful', response);
        if (response && response.token) { // Check for the token in the response
          // Store the token in local storage
          localStorage.setItem('jwtToken', response.token);

          // Optionally, you can also store the role if needed
          const role = response.role.toLowerCase();
          switch(role) {
            case 'admin':
              this.router.navigate(['/admin']);
              break;
            default:
              this.router.navigate(['/home']); // Redirect to a default route
          }
        } else {
          console.error('No token found in response');
          this.message = 'Login failed: Invalid response';
        }
      },
      error: (error) => {
        this.message = 'Login failed, please check your credentials';
        console.error('Login failed', error);
      }
    });
  }
}