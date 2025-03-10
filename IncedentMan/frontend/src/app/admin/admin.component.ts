import { Component, computed, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { User } from '../../../model/user.model';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatTableModule } from '@angular/material/table';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
  imports: [CommonModule, RouterModule,
    MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatButtonModule,
        MatIconModule,
        MatCardModule,
        MatChipsModule,
        MatTooltipModule,
        MatTableModule

  ] 
})
export class AdminComponent {
  
  users = signal<User[]>([]);
  searchTerm = signal("");
  roles = ['admin','user','technician'];
  filtredUsers = computed(()=> {
    const term = this.searchTerm().toLowerCase();
    const allUsers = this.users();
    if (!term) return allUsers;
    //check exact role
    if (this.roles.includes(term)){
      return allUsers.filter(user => user.role.toLowerCase() === term);
    }
    //search username
    return allUsers.filter(user => user.username.toLowerCase().includes(term) || user.role.toLowerCase().includes(term));
  });
  constructor(private http: HttpClient, public router: Router) {}

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.http.get<User[]>('http://localhost:8080/api/users').subscribe(data => {
      this.users.set(data);
    });
  }
  updateSearch(event : Event):void {
    this.searchTerm.set((event.target as HTMLInputElement).value);
  }
  logout() {
    this.router.navigate(['/login']);
    localStorage.removeItem('jwtToken');
  }
  editUser (user: User): void {
    console.log('AdminComponent - Navigating to edit user with ID:', user.id);
    this.router.navigate(['/edit-user', user.id]);

  }
  deleteUser (userId: string): void {
    if (confirm('do you really wanna delete this user ?')) {
      this.http.delete(`http://localhost:8080/api/users/${userId}`, { responseType: 'text' }).subscribe({ // Add responseType: 'text'
        next: (response) => {
          console.log('Delete successful response (text):', response); // Log the text response
          this.loadUsers();
          alert('User deleted successfully'); 
        },
        error: (error) => {
          console.error('Error deleting user:', error);
          alert('There was an error while deleting the user.');
        }
      });
    }
  }
  
}