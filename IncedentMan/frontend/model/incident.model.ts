export interface Incident {
  id?: string;
  title: string;
  description: string;
  category: string;
  status?: string;
  priority?: number;
  creationDate?: Date;
  reporter?: any;
  assignedTechnician?: any;
}