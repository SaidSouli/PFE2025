import { Component, OnInit } from '@angular/core';
import { Incident } from '../../../model/incident.model';
import { IncidentService } from '../services/incident.service';
import { NgFor } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-assigned-incidents',
  imports: [NgFor],
  templateUrl: './assigned-incidents.component.html',
  styleUrl: './assigned-incidents.component.scss'
})
export class AssignedIncidentsComponent implements OnInit {
  incidents: Incident[] = [];
  filteredIncidents: Incident[] = [];
  username: string | null = null; // Initialize username as null

  constructor(private incidentService: IncidentService,private router:Router) {}

  ngOnInit(): void {
    this.username = localStorage.getItem('username'); // Get username from local storage
    if (this.username) {
      this.loadIncidents();
    } else {
      console.error('No username found in local storage');
      // Optionally, redirect to login or show a message
    }
  }

  loadIncidents(): void {
    if (this.username) {
      this.incidentService.getIncidentsByTechnician(this.username).subscribe(
        (data: Incident[]) => {
          this.incidents = data;
          this.filterIncidents();
        },
        (error) => {
          console.error('Error fetching incidents:', error);
        }
      );
    }
  }

  filterIncidents(): void {
    this.filteredIncidents = this.incidents.filter(incident => incident.status === 'En cours');
  }
  back(){
    this.router.navigate(['/technician'])
  }
  logout() {
    this.router.navigate(['/login']);
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username')
  }

}