import { Incident } from "./incident.model";
import { Specialization } from "./specialization.model";
import { User } from "./user.model";
export interface Technician extends User {
    specializations: Specialization[];
    assignedIncidents: Incident[];
  }