import { Injectable } from "@angular/core";
import { environment } from "../../enviroments/enviroment";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";


@Injectable({
    providedIn:'root'
})
export class UserService {
    private apiUrl = `${environment.apiUrl}/api/users`
    
    constructor(private http:HttpClient){}
    
    getUserById(id:string): Observable<any>{
        return this.http.get(`${this.apiUrl}/${id}`)

    }
    updateUser(id:string,userData:any):Observable<any>{
        return this.http.put(`${this.apiUrl}/${id}`,userData)
    }
    setUserPassword(username: string, password: string): Observable<any> {
        return this.http.put(`${this.apiUrl}/${username}/password`, { password: password });
      }

}