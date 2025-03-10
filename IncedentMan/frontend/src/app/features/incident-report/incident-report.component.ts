import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-incident-report',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterLink],
    templateUrl: 'incident-report.component.html',
    styleUrl: 'incident-report.component.scss'
})
export class IncidentReportComponent {
    incidentForm: FormGroup;
    isSubmitting = false;
    submitSuccess = false;
    errorMessage = '';

    // For AI predictions
    aiPrediction: { category: string, priority: number } | null = null;
    showCategoryPrediction = false;
    showPriorityPrediction = false;

    // Options for dropdown selections
    categoryOptions = ['HARDWARE', 'SOFTWARE', 'NETWORK', 'SECURITY', 'GENERAL'];

    // Map numeric priority to display strings and vice versa
    priorityOptions = [
        { value: 1, label: 'Low' },
        { value: 2, label: 'Medium' },
        { value: 3, label: 'High' },
        { value: 4, label: 'Critical' }
    ];

    priorityMap: {[key: number]: string} = {
        1: 'Low',
        2: 'Medium',
        3: 'High',
        4: 'Critical'
    };

    priorityValueMap: {[key: string]: number} = {
        'Low': 1,
        'Medium': 2,
        'High': 3,
        'Critical': 4
    };

    constructor(
        private fb: FormBuilder,
        private http: HttpClient
    ) {
        this.incidentForm = this.fb.group({
            title: ['', Validators.required],
            description: ['', Validators.required],
            category: ['', Validators.required],
            priority: ['', Validators.required]
        });

        // Listen for changes to description to trigger AI prediction
        this.incidentForm.get('description')?.valueChanges.subscribe(() => this.getPrediction());

        // Listen for user selection changes to compare with AI prediction
        this.incidentForm.get('category')?.valueChanges.subscribe(value => {
            if (this.aiPrediction && value !== this.aiPrediction.category) {
                this.showCategoryPrediction = true;
            } else {
                this.showCategoryPrediction = false;
            }
        });

        this.incidentForm.get('priority')?.valueChanges.subscribe(value => {
            const numericValue = this.priorityValueMap[value];
            if (this.aiPrediction && numericValue !== this.aiPrediction.priority) {
                this.showPriorityPrediction = true;
            } else {
                this.showPriorityPrediction = false;
            }
        });
    }

    isFieldInvalid(fieldName: string): boolean {
        const field = this.incidentForm.get(fieldName);
        return field ? field.invalid && (field.dirty || field.touched) : false;
    }

    getPrediction() {
        // Only get prediction if description has meaningful content
        const description = this.incidentForm.get('description')?.value;

        if (description && description.length > 10) {
            this.http.post<any>('http://localhost:5000/predict', {
                description
            }).subscribe({
                next: (response) => {
                    if (response && response.prediction) {
                        this.aiPrediction = {
                            category: response.prediction.category,
                            priority: response.prediction.priority
                        };

                        // Check if user has already made selections different from AI prediction
                        const currentCategory = this.incidentForm.get('category')?.value;
                        const currentPriority = this.incidentForm.get('priority')?.value;
                        const numericPriority = this.priorityValueMap[currentPriority];

                        if (currentCategory && currentCategory !== this.aiPrediction.category) {
                            this.showCategoryPrediction = true;
                        }

                        if (currentPriority && numericPriority !== this.aiPrediction.priority) {
                            this.showPriorityPrediction = true;
                        }
                    }
                },
                error: () => {
                    this.aiPrediction = null;
                    this.showCategoryPrediction = false;
                    this.showPriorityPrediction = false;
                }
            });
        }
    }

    useAiCategory() {
        if (this.aiPrediction) {
            this.incidentForm.get('category')?.setValue(this.aiPrediction.category);
            this.showCategoryPrediction = false;
        }
    }

    useAiPriority() {
        if (this.aiPrediction) {
            this.incidentForm.get('priority')?.setValue(this.priorityMap[this.aiPrediction.priority]);
            this.showPriorityPrediction = false;
        }
    }

    getPriorityDisplay(): string {
        if (this.aiPrediction && this.aiPrediction.priority) {
            return this.priorityMap[this.aiPrediction.priority];
        }
        return '';
    }

    onSubmit() {
        if (this.incidentForm.invalid || this.isSubmitting) {
            return;
        }

        this.isSubmitting = true;
        this.submitSuccess = false;
        this.errorMessage = '';

        const formValues = this.incidentForm.value;
        const username = localStorage.getItem('username') || 'anonymous'; // Get username with fallback

        const incident = {
            title: formValues.title,
            description: formValues.description,
            category: formValues.category,
            priority: this.priorityValueMap[formValues.priority],
            status: 'Open',
            creationDate: new Date(),
            reporter: { username }
        };

        this.http.post('http://localhost:8080/api/incidents', incident)
            .subscribe({
                next: (response) => {
                    this.submitSuccess = true;
                    this.incidentForm.reset();
                    this.isSubmitting = false;
                    this.aiPrediction = null;
                    this.showCategoryPrediction = false;
                    this.showPriorityPrediction = false;
                },
                error: (error) => {
                    this.errorMessage = 'Failed to submit incident report. Please try again.';
                    this.isSubmitting = false;
                }
            });
    }
}