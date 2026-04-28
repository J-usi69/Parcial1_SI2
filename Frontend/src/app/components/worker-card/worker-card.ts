import { Component, Input } from '@angular/core';

export interface WorkerData {
  nombre: string;
  especialidad: string;
  isOnline: boolean;
  fotoUrl: string;
}

@Component({
  selector: 'app-worker-card',
  standalone: true, // Asegúrate de marcarlo como standalone si usas Angular 17+
  templateUrl: './worker-card.html',
  styleUrl: './worker-card.css',
})
export class WorkerCard {
  @Input({ required: true }) data!: WorkerData;
}
