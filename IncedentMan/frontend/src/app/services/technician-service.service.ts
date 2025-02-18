import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Specialization } from '../../../model/specialization.model';
import { Incident } from '../../../model/incident.model';
@Injectable({
  providedIn: 'root'
})
export class TechnicianService {
  private apiUrl = 'http://localhost:8080/api/technicians';

  constructor(private http: HttpClient) {}

  getTechnicianSpecializations(username: string): Observable<Specialization[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
    return this.http.get<Specialization[]>(`${this.apiUrl}/${username}/specializations`, { headers });
  }

  getIncidentsBySpecialization(specializations: string[]): Observable<Incident[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
    return this.http.post<Incident[]>(`http://localhost:8080/api/incidents/by-specialization`, { specializations }, { headers });
  }
}