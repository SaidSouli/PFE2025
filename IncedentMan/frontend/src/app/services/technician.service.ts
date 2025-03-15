import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Specialization } from '../../../model/specialization.model';
import { Incident } from '../../../model/incident.model';
import { Technician } from '../../../model/technician.model';
@Injectable({
  providedIn: 'root'
})
export class TechnicianService {
  private apiUrl = 'http://localhost:8080/api/technicians';
  private apiUrl2 = 'http://localhost:8080/api'

  constructor(private http: HttpClient) {}

  getTechnicianSpecializations(username: string): Observable<Specialization[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
    return this.http.get<Specialization[]>(`${this.apiUrl}/${username}/specializations`, { headers });
  }
  getTechnicianByName(name: string): Observable<Technician> {
    return this.http.get<Technician>(`${this.apiUrl}/name/${name}`);
  }
  

  getIncidentsBySpecialization(specializations: string[]): Observable<Incident[]> {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${localStorage.getItem('token')}`);
    return this.http.post<Incident[]>(`http://localhost:8080/api/incidents/by-specialization`, { specializations }, { headers });
  }
    
  
  takeChargeIncident (incidentId: string , username:string): Observable<any>{
    return this.http.put(`${this.apiUrl2}/incidents/${incidentId}/take-charge?username=${username}`,{});
  }
  updateIncidentStatus(technicianId: string, incidentId: string, status: string): Observable<Technician> {
    return this.http.put<Technician>(
      `${this.apiUrl}/${technicianId}/incidents/${incidentId}/status?status=${status}`, 
      {}
    );
  }
  getAssignedTechnicianForIncident(incidentId: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${incidentId}/technician`);
  }
}