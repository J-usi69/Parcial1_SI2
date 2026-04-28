import { Component, Input } from '@angular/core';
import { ButtonComponent } from '../../components/button/button';

export interface VehicleData {
  nombre: string;
  placa: string;
  sector: string;
  estado: 'ONLINE' | 'OFFLINE';
  imagen: string;
  asignado: string;
}

@Component({
  selector: 'app-vehicle-card',
  standalone: true,
  imports: [ButtonComponent],
  templateUrl: './vehicle-card.html',
})
export class VehicleCard {
  @Input({ required: true }) data!: VehicleData;
}
