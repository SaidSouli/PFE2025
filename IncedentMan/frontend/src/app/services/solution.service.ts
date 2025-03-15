// solution.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Solution } from '../../../model/solution.model';
import { environment } from '../../enviroments/enviroment';

@Injectable({
  providedIn: 'root'
})
export class SolutionService {
  private apiUrl = `${environment.apiUrl}/api/solutions`;

  constructor(private http: HttpClient) {}

  createSolution(solution: Solution): Observable<Solution> {
    return this.http.post<Solution>(this.apiUrl, solution);
  }

  getSolutionByIncidentId(incidentId: string): Observable<Solution> {
    return this.http.get<Solution>(`${this.apiUrl}/incident/${incidentId}`);
  }
  deletesolution(solutionId:String):Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${solutionId}`)
  }

}