import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { User } from '../../../model/user.model';
import { Technician } from '../../../model/technician.model';
import { Specialization } from '../../../model/specialization.model';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatChipsModule } from '@angular/material/chips';
import { MatCardModule } from '@angular/material/card';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';

interface SpecializationOption {
  value: Specialization;
  label: string;
  icon: string;
  color: string;
}

@Component({
  selector: 'app-edit-user',
  standalone: true,
  imports: [
    CommonModule, 
    FormsModule, 
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatIconModule,
    MatButtonModule,
    MatCardModule,
    ReactiveFormsModule,
    RouterModule,
    MatTooltipModule
  ],
  templateUrl: './edit-user.component.html',
  styleUrls: ['./edit-user.component.scss']
})
export class EditUserComponent implements OnInit {
  userId: string | null = null;
  editForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;
  selectedSpecializations: Specialization[] = [];
  showSpecHint = true;
  
  specializationOptions: SpecializationOption[] = [
    { value: Specialization.NETWORK, label: 'Network', icon: 'router', color: 'blue' },
    { value: Specialization.HARDWARE, label: 'Hardware', icon: 'memory', color: 'red' },
    { value: Specialization.SOFTWARE, label: 'Software', icon: 'code', color: 'green' },
    { value: Specialization.DATABASE, label: 'Database', icon: 'storage', color: 'orange' },
    { value: Specialization.SECURITY, label: 'Security', icon: 'security', color: 'purple' },
    { value: Specialization.CLOUD, label: 'Cloud', icon: 'cloud', color: 'teal' }
  ];

  constructor(
    private route: ActivatedRoute,
    public router: Router, // Changed to public for template access
    private http: HttpClient,
    private formBuilder: FormBuilder
  ) {
    this.editForm = this.formBuilder.group({
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      role: ['', Validators.required],
      specializations: [[], this.validateSpecializations.bind(this)]
    });

    // Subscribe to role changes to add/remove specialization validation
    this.editForm.get('role')?.valueChanges.subscribe(role => {
      const roleValue = role?.toString().toLowerCase() || '';
      if (roleValue === 'technician') {
        this.editForm.get('specializations')?.setValidators([Validators.required, this.validateSpecializations.bind(this)]);
      } else {
        this.editForm.get('specializations')?.clearValidators();
        this.selectedSpecializations = [];
      }
      this.editForm.get('specializations')?.updateValueAndValidity();
    });
  }

  ngOnInit(): void {
    this.userId = this.route.snapshot.paramMap.get('id');
    if (this.userId) {
      this.loadUserDetails(this.userId);
    } else {
      console.error('User ID not found in route parameters.');
      this.errorMessage = 'User ID not found. Redirecting back to admin page.';
      setTimeout(() => {
        this.router.navigate(['/admin']);
      }, 2000);
    }
  }

  loadUserDetails(userId: string): void {
    this.http.get<User | Technician>(`http://localhost:8080/api/users/${userId}`).subscribe({
      next: (user) => {
        this.editForm.patchValue({
          username: user.username,
          email: user.email,
          role: user.role
        });
        
        // Handle specializations if user is a technician
        const userRole = user.role?.toString().toLowerCase() || '';
        if (userRole === 'technician') {
          const techUser = user as Technician;
          if (techUser.specializations && Array.isArray(techUser.specializations)) {
            this.selectedSpecializations = techUser.specializations;
            this.editForm.patchValue({ specializations: this.selectedSpecializations });
            this.showSpecHint = this.selectedSpecializations.length === 0;
          }
        }
      },
      error: (error) => {
        console.error('Error loading user details', error);
        this.errorMessage = 'Error loading user details. Please try again.';
      }
    });
  }

  onSubmit(): void {
    if (this.editForm.valid && this.userId) {
      const updatedUser = { ...this.editForm.value,
        assignedIncidents: this.selectedSpecializations.length > 0 ? [] : undefined
       };
      
      const roleValue = updatedUser.role?.toString().toLowerCase() || '';
      if (roleValue === 'technician') {
        updatedUser.specializations = this.selectedSpecializations.map(spec => spec.toString());
        updatedUser.assignedIncidents = [];
      } else {
        delete updatedUser.specializations;
        delete updatedUser.assignedIncidents;
      }

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
      this.markFormGroupTouched(this.editForm);
      this.errorMessage = 'Please fill in all required fields correctly.';
    }
  }

  // Helper method to mark all controls as touched
  markFormGroupTouched(formGroup: FormGroup) {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  cancelEdit(): void {
    this.router.navigate(['/admin']);
  }

  
  isSpecSelected(spec: Specialization): boolean {
    return this.selectedSpecializations.includes(spec);
  }

  toggleSpecialization(spec: Specialization, selected: boolean): void {
    if (selected && !this.isSpecSelected(spec)) {
      this.selectedSpecializations.push(spec);
    } else if (!selected && this.isSpecSelected(spec)) {
      this.selectedSpecializations = this.selectedSpecializations.filter(s => s !== spec);
    }
    
    this.editForm.patchValue({ specializations: this.selectedSpecializations });
    this.editForm.get('specializations')?.markAsDirty();
    this.editForm.get('specializations')?.markAsTouched();
    this.showSpecHint = this.selectedSpecializations.length === 0;
  }

  validateSpecializations(control: any) {
    const role = this.editForm?.get('role')?.value;
    
    if (role && role.toString().toLowerCase() === 'technician') {
      const specializations = control.value;
      if (!specializations || specializations.length === 0) {
        return { required: true };
      }
    }
    
    return null;
  }
}