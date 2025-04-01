import { Component, Inject, OnInit, PLATFORM_ID } from '@angular/core';
import { Incident } from '../../../model/incident.model';
import { IncidentService } from '../services/incident.service';
import { SolutionService } from '../services/solution.service'; // Importer le service de solution
import { Router } from '@angular/router';
import { LocalStorageService } from '../services/localstorage.service';
import { ThemeService } from '../services/theme.service';
import { isPlatformBrowser, NgFor, NgIf } from '@angular/common';
import { Solution } from '../../../model/solution.model'; // Importer le modèle de solution
import { animate, style, transition, trigger } from '@angular/animations';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule, MatIconButton } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatDividerModule } from '@angular/material/divider';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';


@Component({
  selector: 'app-waiting-incidents',
  imports: [NgIf, NgFor, MatIconModule, MatButtonModule,MatFormFieldModule, MatInputModule, MatSelectModule,
          MatButtonModule, MatIconModule, MatCardModule,
          MatChipsModule, MatTooltipModule, MatTableModule, MatProgressSpinnerModule,MatDividerModule],
  templateUrl: './waiting-incidents.component.html',
  styleUrls: ['./waiting-incidents.component.scss'], // Corriger le nom de la propriété
  animations: [
    trigger('fadeIn', [
        transition(':enter', [
            style({ opacity: 0, transform: 'translateY(20px)' }),
            animate('0.5s ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
        ])
    ])
]
})
export class WaitingIncidentsComponent implements OnInit {
  incidents: Incident[] = [];
  filteredIncidents: Incident[] = [];
  solutions: { [key: string]: Solution } = {}; // Dictionnaire pour stocker les solutions par incidentId
  username: string | null = null;

  constructor(
    private incidentService: IncidentService,
    private solutionService: SolutionService, // Injecter le service de solution
    private router: Router,
    private lss: LocalStorageService,
    public themeService: ThemeService,
    @Inject(PLATFORM_ID) private platformId: object
  ) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      setTimeout(() => {
        this.username = this.lss.getItem('username');
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
          this.loadSolutions(); // Charger les solutions après avoir filtré les incidents
        },
        (error) => {
          console.error('Error fetching incidents:', error);
        }
      );
    }
  }

  filterIncidents(): void {
    // Filtrer les incidents où le statut est "Waiting"
    this.filteredIncidents = this.incidents.filter(incident => incident.status === 'Waiting');
  }

  loadSolutions(): void {
    this.filteredIncidents.forEach(incident => {
        if (incident.id) { // Vérifiez si l'ID est défini
            this.solutionService.getSolutionByIncidentId(incident.id).subscribe(
                (solution: Solution) => {
                    this.solutions[incident.id!] = solution; // Stocke la solution par incidentId
                },
                (error) => {
                    console.error(`Error fetching solution for incident ${incident.id}:`, error);
                }
            );
        } else {
            console.warn(`Incident ID is undefined for incident:`, incident);
        }
    });
}

modifySolution(incident: Incident): void {
  const solution = this.solutions[incident.id!]; // Récupérer la solution associée à l'incident
  if (!solution || !solution.id) {
    alert("Aucune solution trouvée pour cet incident ou l'ID de la solution est manquant.");
    return;
  }

  const newDescription = prompt("Entrez la nouvelle description de la solution :");
  if (newDescription) {
    this.solutionService.updateSolution(solution.id, newDescription).subscribe(
      (updatedSolution: Solution) => {
        this.solutions[incident.id!] = updatedSolution; // Mettre à jour la solution dans le dictionnaire
        alert("Solution mise à jour avec succès !");
      },
      (error) => {
        console.error(`Erreur lors de la mise à jour de la solution :`, error);
        alert("Erreur lors de la mise à jour de la solution.");
      }
    );
  }
}

deleteSolution(incident: Incident): void {
  const solution = this.solutions[incident.id!]; // Récupérer la solution associée à l'incident
  if (!solution || !solution.id) {
    alert("Aucune solution trouvée pour cet incident ou l'ID de la solution est manquant.");
    return;
  }

  if (confirm("Êtes-vous sûr de vouloir supprimer cette solution ?")) {
    this.solutionService.deletesolution(solution.id).subscribe(
      () => {
        delete this.solutions[incident.id!]; // Supprimer la solution du dictionnaire
        alert("Solution supprimée avec succès !");
        this.loadIncidents(); // Recharger les incidents si nécessaire
      },
      (error) => {
        console.error(`Erreur lors de la suppression de la solution :`, error);
        alert("Erreur lors de la suppression de la solution.");
      }
    );
  }
}
  back(): void {
    this.router.navigate(['/assigned-incidents']);
  }

  logout(): void {
    this.router.navigate(['/login']);
    this.lss.removeItem('jwtToken');
    this.lss.removeItem('username');
  }
  toggleDarkMode(): void {
    this.themeService.toggleDarkMode();
  }

}