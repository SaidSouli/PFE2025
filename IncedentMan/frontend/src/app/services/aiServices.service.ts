// ai-suggestion.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../enviroments/enviroment';

@Injectable({
  providedIn: 'root'
})
export class AiSuggestionService {
  private apiUrl = environment.AIapiUrl; // Add this to your environment file

  constructor(private http: HttpClient) {}

  getSolutionSuggestion(incident: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/suggest-solution`, incident);
  }
}