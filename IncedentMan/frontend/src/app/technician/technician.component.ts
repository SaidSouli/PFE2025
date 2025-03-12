import { Component, OnInit } from '@angular/core';
import { NgFor, NgClass, NgIf, SlicePipe } from '@angular/common';
import { Incident } from '../../../model/incident.model';
import { Specialization } from '../../../model/specialization.model';
import { TechnicianService } from '../services/technician-service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-technicien',
  templateUrl: './technician.component.html',
  styleUrls: ['./technician.component.scss'],
  imports: [NgFor, NgClass, NgIf, SlicePipe],
  standalone: true
})
export class TechnicianComponent implements OnInit {
  incidents: Incident[] = [];
  specializations: Specialization[] = [];
  username = '';
  expandedIncidents: Map<string, boolean> = new Map();

  constructor(
    private technicianService: TechnicianService,
    private router: Router
  ) {}

  ngOnInit(): void {
    const username = localStorage.getItem('username');
    console.log('Retrieved username:', username);
    if (username) {
      this.fetchTechnicianSpecializations(username);
    } else {
      console.error('Username not found in local storage');
    }
  }

  toggleExpanded(incident: Incident): void {
    const incidentId = incident.id!;
    this.expandedIncidents.set(incidentId, !this.isExpanded(incident));
  }

  isExpanded(incident: Incident): boolean {
    return this.expandedIncidents.get(incident.id!) === true;
  }

  fetchTechnicianSpecializations(username: string): void {
    this.technicianService.getTechnicianSpecializations(username).subscribe(
      (data) => {
        this.specializations = data;
        this.fetchIncidents(this.specializations.map(spec => spec.toString()));
      },
      (error) => {
        console.error('Error fetching specializations', error);
      }
    );
  }

  fetchIncidents(specializations: string[]): void {
    this.technicianService.getIncidentsBySpecialization(specializations).subscribe(
      (data) => {
        this.incidents = data;
      },
      (error) => {
        console.error('Error fetching incidents', error);
      }
    );
  }

  takeCharge(IncidentId: string): void {
    const username = localStorage.getItem('username');
    if (!username) {
      console.error('username not found in the local storage');
      return;
    }
    this.technicianService.takeChargeIncident(IncidentId, username).subscribe(
      () => {
        const incident = this.incidents.find(inc => inc.id === IncidentId);
        if (incident) {
          incident.status = 'in progress';
          incident.assignedTechnician = { username: username } as any;
        }
        this.fetchIncidents(this.specializations.map(spec => spec.toString()));
        alert('Incident successfully taken in charge');
      },
      (error) => {
        console.error('Error taking charge of incident ', error);
        alert('Failed to take charge of incident: ' + (error.message || 'unknown error'));
      }
    );
  }

  get openIncidents() {
    return this.incidents.filter(incident => incident.status === 'Open');
  }

  goToAssignedIncidents() {
    this.router.navigate(['/assigned-incidents']);
  }

  logout() {
    this.router.navigate(['/login']);
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username');
  }

  getPriorityLabel(priority?: number): string {
    if (!priority) return 'Not Assigned';
    switch (priority) {
      case 1: return 'Low';
      case 2: return 'Medium';
      case 3: return 'High';
      case 4: return 'Critical'
      default: return 'Unknown';
    }
  }
}
