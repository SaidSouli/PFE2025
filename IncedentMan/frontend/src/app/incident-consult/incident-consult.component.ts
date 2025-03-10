import { Component, OnInit } from '@angular/core';
import { Incident } from '../../../model/incident.model';
import { IncidentService } from '../services/incident.service';
import { NgFor, NgIf } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'incident-consult',
  imports: [NgIf,NgFor,ReactiveFormsModule,RouterLink],
  templateUrl: 'incident-consult.component.html',
  styleUrl: './incident-consult.component.scss'
})
export class IncidentConsultComponent implements OnInit {
  incidents: Incident[] = [];
  loading: boolean = true;
  selectedIncident: Incident | null = null;
  editForm: FormGroup;
  error: string | null = null;

  constructor(private incidentService: IncidentService , private fb:FormBuilder) {
    this.editForm = this.fb.group({
      title: [''],
      description: [''],
      category: [''],
      status: [''],
      priority: ['']
    });
  }

  ngOnInit(): void {
    const username = localStorage.getItem('username'); // Retrieve the username from local storage
    if (username) {
        this.incidentService.getIncidentsByReporterUsername(username).subscribe(
            (data) => {
                this.incidents = data;
                this.loading = false;
            },
            (error) => {
                this.error = 'Failed to load incidents';
                this.loading = false;
            }
        );
    } else {
        this.error = 'No username found in local storage';
        this.loading = false;
    }
}
onDelete(id: string): void {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet incident ?')) {
    this.incidentService.deleteIncident(id).subscribe({
      next: () => {
        this.incidents = this.incidents.filter(inc => inc.id !== id);
      },
      error: (err) => {
        this.error = 'Erreur lors de la suppression';
      }
    });
  }
}
onEdit(incident: Incident) {
  this.selectedIncident = incident;
  this.editForm.patchValue(incident); // Populate the form with the incident data
}
onSubmit() {
  if (this.selectedIncident) {
    this.incidentService.updateIncident(this.selectedIncident.id!, this.editForm.value).subscribe(
      response => {
        // Update the local incidents array
        const index = this.incidents.findIndex(i => i.id === this.selectedIncident!.id);
        if (index !== -1) {
          this.incidents[index] = { ...this.incidents[index], ...this.editForm.value };
        }
        this.selectedIncident = null; // Reset selected incident
      },
      error => {
        this.error = 'Error updating incident';
        console.error('Error updating incident', error);
      }
    );
  }
}

}