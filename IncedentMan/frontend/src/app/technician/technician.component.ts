import { Component, OnInit } from '@angular/core';
import { NgFor } from '@angular/common';
import { Incident } from '../../../model/incident.model';
import { Specialization } from '../../../model/specialization.model';
import { TechnicianService } from '../services/technician-service.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-technicien',
  templateUrl: './technician.component.html',
  styleUrls: ['./technician.component.scss'], // Corrected from styleUrl to styleUrls
  imports : [NgFor]
})
export class TechnicianComponent implements OnInit {
  incidents: Incident[] = [];
  specializations: Specialization[] = [];
  username = '';

  constructor(private technicianService: TechnicianService,private router:Router) {}

  ngOnInit(): void {
    const username = localStorage.getItem('username');
    console.log('Retrieved username:', username);
    if (username) {
      this.fetchTechnicianSpecializations(username);
  } else {
      console.error('Username not found in local storage');
      // Rediriger vers la page de connexion ou afficher un message d'erreur
  }
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
  get openIncidents() {
    return this.incidents.filter(incident => incident.status === 'Open');
  }
  logout() {
    this.router.navigate(['/login']);
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('username')
  }
}