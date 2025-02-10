import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { User } from '../../../model/user.model'; // Adjust path if needed
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit-user',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './edit-user.component.html',
  styleUrls: ['./edit-user.component.scss']
})
export class EditUserComponent implements OnInit {
  userId: string | null = null;
  editForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
    private formBuilder: FormBuilder
  ) {
    this.editForm = this.formBuilder.group({ // Initialize the form in the constructor
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      role: ['', Validators.required]
      // Password is intentionally NOT included in edit form for security best practices.
      // Consider a separate "change password" feature if needed.
    });
  }

  ngOnInit(): void {
    this.userId = this.route.snapshot.paramMap.get('id');
    if (this.userId) {
      this.loadUserDetails(this.userId);
    } else {
      console.error('User ID not found in route parameters.');
      // Handle error - maybe redirect back to admin page
    }
  }

  loadUserDetails(userId: string): void {
    this.http.get<User>(`http://localhost:8080/api/users/${userId}`).subscribe({
      next: (user) => {
        this.editForm.patchValue(user); // Fill the form with user details
      },
      error: (error) => {
        console.error('Error loading user details', error);
        this.errorMessage = 'Error loading user details. Please try again.';
      }
    });
  }

  onSubmit(): void {
    if (this.editForm.valid && this.userId) {
      const updatedUser = this.editForm.value;
      this.http.put<User>(`http://localhost:8080/api/users/${this.userId}`, updatedUser).subscribe({
        next: (updatedUserResponse) => {
          console.log('User updated successfully', updatedUserResponse);
          this.successMessage = 'User updated successfully!';
          this.errorMessage = null;
          // Optionally navigate back to admin page after successful update
          setTimeout(() => { // Small delay for success message to show
            this.router.navigate(['/admin']);
          }, 1500);
        },
        error: (error) => {
          console.error('Error updating user', error);
          this.errorMessage = 'Error updating user. Please check the form and try again.';
          this.successMessage = null;
        }
      });
    } else {
      this.errorMessage = 'Please fill in all required fields correctly.';
    }
  }

  cancelEdit(): void {
    this.router.navigate(['/admin']);
  }
}