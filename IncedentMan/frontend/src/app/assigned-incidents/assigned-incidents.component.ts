// assigned-incidents.component.ts
import { isPlatformBrowser } from '@angular/common';
import { Component, OnInit ,Inject,PLATFORM_ID, effect} from '@angular/core';
import { Incident } from '../../../model/incident.model';
import { Solution } from '../../../model/solution.model';
import { IncidentService } from '../services/incident.service';
import { SolutionService } from '../services/solution.service';
import { NgFor, NgIf, NgClass } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { LocalStorageService } from '../services/localstorage.service';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { ThemeService } from '../services/theme.service';
@Component({
  selector: 'app-assigned-incidents',
  imports: [NgFor, NgIf, NgClass, FormsModule,MatFormFieldModule, MatInputModule, MatSelectModule,
        MatButtonModule, MatIconModule, MatCardModule,
        MatChipsModule, MatTooltipModule, MatTableModule,MatProgressSpinnerModule,RouterLink
      ],
  templateUrl: './assigned-incidents.component.html',
  styleUrl: './assigned-incidents.component.scss'
})
export class AssignedIncidentsComponent implements OnInit {
  incidents: Incident[] = [];
  filteredIncidents: Incident[] = [];
  username: string | null = null;
  solutionText: { [key: string]: string } = {}; // To store solution text for each incident
  isSubmitting: { [key: string]: boolean } = {}; // Track submission status
  submissionError: { [key: string]: string } = {}; // Track error messages

  constructor(
    private incidentService: IncidentService,
    private solutionService: SolutionService,
    private router: Router,
    public themeService:ThemeService,
    @Inject(PLATFORM_ID) private platformId: object ,
    private lss:LocalStorageService
  ) {

    const savedTheme = localStorage.getItem('theme');
            effect(() => {
              if (this.themeService.getCurrentTheme()) {
                document.body.classList.add('dark-theme');
              } else {
                document.body.classList.remove('dark-theme');
              }
            });
        
  }

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      
      setTimeout(() => {
        this.username = this.lss.getItem('username');
        console.log('Retrieved username after delay:', this.username);
        
        if (this.username) {
          this.loadIncidents();
        } else {
          console.error('No username found in local storage');
          this.router.navigate(['/login']);
        }
      }, 100);
    }
  }

  loadIncidents(): void {
    if (this.username) {
      this.incidentService.getIncidentsByTechnician(this.username).subscribe(
        (data: Incident[]) => {
          this.incidents = data;
          this.filterIncidents();
          
          // Initialize solution text objects for each incident
          this.incidents.forEach(incident => {
            if (incident.id) {
              this.solutionText[incident.id] = '';
              this.isSubmitting[incident.id] = false;
              this.submissionError[incident.id] = '';
            }
          });
        },
        (error) => {
          console.error('Error fetching incidents:', error);
        }
      );
    }
  }

  filterIncidents(): void {
    this.filteredIncidents = this.incidents.filter(incident => incident.status ==='In progress');
  }

  submitSolution(incident: Incident): void {
    if (!incident.id || !this.username) return;
    
    const incidentId = incident.id;
    
    // Validate solution text
    if (!this.solutionText[incidentId] || this.solutionText[incidentId].trim() === '') {
      this.submissionError[incidentId] = 'Please enter a solution description';
      return;
    }
    
    // Set submission status
    this.isSubmitting[incidentId] = true;
    this.submissionError[incidentId] = '';
    
    const solution: Solution = {
      IncidentId: incidentId,
      TechnicianName: this.username,
      description: this.solutionText[incidentId]
    };
    
    this.solutionService.createSolution(solution).subscribe(
      (response) => {
        // Update incident status locally
        incident.status = 'Waiting for approval';
        
        // Clear and reset
        this.solutionText[incidentId] = '';
        this.isSubmitting[incidentId] = false;
        
        // Refresh the incident list
        this.filterIncidents();
      },
      (error) => {
        console.error('Error submitting solution:', error);
        this.isSubmitting[incidentId] = false;
        this.submissionError[incidentId] = 
          error.error && typeof error.error === 'string' 
            ? error.error 
            : 'Failed to submit solution. Please try again.';
      }
    );
  }

  back() {
    this.router.navigate(['/technician']);
  }

  logout() {
    this.router.navigate(['/login']);
    this.lss.removeItem('jwtToken');
    this.lss.removeItem('username');
  }

  getPriorityClass(priority: number | undefined): string {
    if (priority === undefined) return 'priority-medium';
        
    switch(priority) {
      case 1: return 'priority-low';
      case 2: return 'priority-medium';
      case 3: return 'priority-high';
      case 4: return 'priority-Critical';
      default: return 'priority-medium';
    }
  }

  getPriorityLabel(priority: number | undefined): string {
    if (priority === undefined) return 'Medium';
        
    switch(priority) {
      case 1: return 'Low';
      case 2: return 'Medium';
      case 3: return 'High';
      case 4: return 'Critical';
      default: return 'Medium';
    }
  }
  toggleDarkMode(): void {
    this.themeService.toggleDarkMode();
  }
}