import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { AdminComponent } from './admin/admin.component';
import { EditUserComponent } from './edit-user/edit-user.component';
import { AddUserComponent } from './add-user/add-user.component';
import { IncidentReportComponent } from './features/incident-report/incident-report.component';
import { TechnicianComponent } from './technician/technician.component';
import { AssignedIncidentsComponent } from './assigned-incidents/assigned-incidents.component';
import { IncidentConsultComponent } from './incident-consult/incident-consult.component';
import { SetPasswordComponent } from './set-password/set-password.component';
import { WaitingIncidentsComponent } from './waiting-incidents/waiting-incidents.component';

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'login', component: LoginComponent },
  {path : 'admin',component:AdminComponent},
  {path: 'edit-user/:id', component: EditUserComponent},
  { path: 'add-user', component: AddUserComponent },
  {path: 'report-incident', component:IncidentReportComponent },
  {path: 'technician', component:TechnicianComponent },
  {path:'assigned-incidents',component:AssignedIncidentsComponent},
  {path:'incident-consult',component:IncidentConsultComponent},
  {path:'set-password',component : SetPasswordComponent},
  {path:'waiting-incidents',component:WaitingIncidentsComponent}
];