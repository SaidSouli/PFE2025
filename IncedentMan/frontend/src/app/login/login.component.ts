import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../services/auth-service.service';

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

  constructor(private authService: AuthService) {}

  onSubmit() {
    // Trim whitespace from username and password
    const trimmedUsername = this.username.trim();
    const trimmedPassword = this.password.trim();
    
    this.authService.login(trimmedUsername, trimmedPassword);
  }
}