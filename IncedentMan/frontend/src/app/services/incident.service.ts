import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Incident } from '../../../model/incident.model';
import { environment } from '../../enviroments/enviroment';

@Injectable({
  providedIn: 'root'
})
export class IncidentService {
  private apiUrl = `${environment.apiUrl}/api/incidents`;

  constructor(private http: HttpClient) {}

  createIncident(incident: Incident): Observable<Incident> {
    return this.http.post<Incident>(this.apiUrl, incident);
  }
  getIncidentsByTechnician(username: string): Observable<Incident[]> {
    return this.http.get<Incident[]>(`${this.apiUrl}/assigned/${username}`);
  }
  getIncidentsByReporterUsername(username: string): Observable<Incident[]> {
    return this.http.get<Incident[]>(`${this.apiUrl}/reporter/${username}`);
  }
  deleteIncident(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  updateIncident(id: string, incident: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, incident);
  }
}