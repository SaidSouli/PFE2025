import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-incident-report',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: 'incident-report.component.html',
  styleUrl:'incident-report.component.scss'

})
export class IncidentReportComponent {
  incidentForm: FormGroup;
  isSubmitting = false;
  submitSuccess = false;
  errorMessage = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient
  ) {
    this.incidentForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required]
    });
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.incidentForm.get(fieldName);
    return field ? field.invalid && (field.dirty || field.touched) : false;
  }

  onSubmit() {
    if (this.incidentForm.invalid || this.isSubmitting) {
      return;
    }

    this.isSubmitting = true;
    this.submitSuccess = false;
    this.errorMessage = '';

    const incident = {
      ...this.incidentForm.value,
      status: 'Open',
      creationDate: new Date()
      
    };

    this.http.post('http://localhost:8080/api/incidents', incident)
      .subscribe({
        next: (response) => {
          this.submitSuccess = true;
          this.incidentForm.reset();
          this.isSubmitting = false;
        },
        error: (error) => {
          this.errorMessage = 'Failed to submit incident report. Please try again.';
          this.isSubmitting = false;
        }
      });
  }
}