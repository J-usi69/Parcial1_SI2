import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonComponent } from '../button/button';

export interface NewRequestData {
  titulo: string;
  tiempo: string;
  severidad: 'Crítico' | 'Alto' | 'Medio';
  vehiculo: string;
  placa: string;
  ubicacion: string;
  distancia: string;
}

@Component({
  selector: 'app-new-request-card',
  standalone: true,
  imports: [CommonModule, ButtonComponent],
  templateUrl: './new-request-card.html',
  styleUrl: './new-request-card.css',
})
export class NewRequestCard {
  @Input({ required: true }) data!: NewRequestData;
}
