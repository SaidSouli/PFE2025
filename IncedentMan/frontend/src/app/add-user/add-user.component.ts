import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Specialization } from '../../../model/specialization.model';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatChipsModule } from '@angular/material/chips';
import { MatTooltipModule } from '@angular/material/tooltip';

@Component({
  selector: 'app-add-user',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatButtonModule,
    MatIconModule,
    MatCardModule,
    MatChipsModule,
    MatTooltipModule
  ],
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.scss']
})
export class AddUserComponent {
  userForm: FormGroup;
  selectedSpecializations: Specialization[] = [];
  hidePassword = true;
  showSpecHint = false;
  
  
  specializationOptions = [
    { value: Specialization.NETWORK, label: 'Network', icon: 'router', color: 'network' },
    { value: Specialization.HARDWARE, label: 'Hardware', icon: 'memory', color: 'hardware' },
    { value: Specialization.SOFTWARE, label: 'Software', icon: 'code', color: 'software' },
    { value: Specialization.DATABASE, label: 'Database', icon: 'storage', color: 'database' },
    { value: Specialization.SECURITY, label: 'Security', icon: 'security', color: 'security' },
    { value: Specialization.CLOUD, label: 'Cloud', icon: 'cloud', color: 'cloud' }
  ];

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    public router: Router,
    private snackBar: MatSnackBar
  ) {
    this.userForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      email: ['', [Validators.required, Validators.email]],
      role: ['', Validators.required],
      specializations: [[], this.conditionalValidator(() => 
        this.userForm?.get('role')?.value === 'technician', 
        Validators.required
      )]
    });
    
    
    this.userForm.get('role')?.valueChanges.subscribe(role => {
      this.userForm.get('specializations')?.updateValueAndValidity();
      
      
      if (role !== 'technician') {
        this.selectedSpecializations = [];
      } else {
        
        setTimeout(() => {
          this.showSpecHint = true;
        }, 300);
      }
    });
  }

  
  conditionalValidator(condition: () => boolean, validator: any) {
    return (control: any) => {
      if (!condition()) {
        return null;
      }
      return validator(control);
    };
  }

  
  isSpecSelected(spec: Specialization): boolean {
    return this.selectedSpecializations.includes(spec);
  }

  
  toggleSpecialization(spec: Specialization, selected: boolean): void {
    if (selected) {
      if (!this.selectedSpecializations.includes(spec)) {
        this.selectedSpecializations.push(spec);
      }
    } else {
      this.selectedSpecializations = this.selectedSpecializations.filter(s => s !== spec);
    }
    
    
    this.userForm.get('specializations')?.setValue(this.selectedSpecializations);
  }

  
  getSpecIcon(spec: Specialization): string {
    const option = this.specializationOptions.find(opt => opt.value === spec);
    return option ? option.icon : 'engineering';
  }
  
  
  getSpecColor(spec: Specialization): string {
    const option = this.specializationOptions.find(opt => opt.value === spec);
    return option ? option.color : '';
  }
  
  
  getSpecLabel(spec: Specialization): string {
    const option = this.specializationOptions.find(opt => opt.value === spec);
    return option ? option.label : String(spec);
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

      Object.keys(payload).forEach(key => payload[key] === undefined && delete payload[key]);

      this.http.post<any>('http://localhost:8080/api/users', payload)
        .subscribe({
          next: () => {
            this.router.navigate(['/admin']);
            this.snackBar.open('User created successfully!', 'Close', {
              duration: 3000,
              horizontalPosition: 'end',
              verticalPosition: 'top'
            });
          },
          error: (error) => {
            console.error('Error creating user:', error);
            this.snackBar.open(`Error: ${error.error?.error || 'Unknown error'}`, 'Close', {
              duration: 5000,
              horizontalPosition: 'end',
              verticalPosition: 'top'
            });
          }
        });
    }
  }

  getErrorMessage(controlName: string): string {
    const control = this.userForm.get(controlName);
    if (control?.hasError('required')) {
      return `${controlName.charAt(0).toUpperCase() + controlName.slice(1)} is required`;
    }
    if (control?.hasError('email')) {
      return 'Invalid email format';
    }
    if (control?.hasError('minlength')) {
      if (controlName === 'password') {
        return 'Password must be at least 6 characters';
      }
      if (controlName === 'username') {
        return 'Username must be at least 3 characters';
      }
      return `${controlName} does not meet minimum length requirements`;
    }
    return '';
  }
}