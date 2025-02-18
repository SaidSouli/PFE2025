import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-incident-report',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  template: `
    <div class="container mx-auto p-4">
      <h2 class="text-2xl font-bold mb-6">Report an Incident</h2>
      
      <form [formGroup]="incidentForm" (ngSubmit)="onSubmit()" class="max-w-2xl">
        <!-- Title Field -->
        <div class="mb-4">
          <label class="block mb-2">Title</label>
          <input
            type="text"
            formControlName="title"
            class="w-full p-2 border rounded"
            placeholder="Brief title describing the issue"
          >
          <div *ngIf="isFieldInvalid('title')" class="text-red-500 mt-1">
            Title is required
          </div>
        </div>

        <!-- Category Field -->
        <div class="mb-4">
          <label class="block mb-2">Category</label>
          <select
            formControlName="category"
            class="w-full p-2 border rounded"
          >
            <option value="">Select a category</option>
            <option value="NETWORK">Network</option>
            <option value="HARDWARE">Hardware</option>
            <option value="SOFTWARE">Software</option>
            <option value="DATABASE">Database</option>
            <option value="SECURITY">Security</option>
          </select>
          <div *ngIf="isFieldInvalid('category')" class="text-red-500 mt-1">
            Please select a category
          </div>
        </div>
        <div class="mb-4">
  <label class="block mb-2">Priority</label>
  <select formControlName="priority" class="w-full p-2 border rounded">
    <option value="">Select a priority</option>
    <option value="1">Low</option>
    <option value="2">Medium</option>
    <option value="3">High</option>
    <option value="4">Critical</option>
  </select>
  <div *ngIf="isFieldInvalid('priority')" class="text-red-500 mt-1">
    Please select a priority
  </div>
</div>
        <!-- Description Field -->
        <div class="mb-4">
          <label class="block mb-2">Description</label>
          <textarea
            formControlName="description"
            rows="6"
            class="w-full p-2 border rounded"
            placeholder="Detailed description of the issue"
          ></textarea>
          <div *ngIf="isFieldInvalid('description')" class="text-red-500 mt-1">
            Description is required
          </div>
        </div>

        <button
          type="submit"
          [disabled]="incidentForm.invalid || isSubmitting"
          class="w-full bg-blue-500 text-white p-2 rounded"
        >
          {{ isSubmitting ? 'Submitting...' : 'Submit Incident Report' }}
        </button>

        <div *ngIf="submitSuccess" class="mt-4 p-4 bg-green-100 text-green-700 rounded">
          Incident reported successfully!
        </div>

        <div *ngIf="errorMessage" class="mt-4 p-4 bg-red-100 text-red-700 rounded">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  `
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
      // Category and priority will be set by backend AI integration
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