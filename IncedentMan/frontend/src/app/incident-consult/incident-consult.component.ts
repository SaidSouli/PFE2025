import { Component, OnInit } from '@angular/core';
import { Incident } from '../../../model/incident.model';
import { IncidentService } from '../services/incident.service';
import { SolutionService } from '../services/solution.service'; // Importez le service de solution
import { CommonModule, NgFor, NgIf } from '@angular/common';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Solution } from '../../../model/solution.model'; // Assurez-vous d'avoir un modèle pour la solution
import { TechnicianService } from '../services/technician.service';

@Component({
  selector: 'incident-consult',
  imports: [NgIf, NgFor, ReactiveFormsModule, RouterLink, FormsModule,CommonModule],
  templateUrl: './incident-consult.component.html',
  styleUrls: ['./incident-consult.component.scss'],
})
export class IncidentConsultComponent implements OnInit {
  incidents: Incident[] = [];
  filteredIncidents: Incident[] = [];
  loading: boolean = true;
  selectedIncident: Incident | null = null;
  editForm: FormGroup;
  error: string | null = null;
  selectedStatus: string = '';
  solution: Solution | null = null; // Pour stocker la solution
  showSolutionFormFlag: boolean = false; // Nouvelle variable pour gérer l'affichage du formulaire de solution

  constructor(
    private incidentService: IncidentService,
    private solutionService: SolutionService,
    private technicianService:TechnicianService, // Injectez le service de solution
    private fb: FormBuilder
  ) {
    this.editForm = this.fb.group({
      title: [''],
      description: [''],
      category: [''],
      status: [''],
      priority: [''],
    });
  }

  ngOnInit(): void {
    const username = localStorage.getItem('username');
    if (username) {
      this.incidentService.getIncidentsByReporterUsername(username).subscribe(
        (data) => {
          this.incidents = data;
          this.filteredIncidents = data;
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
          this.incidents = this.incidents.filter((inc) => inc.id !== id);
          this.filteredIncidents = this.filteredIncidents.filter((inc) => inc.id !== id);
        },
        error: (err) => {
          this.error = 'Erreur lors de la suppression';
        },
      });
    }
  }

  onEdit(incident: Incident) {
    this.selectedIncident = incident;
    this.editForm.patchValue(incident);
    this.showSolutionFormFlag = false; 
  }

  onSubmit() {
    if (this.selectedIncident) {
      this.incidentService.updateIncident(this.selectedIncident.id!, this.editForm.value).subscribe(
        (response) => {
          const index = this.incidents.findIndex((i) => i.id === this.selectedIncident!.id);
          if (index !== -1) {
            this.incidents[index] = { ...this.incidents[index], ...this.editForm.value };
            this.filteredIncidents[index] = { ...this.filteredIncidents[index], ...this.editForm.value };
          }
          this.selectedIncident = null;
        },
        (error) => {
          this.error = 'Error updating incident';
          console.error('Error updating incident', error);
        }
      );
    }
  }

  filterByStatus(status: string): void {
    this.selectedStatus = status;
    this.filteredIncidents = this.incidents.filter((incident) => incident.status === status);
  }

  resetFilter(): void {
    this.selectedStatus = '';
    this.filteredIncidents = this.incidents;
  }

  onStatusChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    const selectedValue = selectElement.value;
    this.filterByStatus(selectedValue);
  }

  // Méthode pour afficher le formulaire de solution
   // Méthode pour afficher le formulaire de solution
   showSolutionForm(incident: Incident): void {
    this.selectedIncident = {...incident};
    this.solution = null; // Réinitialiser la solution
    this.showSolutionFormFlag = true; // Afficher le formulaire de solution

    // Récupérer la solution pour l'incident sélectionné
    this.solutionService.getSolutionByIncidentId(incident.id!).subscribe(
      (data: Solution) => {
        this.solution = data; // Stocker la solution récupérée
      },
      (error) => {
        console.error('Erreur lors de la récupération de la solution', error);
        this.error = 'Erreur lors de la récupération de la solution';
      }
    );
  }

  // Méthode pour accepter la solution
  acceptSolution(): void {
    if (this.selectedIncident) {
      this.selectedIncident.status = 'Resolved'; // Mettre à jour le statut
      this.selectedIncident.resolutionDate = new Date().toISOString(); // Ajouter la date de résolution
      this.incidentService.updateIncident(this.selectedIncident.id!, this.selectedIncident).subscribe(
        (response) => {
          const index = this.incidents.findIndex((i) => i.id === this.selectedIncident!.id);
          if (index !== -1) {
            this.incidents[index] = { ...this.incidents[index], ...this.selectedIncident };
            this.filteredIncidents[index] = { ...this.filteredIncidents[index], ...this.selectedIncident };
          }
          this.selectedIncident = null; // Réinitialiser l'incident sélectionné
          this.solution = null; // Réinitialiser la solution
          this.showSolutionFormFlag = false; // Masquer le formulaire de solution
        },
        (error) => {
          this.error = 'Erreur lors de l\'acceptation de la solution';
          console.error('Error accepting solution', error);
        }
      );
    }
  }

  // Méthode pour refuser la solution

  rejectSolution(): void {
    if (!this.selectedIncident || !this.selectedIncident.id) {
      console.error('No incident selected or incident ID is missing');
      return;
    }
    
    // First get the technician assigned to this incident
    this.technicianService.getAssignedTechnicianForIncident(this.selectedIncident.id)
      .subscribe({
        next: (technicianData) => {
          const technicianId = technicianData.id;
          if (!technicianId) {
            this.showNotification('Error: No technician ID found', 'error');
            return;
          }
          
          // Now update the incident status
          this.technicianService.updateIncidentStatus(technicianId, this.selectedIncident!.id!, 'notResolved')
            .subscribe({
              next: (response) => {
                // Update your UI and close the modal
                const index = this.incidents.findIndex(inc => inc.id === this.selectedIncident!.id);
                if (index !== -1) {
                  this.incidents[index].status = 'Open';
                }
                
                // Update filtered incidents if necessary
                if (this.selectedStatus) {
                  this.filteredIncidents = this.incidents.filter(inc => 
                    inc.status === this.selectedStatus
                  );
                }
                
                this.closeModal();
                this.showNotification('Solution rejected. Incident re-opened.');
              },
              error: (err) => {
                console.error('Error updating status:', err);
                this.showNotification('Failed to update incident status', 'error');
              }
            });
        },
        error: (error) => {
          console.error('Error fetching technician:', error);
          this.showNotification('Failed to get assigned technician', 'error');
        }
      });
  }
  
  // Helper method for notifications (implement based on your UI framework)
  private showNotification(message: string, type: string = 'success'): void {
    // Implementation depends on your notification system
    // For example, using a service or component
  }
    

  // Méthode pour annuler l'affichage du formulaire de solution
  cancelSolution(): void {
    this.selectedIncident = null; // Réinitialiser l'incident sélectionné
    this.solution = null; // Réinitialiser la solution
    this.showSolutionFormFlag = false; // Masquer le formulaire de solution
  }

  // Méthode pour fermer le modal
  closeModal(): void {
    this.selectedIncident = null; // Fermer la modale
    this.solution = null; // Réinitialiser la solution
    this.showSolutionFormFlag = false; // Masquer le formulaire de solution
  }
}