import { User } from "./user.model";
import { Technician } from "./technician.model";
export interface Incident {
    id: string;
    title: string;
    description: string;
    creationDate: Date;
    status: string;
    priority: number;
    category: string;
    reporter: User;
    assignedTechnician: Technician;
  }