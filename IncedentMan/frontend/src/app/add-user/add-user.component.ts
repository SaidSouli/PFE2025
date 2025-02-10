import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { User } from '../../../model/user.model';
import { Specialization } from '../../../model/specialization.model';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-user',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.scss']
})
export class AddUserComponent {
  userForm: FormGroup;
  specializations = Object.values(Specialization);
  selectedSpecializations: Specialization[] = [];

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    public router: Router
  ) {
    
    this.userForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', [Validators.required, Validators.minLength(6)]],
      email: ['', [Validators.required, Validators.email]],
      role: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.userForm.valid) {
      const baseData = this.userForm.value;
      const payload = {
        ...baseData,
        ...(baseData.role === 'technician' && {
          specializations: this.selectedSpecializations
        })
      };
  
      // Remove undefined/null fields
      Object.keys(payload).forEach(key => payload[key] === undefined && delete payload[key]);
  
      this.http.post<any>('http://localhost:8080/api/users', payload)
        .subscribe({
          next: () => {
            this.router.navigate(['/admin']);
            alert('User created successfully!');
          },
          error: (error) => {
            console.error('Error creating user:', error);
            alert(`Error: ${error.error?.error || 'Unknown error'}`);
          }
        });
    }
  }
}