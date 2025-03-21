import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../services/users.service';
import { AuthService } from '../services/auth-service.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { RouterModule } from '@angular/router';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-set-password',
  templateUrl: './set-password.component.html',
  styleUrls: ['./set-password.component.scss'],
  imports: [
      CommonModule, RouterModule,ReactiveFormsModule,
          FormsModule,
      MatFormFieldModule, MatInputModule, MatSelectModule,
      MatButtonModule, MatIconModule, MatCardModule,
      MatChipsModule, MatTooltipModule, MatTableModule,MatProgressSpinnerModule
    ]
})
export class SetPasswordComponent implements OnInit {
  passwordForm: FormGroup;
  currentUser: any;
  hideCurrentPassword = true;
  hideNewPassword = true;
  hideConfirmPassword = true;
  isLoading = false;
  isFirstLogin = false;

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private authService: AuthService,
    private snackBar: MatSnackBar
  ) {
    this.passwordForm = this.fb.group({
      currentPassword: ['', [Validators.required]],
      newPassword: ['', [Validators.required, Validators.minLength(8)]],
      confirmPassword: ['', Validators.required]
    }, { validator: this.checkPasswords });
  }

  ngOnInit(): void {
    this.currentUser = this.authService.getCurrentUser();
    this.isFirstLogin = this.authService.isFirstLogin();
    if (this.isFirstLogin) {
      
      this.passwordForm.get('currentPassword')?.clearValidators();
      this.passwordForm.get('currentPassword')?.updateValueAndValidity();
    }
  }

  // Custom validator to check if passwords match
  checkPasswords(group: FormGroup) {
    const newPass = group.get('newPassword')?.value;
    const confirmPass = group.get('confirmPassword')?.value;
    
    return newPass === confirmPass ? null : { notMatching: true };
  }

  onSubmit(): void {
    if (this.passwordForm.valid) {
      this.isLoading = true;
      const newPassword = this.passwordForm.get('newPassword')?.value;
      
      // Get the username from localStorage if currentUser is null
      const username = this.currentUser?.username || localStorage.getItem('username');
      
      if (!username) {
        this.isLoading = false;
        this.snackBar.open('User information not found. Please log in again.', 'Close', { duration: 5000 });
        this.authService.logout();
        return;
      }
      
      this.userService.setUserPassword(username, newPassword)
        .subscribe({
          next: (response) => {
            this.isLoading = false;
            this.snackBar.open('Password updated successfully', 'Close', { duration: 3000 });
            this.passwordForm.reset();
            
            // Clear first login flag and redirect to appropriate page
            this.authService.clearFirstLoginFlag();
            const role = localStorage.getItem('role') || 'user';
            this.authService.redirectBasedOnRole(role);
          },
          error: (error) => {
            this.isLoading = false;
            this.snackBar.open('Failed to update password: ' + error.message, 'Close', { duration: 5000 });
          }
        });
    } else {
      this.markFormGroupTouched(this.passwordForm);
    }
  }

  // Utility function to mark all controls as touched
  markFormGroupTouched(formGroup: FormGroup) {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  // Get form control for easier access in template
  get f() {
    return this.passwordForm.controls;
  }
}